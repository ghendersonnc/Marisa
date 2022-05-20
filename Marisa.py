import hikari
import lightbulb
import os
from dotenv import load_dotenv

load_dotenv()

bot = lightbulb.BotApp(
    token=os.getenv('BOT_TOKEN'),
    prefix='$',
    default_enabled_guilds=int(os.getenv('DEFAULT_GUILD_ID'))
)

bot.load_extensions(
    'marisa.extensions.General',
    'marisa.extensions.Gelbooru',
    'marisa.extensions.Random'
)


@bot.listen(hikari.GuildMessageCreateEvent)
async def on_guild_message(event: hikari.GuildMessageCreateEvent):
    if event.author.is_bot:
        return


@bot.listen(hikari.DMMessageCreateEvent)
async def on_dm_message(event: hikari.DMMessageCreateEvent):
    if event.author.is_bot:
        return

    await event.author.send('fbfbfb')


@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent):

    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(f"You are on cooldown for this command. Please retry in {int(exception.retry_after)} seconds")
    else:
        raise exception

if __name__ == '__main__':

    # use uvloop if on Unix machine
    if os.name != 'nt':
        import uvloop
        uvloop.install()
    bot.run()
