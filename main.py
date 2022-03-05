import logging
import os
import sys
import traceback

import discord
from discord.ext import commands

import auth


logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
                    datefmt="%y.%m.%d %H:%M:%S",
                    filename="discord.log",
                    filemode="w+")

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s", datefmt="%H:%M:%S"))
logging.getLogger("").addHandler(console)
bot_logger = logging.getLogger("bot.client")


def get_prefix(client, message):
    return commands.when_mentioned_or("%")(client, message)


class NESBot(commands.Bot):

    def __init__(self, logger):
        super().__init__(command_prefix=get_prefix,
                         description=f"Sex",
                         help_attrs=dict(hidden=True))

        self.logger = logger
        self.admin_ids = auth.ADMINS
        self.dump_channel = None

    @staticmethod
    def log(msg):
        bot_logger.info(msg)

    async def update_presence(self):
        name = f"{len(list(self.get_all_members()))} users in {len(self.guilds)} guilds"
        activity = discord.Activity(type=discord.ActivityType.watching,
                                    name=name)
        await self.change_presence(status=discord.Status.online,
                                   activity=activity)

    # Bot events
    async def on_ready(self):
        self.log(f"Logged in as {self.user.name} (ID: {self.user.id})")
        await self.update_presence()

        guild = discord.utils.get(self.guilds, id=851697057584119819)
        self.dump_channel = discord.utils.get(guild.channels, id=851697058057814068)

    async def invoke(self, ctx):
        if ctx.command is not None:
            if ctx.author.id not in self.admin_ids:
                return
        await super().invoke(ctx)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        elif isinstance(error, commands.CheckFailure):
            return
        elif isinstance(error, commands.NotOwner):
            await ctx.send("You do not own this bot.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"\"{error.param}\" is a required argument and is missing.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(str(error))
        else:
            k = True
            if k:
                exc = traceback.format_exception(type(error), error, sys.exc_info()[2])
                await ctx.send("```" + ("".join(exc))[-1994:] + "```")
                await super().on_command_error(ctx, error)
            else:
                await ctx.send("```" + str(error)[:1994] + "```")

    async def on_guild_join(self, guild):
        self.log(f"Joined guild {guild.name}. (ID: {guild.id})")
        await self.update_presence()

    async def on_guild_remove(self, guild):
        self.log(f"Left guild {guild.name}. (ID: {guild.id})")
        await self.update_presence()

    def shut_down(self):
        self.log("Shutting down...")


bot = NESBot(bot_logger)


def main():
    extensions = ["modules." + module + ".cog" for module in os.listdir("modules") if module[0] not in "._"]
    for ext in extensions:
        try:
            bot.load_extension(ext)
        except Exception:
            bot.log(f"Failed to load extension {ext}:")
            bot.log(traceback.format_exc(limit=-1))
    try:
        bot.run(auth.TOKEN)
    finally:
        bot.shut_down()


if __name__ == "__main__":
    main()