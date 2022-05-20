import hikari
import lightbulb
from dotenv import load_dotenv

load_dotenv('../')


@lightbulb.option(name='user', description='User', required=False)
@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@lightbulb.command(name='info', description='info on user', auto_defer=True)
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


def setup(bot: lightbulb.BotApp) -> None:
    """
    Registers commands
    :param bot: bot to register command to. Should be lightbulb.BotApp
    """
    bot.command(info)
