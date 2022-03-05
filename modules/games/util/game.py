from typing import Union

import discord
from discord.ext import commands


DEFAULT_GAME_TOKENS = ["\N{LARGE RED CIRCLE}",
                       "\N{LARGE BLUE CIRCLE}",
                       chr(0x1f7e2),
                       chr(0x1f7e1),
                       "\N{RADIO BUTTON}"]


class GameCheckFailure(commands.CheckFailure):

    def __init__(self, gametype, message=None):
        super().__init__(message)
        self.gametype = gametype


class Rules:

    keys = []

    def __init__(self):
        pass


class LobbyView(discord.ui.View):

    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game
    
    @discord.ui.button(label="Join/Leave", style=discord.ButtonStyle.red)
    async def joinleave(self, button, interaction):
        player = interaction.user
        if player in self.game.players:
            await self.game.remove_player(player)
        else:
            await self.game.add_player(player)
        
        self.game.embed.description = "\n".join(str(player) for player in self.game.players)
        await self.game.update_message()

    @discord.ui.button(label="Start", style=discord.ButtonStyle.green)
    async def start(self, button, interaction):
        if interaction.user != self.game.owner:
            return
        await self.game.start()


class Game:

    min_players = 1
    max_players = 5
    timeout_time = 600
    # timeout_time_lobby = 1200
    name = "Null"

    def __init__(self, channel, players):
        self.rules = Rules()
        self.channel = channel
        self.players = players
        self.owner = players[0]
        self.winner = None
        self.playing = False

        self.message = None
        self.embed = None
        self.view = LobbyView(self)

    async def init(self):
        self.embed = discord.Embed(title=f"{self.name} Game")
        self.message = await self.channel.send(embed=self.embed, view=self.view)

    async def remove_player(self, player):
        if player not in self.players:
            return
        self.players.remove(player)
        if len(self.players) == 0:
            pass
            # remove game
        elif len(self.players) == 1 and self.playing:
            self.winner = self.players[0]
            await self.end()
        else:
            if player == self.owner:
                self.owner = self.players[0]
            await self.update_message()

    async def add_player(self, player):
        if player in self.players:
            return
        self.players.append(player)

    async def start(self):
        self.playing = True

    async def on_message(self, message):
        pass

    async def end(self):
        self.handler.remove_game(self)

    async def update_message(self):
        await self.message.edit(embed=self.embed, view=self.view)


class TurnBasedGame(Game):

    min_players = 2
    max_players = 5

    def __init__(self, channel, players):
        super().__init__(channel, players)
        self.turn = 0
        self.is_reversed = False

    def next_turn(self):
        if self.is_reversed:
            self.turn -= 1
        else:
            self.turn += 1
        self.turn %= len(self.players)

    def get_turn(self, offset=0):
        turn = (self.turn + offset * (-1 if self.is_reversed else 1)) % len(self.players)
        return self.players[turn]

    """
    async def play(self, message):
        await super().play(message)
        if message.author != self.players[self.turn]:
            return
        self.turn += 1
        self.turn %= len(self.players)
        await self.on_turn(self.players[self.turn])
    """

    async def on_turn(self, player):
        await self.channel.send(f"It is now **{player.name}'s** turn.")


class RoundBasedGame(Game):

    def __init__(self, channel, players):
        super().__init__(channel, players)
        self.round = 0
        self.players_done = []

    async def check_round_end(self):
        if len(self.players_done) == len(self.players):
            self.players_done = []
            self.round += 1
            await self.on_round()

    async def remove_player(self, player):
        await super().remove_player(player)
        if player in self.players_done:
            self.players_done.remove(player)

    async def on_player_finish(self, player):
        if player not in self.players_done:
            self.players_done.append(player)
            await self.check_round_end()

    async def on_round(self):
        pass
