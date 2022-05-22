import hikari
import lightbulb
from dotenv import load_dotenv

load_dotenv('../')

plugin = lightbulb.Plugin('General')


def generate_response(user: hikari.User) -> str:
    res = f"{user} info:\n"
    res += f"Join date: {user.created_at.strftime('%m/%d/%Y')}\n"
    res += f"id: {user.id}\n"
    res += f"Bot Status: {'Is a bot' if user.is_bot else 'Not a bot'}\n"
    res += f"Avatar URL: {user.avatar_url}\n"

    return res


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

            await ctx.respond(generate_response(user))
            return

        user: hikari.User = ctx.author
        await ctx.respond(generate_response(user))
    except TypeError:
        await ctx.respond(f"That didn't work :(")


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
