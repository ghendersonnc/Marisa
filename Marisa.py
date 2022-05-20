import hikari
import lightbulb
from lightbulb.ext import tasks
import os
from dotenv import load_dotenv
import marisa
load_dotenv()

bot = lightbulb.BotApp(
    token=os.getenv('BOT_TOKEN'),
    prefix='$',
    default_enabled_guilds=int(os.getenv('DEFAULT_GUILD_ID'))
)

tasks.load(bot)

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

previous_marisa_count = 0

@tasks.task(h=1, auto_start=True)
async def check_marisa():
    global previous_marisa_count
    marisa_count = marisa.extensions.Gelbooru.check_for_marisa()

    await bot.rest.create_message(
        channel=int(os.getenv('MARISA_COUNT_UPDATE_CHANNEL_ID')),
        content=f"@everyone There has been {marisa_count - previous_marisa_count} Marisa Kirisame artworks uploaded to Gelbooru since last check ({marisa_count} total)",
        mentions_everyone=True
    )
    previous_marisa_count = marisa_count


if __name__ == '__main__':

    # use uvloop if on Unix machine
    if os.name != 'nt':
        import uvloop
        uvloop.install()

    bot.run()
