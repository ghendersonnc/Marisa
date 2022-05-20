import hikari
import lightbulb
from dotenv import load_dotenv

load_dotenv('../')

plugin = lightbulb.Plugin('General')


@plugin.command
@lightbulb.option(name='user', description='User', required=False)
@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@lightbulb.command(name='info', description='Info on provided user. Enter user as @user#1234', auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def info(ctx: lightbulb.Context) -> None:
    try:
        if ctx.options.user:
            converter = lightbulb.UserConverter(ctx.author)
            user = await converter.convert(ctx.options.user[3:-1])

            await ctx.respond(f"{user} joined Discord on {user.created_at.strftime('%m/%d/%Y')}")
        else:
            user: hikari.User = ctx.author
            await ctx.respond(f"{user} joined Discord on {user.created_at.strftime('%m/%d/%Y')}")
    except TypeError:
        await ctx.respond(f"That didn't work :(")


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
