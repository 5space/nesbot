import random

import discord
from discord.ext.commands.converter import UserConverter

from modules.games.uno_vars import *
from modules.games.util.game import TurnBasedGame, Rules
# from utils.embed import prompt_channel


def _is_sublist(lst1, lst2):
    """ls1 = [element for element in lst1 if element in lst2]
    ls2 = [element for element in lst2 if element in lst1]
    return ls1 == ls2"""
    ls2 = lst2.copy()
    for element in lst1:
        if element in ls2:
            ls2.remove(element)
        else:
            return False
    return True


class UnoRules(Rules):

    keys = ["cards", "jumpins", "stacking", "trains", "sevenzero"]

    def __init__(self):
        super().__init__()
        self._cards = 7
        self._jumpins = True
        self._stacking = True
        self._trains = False
        self._sevenzero = False

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, value):
        if not value.isdigit() or not (1 <= int(value) <= 20):
            raise ValueError("Invalid value (must be between 1 and 20)")
        self._cards = int(value)

    @property
    def jumpins(self):
        return self._jumpins

    @jumpins.setter
    def jumpins(self, value):
        if value not in ["true", "false"]:
            raise ValueError("Invalid value (must be true or false)")
        self._jumpins = value == "true"

    @property
    def stacking(self):
        return self._stacking

    @stacking.setter
    def stacking(self, value):
        if value not in ["true", "false"]:
            raise ValueError("Invalid value (must be true or false)")
        self._stacking = value == "true"

    @property
    def trains(self):
        return self._trains

    @trains.setter
    def trains(self, value):
        if value not in ["true", "false"]:
            raise ValueError("Invalid value (must be true or false)")
        self._trains = value == "true"

    @property
    def sevenzero(self):
        return self._sevenzero

    @sevenzero.setter
    def sevenzero(self, value):
        if value not in ["true", "false"]:
            raise ValueError("Invalid value (must be true or false)")
        self._sevenzero = value == "true"


class HandView(discord.ui.View):

    def __init__(self, game, player, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game
        self.player = player
        self.hand = self.game.hands[self.player]

        for card in self.hand:
            button = discord.ui.Button(emoji=CARD_EMOJIS[card], style=discord.ButtonStyle.gray)
            self.add_item(button)


class UnoView(discord.ui.View):

    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game
    
    @discord.ui.button(label="Resend Hand", style=discord.ButtonStyle.red)
    async def resendhand(self, button, interaction):
        player = interaction.user
        if player in self.game.players:
            await self.game.send_hand(player)
    
    @discord.ui.button(label="Leave Game", style=discord.ButtonStyle.red)
    async def leave(self, button, interaction):
        player = interaction.user
        if player in self.game.players:
            self.game.remove_player(player)


class Uno(TurnBasedGame):

    min_players = 1
    max_players = 20
    name = "UNO"

    def __init__(self, channel, players):
        super().__init__(channel, players)
        self.top_card = None
        self.hands = {}
        self.rules = UnoRules()

        self.draw_train = 0
        self.is_in_draw_train = False
        self.last_player = None

        self.can_be_called = set()

    async def remove_player(self, player):
        if player not in self.players:
            return

        if len(self.players) > 2 and self.playing:
            if player in self.hands:
                self.hands.pop(player)
            if player in self.can_be_called:
                self.can_be_called.remove(player)
            if player == self.get_turn():
                self.next_turn()
        await super().remove_player(player)
        if self.playing and len(self.players) > 0:
            await self.send_hand(self.get_turn())

    def can_play(self, card):
        if self.is_in_draw_train:
            return card[1] in CARD_SPECIALS and (card[1] in CARD_WILDS or self.top_card[0] == COLOR_WILD
                                                 or card[0] == self.top_card[0] or card[1] == self.top_card[1])
        else:
            return card[1] in CARD_WILDS or self.top_card[0] == COLOR_WILD \
                or card[0] == self.top_card[0] or card[1] == self.top_card[1]

    def can_stack(self, card, before=None):
        if self.rules.sevenzero and card[1] in (0, 7):
            return False
        if before is None:
            before = self.top_card
        if before[1] > 9 or card[1] > 9:
            return False
        if before[0] == card[0]:
            return (before[1] - card[1]) % 10 in (0, 1, 9)
        else:
            return before[1] == card[1]

    def can_train(self, card, before=None):
        if self.rules.sevenzero and card[1] in (0, 7):
            return False
        if before is None:
            before = self.top_card
        if before[1] > 9 or card[1] > 9:
            return False
        return (before[1] - card[1]) % 10 in (0, 1, 2, 8, 9)

    def can_jumpin(self, card):
        if not self.rules.jumpins:
            return False
        if self.rules.sevenzero and card[1] in (0, 7):
            return False
        return card[1] < 10

    def rotate_hands(self):
        n = len(self.players)
        if self.is_reversed:
            self.hands = {self.players[i]: self.hands[self.players[(i+1) % n]] for i in range(n)}
        else:
            self.hands = {self.players[i]: self.hands[self.players[(i-1) % n]] for i in range(n)}

    async def send_hand(self, player, turn=True):
        try:
            msg = "You have the following cards in your hand:\n" \
                  + ", ".join(CARD_EMOJIS[k] + " " + CARD_STRINGS[k] for k in self.hands[player])
            if turn:
                msg = chr(0x17b5) + "\nIt's your turn!\n" + msg
            else:
                msg = chr(0x17b5) + "\n" + msg
            dm = await player.create_dm()
            await dm.send(msg + "\n\nTop card:\n" + CARD_EMOJIS[self.top_card] + " " + CARD_STRINGS[self.top_card])
        except AttributeError:
            pass

    async def deal(self, player, amount):
        dealt = [random.choice(CARDS) for _ in range(amount)]
        self.hands[player] += dealt
        await self.send_hand(player, turn=False)

    async def start(self):
        await super().start()
        self.hands = {player: [] for player in self.players}
        self.top_card = random.choice(CARDS)
        for player in self.players:
            await self.deal(player, self.rules.cards)
        if self.rules.cards <= 1:
            self.can_be_called = set(self.players)
        await self.display()

    def get_display(self, passed_msg="It is currently **{0}'s** turn."):
        lines = [passed_msg.format(self.get_turn().name),
                 f"Top card: {CARD_EMOJIS[self.top_card]} {CARD_STRINGS[self.top_card]}\n"]

        def ordinal(n):
            return "%d%s" % (n, "tsnrhtdd"[(int(n/10) % 10 != 1) * (n % 10 < 4) * n % 10::4])
        for player in self.players:
            if player == self.get_turn():
                lines.append(f"{player.name} ({len(self.hands[player])} cards) **Now**")
            elif player == self.get_turn(1):
                lines.append(f"{player.name} ({len(self.hands[player])} cards) **Next**")
            else:
                indicator = ordinal(((self.players.index(player) - self.turn) * (-1 if self.is_reversed else 1))
                                    % len(self.players) + 1)
                lines.append(f"{player.name} ({len(self.hands[player])} cards) {indicator}")
        return "\n".join(lines)

    async def display(self, passed_msg="It is currently **{0}'s** turn."):
        if self.top_card is not None:
            await self.send(self.get_display(passed_msg))

    async def draw(self, player):
        await self.deal(player, self.draw_train)
        await self.send(f"{player.name} has drawn {self.draw_train} cards.")

        self.next_turn()
        self.draw_train = 0
        self.is_in_draw_train = False

    async def call_uno(self, message, player, query):
        ctx = await self.handler.bot.get_context(message)
        try:
            user = await UserConverter().convert(ctx, query)
            if user not in self.players or user == player or user not in self.can_be_called:
                return
            self.can_be_called.remove(user)
            await self.deal(user, 2)
            await self.send(f"{user.name} has drawn 2 cards.")
        except Exception:
            return

    async def swap_hands(self, channel, player):
        user = None

        def message_check(m):
            nonlocal user
            try:
                """ctx = await self.handler.bot.get_context(m)
                user = await UserConverter().convert(ctx, m.content)"""
                return user in self.players
            except Exception:
                return False

        async def timeout_callback(_):
            nonlocal user
            players_temp = self.players.copy()
            players_temp.remove(player)
            user = random.choice(players_temp)
            await channel.send(f"You took too long, and the player {user} has been randomly selected.")

            self.hands[player], self.hands[user] = self.hands[user], self.hands[player]

        async def callback(_, __):
            if user is None:
                await timeout_callback(_)
            else:
                self.hands[player], self.hands[user] = self.hands[user], self.hands[player]

        # TODO
        # await prompt_channel(self.handler.bot, channel, player,
        #                      "Choose a player to swap with:", callback, message_check=message_check,
        #                      timeout_callback=timeout_callback)
        self.next_turn()

    async def play_card(self, channel, player, card, called_uno=False):
        if card[0] == COLOR_WILD:
            def message_check(m):
                return m.channel == channel and m.author == player \
                       and m.content.lower() in ["red", "green", "yellow", "blue"]

            async def callback(_, m):
                color = [COLOR_RED, COLOR_GREEN, COLOR_YELLOW, COLOR_BLUE][["red", "green", "yellow", "blue"]
                                                                           .index(m.content.lower())]
                self.top_card = (color, card[1])

            async def timeout_callback(_):
                color = random.randint(0, 3)
                color_id = [COLOR_RED, COLOR_GREEN, COLOR_YELLOW, COLOR_BLUE][color]
                color_string = ["red", "green", "yellow", "blue"][color]
                await channel.send(f"You took too long, and the color {color_string} has been randomly selected.")

                self.top_card = (color_id, card[1])

            # TODO
            # await prompt_channel(self.handler.bot, channel, player,
            #                      "Choose a color:", callback, message_check=message_check,
            #                      timeout_callback=timeout_callback)
        else:
            self.top_card = card
        if card[1] in CARD_WILDS:
            card = (COLOR_WILD, card[1])
        self.hands[player].remove(card)
        self.last_player = player

        if card[1] == CARD_REVERSE:
            self.is_reversed = not self.is_reversed
            if len(self.players) == 2 and not self.is_in_draw_train:
                self.next_turn()
        elif card[1] == CARD_SKIP:
            if not self.is_in_draw_train:
                self.next_turn()
        elif card[1] == CARD_DRAWTWO:
            self.is_in_draw_train = True
            self.draw_train += 2
        elif card[1] == CARD_DRAWFOUR:
            self.is_in_draw_train = True
            self.draw_train += 4
        elif card[1] == CARD_DRAWEIGHT:
            self.is_in_draw_train = True
            self.draw_train += 8
        elif card[1] == CARD_SHUFFLEHANDS:
            await self.swap_hands(channel, player)

        if len(self.hands[player]) == 0:
            self.winner = player
            await self.end()
            return
        elif len(self.hands[player]) == 1 and not called_uno:
            self.can_be_called.add(player)

        if card[1] != CARD_SHUFFLEHANDS:
            self.next_turn()
        if self.is_in_draw_train:
            if not any(self.can_play(c) for c in self.hands[self.get_turn()]):
                await self.draw(self.get_turn())
                self.is_in_draw_train = False

        # if self.get_turn() != player:  # Don't dm hand again if it stays your turn
        self.last_player = player
        await self.send_hand(self.get_turn())
        await self.display()

    async def play_train(self, _, player, cards, called_uno=False):
        self.top_card = cards[-1]
        for card in cards:
            if card in self.hands[player]:
                self.hands[player].remove(card)
        self.last_player = player

        if len(self.hands[player]) == 0:
            self.winner = player
            await self.end()
            return
        elif len(self.hands[player]) == 1 and not called_uno:
            self.can_be_called.add(player)

        self.next_turn()
        # if self.get_turn() != player:  # Don't dm hand again if it stays your turn
        self.last_player = player
        await self.send_hand(self.get_turn())
        await self.display()

    async def on_message(self, message):
        await super().on_message(message)

        # Do not allow other players to do anything
        if message.author not in self.players:
            return

        # Calling uno on another player
        if message.content.lower().startswith("uno") and len(self.can_be_called) != 0 and " " in message.content:
            await self.call_uno(message, message.author, message.content[message.content.index(" ")+1:])
            return
        elif message.content.lower() in ("uno", "uno!"):
            if message.author in self.can_be_called:
                self.can_be_called.remove(message.author)
            return

        # Preventing random turns if you cannot stack or jump in
        if not (self.rules.jumpins or self.rules.stacking) and message.author != self.get_turn():
            return
        msg = message.content.lower()
        called_uno = False

        tokens = msg.split(" && ")
        if tokens[-1] in ("uno", "uno!"):
            called_uno = True
            tokens.pop()

        if len(tokens) == 0:
            return
        elif len(tokens) == 1:
            msg = tokens[0]
            if msg in CARD_STRINGS_REVERSED:
                card = CARD_STRINGS_REVERSED[msg]
            else:
                return

            if card not in self.hands[message.author] and not (card[1] >= 13
                                                               and (COLOR_WILD, card[1]) in self.hands[message.author]):
                await self.send("You do not have that card.")
                return

            if message.author != self.get_turn():
                if self.rules.jumpins and card == self.top_card and self.can_jumpin(card):  # Only works with numbers
                    self.turn = self.players.index(message.author)
                    await self.play_card(message.channel, message.author, card, called_uno=called_uno)
                elif message.author == self.last_player:
                    if (self.rules.trains and self.can_train(card)) or (self.rules.stacking and self.can_stack(card)):
                        self.turn = self.players.index(message.author)
                        await self.play_card(message.channel, message.author, card, called_uno=called_uno)
                return

            if not self.can_play(card):
                await self.send("Invalid move.")
                return

            await self.play_card(message.channel, message.author, card, called_uno=called_uno)
        else:
            if not all(c in CARD_STRINGS_REVERSED for c in tokens):  # Cards aren't valid
                return
            cards = [CARD_STRINGS_REVERSED[c] for c in tokens]
            if not _is_sublist(cards, self.hands[message.author]):  # User doesn't have all cards
                return
            # Stack isn't valid
            if not (self.rules.trains and all(self.can_train(cards[i], cards[i-1]) for i in range(1, len(cards)))
                    or self.rules.stacking and all(self.can_stack(cards[i], cards[i-1]) for i in range(1, len(cards)))):
                return

            if message.author != self.get_turn():
                if self.rules.jumpins and cards[0][1] < 10 and cards[0] == self.top_card:  # Only works with numbers
                    self.turn = self.players.index(message.author)
                    await self.play_train(message.channel, message.author, cards, called_uno)
                elif message.author == self.last_player:
                    if self.rules.trains and self.can_train(cards[0]) or self.rules.stacking and self.can_stack(cards[0]):
                        self.turn = self.players.index(message.author)
                        await self.play_train(message.channel, message.author, cards, called_uno)
            else:
                if self.can_play(cards[0]):
                    await self.play_train(message.channel, message.author, cards, called_uno)

    async def end(self):
        await super().end()
        if self.winner is None:
            await self.send("There was a tie and nobody received points.")
        else:
            # self.handler.add_tokens(self.channel.guild, self.winner.id, 5)
            await self.send(f"Winner: **{self.winner.name}**\n\n"
                            f"Top card: {CARD_EMOJIS[self.top_card]} {CARD_STRINGS[self.top_card]}")
