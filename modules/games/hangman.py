import asyncio

from modules.games.util.game import Game

HANGMAN_EMOJI_HEAD = "<:head:542748031196332051>"

HANGMAN_EMOJIS_ARMS = ["<:arms0:542748031393464320>",
                       "<:arms1:542748031494258708>",
                       "<:arms2:542748031573950464>"]

HANGMAN_EMOJIS_LEGS = ["<:legs1:542748031460835328>",
                       "<:legs2:542748031456641064>"]


async def prompt_user(bot, user, text, callback, message_check=None):

    dm = await user.create_dm()
    prompt = await dm.send(text)

    if message_check is None:
        def message_check(m):
            return m.author == user and m.channel == dm

    try:
        msg = await bot.wait_for("message", check=message_check, timeout=30.0)
        await callback(prompt, msg)
    except asyncio.TimeoutError:
        await dm.send("Took too long.")
        return


async def prompt_hangman(bot, user, text, callback):

    def message_check(m):
        return m.author == user and len(m.content) <= 30
    await prompt_user(bot, user, text, callback, message_check)


class Hangman(Game):

    min_players = 2
    max_players = 5
    name = "Hangman"

    def __init__(self, handler, channel, players):
        super().__init__(handler, channel, players)
        self.letters_used = []
        self.string = str()
        self.can_play = False
        self.lives = {}
        self.points = {}

    def get_hangman(self, player):
        lives = self.lives[player]
        hangman = HANGMAN_EMOJI_HEAD
        if lives >= 2:
            hangman += "\n" + HANGMAN_EMOJIS_ARMS[2]
        else:
            hangman += "\n" + HANGMAN_EMOJIS_ARMS[lives]
        if lives >= 3:
            hangman += "\n" + HANGMAN_EMOJIS_LEGS[lives-3]
        else:
            hangman += "\n"
        return player.name + "\n" + str(hangman)

    def get_string_display(self):
        string = list(self.string)
        for i, ch in enumerate(string):
            if ch.lower() in "abcdefghijklmnopqrstuvwxyz" and ch.lower() not in self.letters_used:
                string[i] = "_"
        return "".join(string)

    def check_done(self):
        for ch in "abcdefghijklmnopqrstuvwxyz":
            if ch in self.string and ch not in self.letters_used:
                return False
        return True

    def get_display(self):
        lines = "\n".join(self.get_hangman(player) for player in self.players
                          if player != self.owner) + "\n`" + self.get_string_display() + "`"
        return lines

    async def start(self):
        await super().start()
        self.lives = {player: 4 for player in self.players}  # if player != self.owner}
        self.points = {player: 0 for player in self.players}  # if player != self.owner}

        async def callback(_, msg):
            self.string = msg.content
            self.can_play = True
            await self.display()

        await self.send(f"**{self.owner.name}** is choosing a phrase.")
        await prompt_hangman(self.handler.bot,
                             self.owner,
                             "Choose a word or phrase (1 to 30 characters):",
                             callback)

    async def on_message(self, message):
        await super().on_message(message)
        if message.author not in self.players or message.author == self.owner:
            return
        if not self.can_play:
            return
        if message.content.lower() == self.string.lower():
            self.points[message.author] += 5
            await self.send(message.author.mention + " guessed the phrase. (+5 points)")
            await self.end()
        letter = message.content.lower()
        if letter not in "abcdefghijklmnopqrstuvwxyz":
            return
        if self.lives[message.author] == 0:
            return
        if letter in self.letters_used:
            await self.send("That letter has already been guessed.")
            return
        self.letters_used.append(letter)
        if letter in self.string.lower():
            self.points[message.author] += 1
            await self.send(message.author.mention + " guessed the letter " + letter + " correct. (+1 point)\n"
                            + self.get_display())
            if self.check_done():
                await self.end()
        else:
            self.lives[message.author] -= 1
            if self.lives[message.author] <= 0:
                await self.send(message.author.mention + " guessed the letter " + letter
                                + " wrong and is now out of lives.\n" + self.get_display())
                if max(self.lives.values()) <= 0:
                    await self.end()
            else:
                await self.send(message.author.mention + " guessed the letter " + letter
                                + " wrong and lost a life.\n" + self.get_display())

    async def display(self):
        await self.send(self.get_display())

    async def end(self):
        await super().end()
        sorted_scores = sorted(self.points.items(), key=lambda kv: -kv[1])
        if max(self.lives.values()) <= 0:
            await self.send(f"The creator of the game ({self.owner.mention}) won as nobody guessed the phrase.")
        else:
            self.winner = sorted_scores[0][0]
            # self.handler.add_tokens(self.channel.guild, self.winner.id, 10)
            await self.send(f"Winner: **{self.winner.name}** ({sorted_scores[0][1]} points).\n"
                            f"They received +10 tokens for winning.")
