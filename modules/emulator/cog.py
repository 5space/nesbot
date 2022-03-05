from discord.ext import commands

from .nes import NESGame
from .atari import AtariGame


class Emulator(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.session = None
    
    @commands.command(name="nes")
    async def nes_start(self, ctx, *, rom: str):
        if self.session is not None:
            await ctx.send(f"A game of {self.session.name} is already in session.")
        else:
            self.session = NESGame(self.bot, ctx.channel, ctx.author, rom)
            await self.session.start()
    
    @commands.command(name="atari")
    async def atari_start(self, ctx, *, rom: str):
        if self.session is not None:
            await ctx.send(f"A game of {self.session.name} is already in session.")
        else:
            self.session = AtariGame(self.bot, ctx.channel, ctx.author, rom)
            await self.session.start()
    
    @commands.command(name="stop")
    async def game_stop(self, ctx):
        if self.session is None:
            await ctx.send(f"There is no game in session.")
        else:
            self.session = None


def setup(bot):
    bot.add_cog(Emulator(bot))
