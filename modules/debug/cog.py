from discord.ext import commands
import discord


class Debug(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="module",
                    aliases=["m"])
    @commands.is_owner()
    async def module(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid command passed.")

    @module.command(name="unload",
                    aliases=["u", "ul"])
    async def module_unload(self, ctx, *, name):
        self.bot.unload_extension("modules." + name + ".cog")

        self.bot.log(f"Unloaded module {name}.")
        await ctx.send(f"Unloaded module {name}.")

    @module.command(name="load",
                    aliases=["l"])
    async def module_load(self, ctx, *, name):
        self.bot.load_extension("modules." + name + ".cog")

        self.bot.log(f"Loaded module {name}.")
        await ctx.send(f"Loaded module {name}.")

    @module.command(name="reload",
                    aliases=["r", "rl"])
    async def module_reload(self, ctx, *, name):
        self.bot.reload_extension("modules." + name + ".cog")

        self.bot.log(f"Reloaded module {name}.")
        await ctx.send(f"Reloaded module {name}.")

    @module.command(name="list",
                    aliases=["li"])
    async def module_list(self, ctx):
        await ctx.send("```" + "".join(f"{module}: {len(self.bot.get_module(module).get_commands())} command(s)\n" for module in self.bot.modules) + "```")

    @commands.command(name="eval")
    @commands.is_owner()
    async def owner_eval(self, ctx, *, query):
        try:
            if query[:6] == "await ":
                k = await eval(query[6:], locals())
                if k is not None:
                    await ctx.send(k)
            else:
                k = eval(query, locals())
                if k is not None:
                    await ctx.send(k)
        except Exception as ex:
            await ctx.send(f"```{ex}```")

    @commands.command(name="exec")
    @commands.is_owner()
    async def owner_exec(self, ctx, *, query):
        try:
            exec(query, locals())
        except Exception as ex:
            await ctx.send(f"```{ex}```")


def setup(bot):
    bot.add_cog(Debug(bot))
