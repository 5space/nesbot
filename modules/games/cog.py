from typing import Union

# from .chess import *
# from .connectfour import *
# from .hangman import *
# from .quiz import *
# from .tictactoe import *
from .uno import *
from .util.game import *


class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.games = {}
    
    @commands.command(name="uno")
    async def uno(self, ctx):
        if ctx.channel in self.games:
            await ctx.send("There is already an UNO game in this channel.")
        else:
            game = Uno(ctx.channel, [ctx.author])
            self.games[ctx.channel] = game
            await game.init()


def setup(bot):
    bot.add_cog(Games(bot))
