import asyncio
import math
import random

from modules.games.util.game import Game

ROLE_MAFIA = 0
ROLE_DOCTOR = 1
ROLE_DETECTIVE = 2
ROLE_CITIZEN = 3


async def prompt_user(bot, user, text, callback, message_check=None):

    dm = await user.create_dm()
    prompt = await dm.send(text)

    if message_check is None:
        def message_check(m):
            return m.author == user

    try:
        msg = await bot.wait_for("message", check=message_check, timeout=30.0)
        await callback(prompt, msg)
    except asyncio.TimeoutError:
        await dm.send("Took too long.")
        return


async def prompt_mafia(bot, user, text, callback):

    def message_check(m):
        return m.author == user and m.content.isnumeric()
    await prompt_user(bot, user, text, callback, message_check)


class Mafia(Game):

    min_players = 4
    max_players = 10
    name = "Mafia"

    def __init__(self, handler, channel, players):
        super().__init__(handler, channel, players)
        self.roles = {}
        self.day = 1

    def get_display(self):
        return str(self.players)

    async def start(self):
        await super().start()
        mafia_count = math.floor(len(self.players)/3)
        doctor_count = 1
        detective_count = 1
        citizen_count = len(self.players) - mafia_count - doctor_count - detective_count
        roles = [ROLE_MAFIA] * mafia_count + [ROLE_DOCTOR] * doctor_count \
            + [ROLE_DETECTIVE] * detective_count + [ROLE_CITIZEN] * citizen_count
        random.shuffle(roles)

        self.roles = {player: 0 for player in self.players}
        for i in range(len(self.players)):
            self.roles[self.players[i]] = roles[i]

        await self.send(self.roles)

    async def night(self):
        to_kill = []

        async def mafia_callback(prompt, msg):
            pass

        async def doctor_callback(prompt, msg):
            pass

        async def detective_callback(prompt, msg):
            pass

        for player in self.players:
            if self.roles[player] == ROLE_MAFIA:
                await prompt_mafia(self.handler.bot, player, "Choose a player to kill:", mafia_callback)
            elif self.roles[player] == ROLE_DOCTOR:
                await prompt_mafia(self.handler.bot, player, "Choose a player to save:", doctor_callback)
            elif self.roles[player] == ROLE_DETECTIVE:
                await prompt_mafia(self.handler.bot, player, "Choose a player to investigate:", detective_callback)

    async def on_message(self, message):
        pass

    async def display(self):
        await self.send(self.get_display())

    async def end(self):
        await super().end()
        sorted_scores = sorted(self.points.items(), key=lambda kv: kv[1])
        if max(self.lives.values()) <= 0:
            await self.send(f"The creator of the game ({self.owner.mention}) won as nobody guessed the phrase.")
        else:
            self.winner = sorted_scores[0][0]
            # self.handler.add_tokens(self.channel.guild, self.winner.id, 10)
            await self.send(f"Winner: {self.winner.mention} ({sorted_scores[0][1]} points).")
