import logging

import hikari
import lightbulb
from lightbulb.ext import tasks
import os
from dotenv import load_dotenv

import marisa.help
from marisa import help

load_dotenv()

log = logging.getLogger('MARISA')

bot = lightbulb.BotApp(
    token=os.getenv('BOT_TOKEN'),
    prefix='$',
    default_enabled_guilds=int(os.getenv('DEFAULT_GUILD_ID')),
    banner='marisa',
    allow_color=False,
)

tasks.load(bot)

bot.load_extensions_from('./marisa/extensions')


@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command(name='reload', description='reload commands', hidden=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def reload(ctx: lightbulb.Context):
    bot.reload_extensions(
        'marisa.extensions.General',
        'marisa.extensions.Gelbooru',
        'marisa.extensions.Random',
        'marisa.extensions.Twitter'
    )

    await ctx.respond("Extensions reloaded?")
bot.command(reload)

@lightbulb.option(name="command", description="Name of command", required=False)
@lightbulb.command(name="help", description="help")
@lightbulb.implements(lightbulb.SlashCommand)
async def help_cmd(ctx: lightbulb.Context):
    if ctx.options.command:
        await bot.help_command.send_command_help(ctx, bot.get_slash_command(ctx.options.command))
        return
    await bot.help_command.send_bot_help(ctx)

bot.help_command = marisa.help.CustomHelp(bot)
bot.command(help_cmd)


@bot.listen(hikari.GuildMessageDeleteEvent)
async def do_something(event: hikari.GuildMessageDeleteEvent):
    print(f"Message deleted by {event.old_message.author}: {event.old_message.content}")


@bot.listen(lightbulb.SlashCommandInvocationEvent)
async def on_command_use(event: lightbulb.SlashCommandInvocationEvent):
    await bot.rest.trigger_typing(channel=event.context.channel_id)


@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, hikari.NotFoundError):
        if event.context.command.name == 'info':
            await event.context.respond('User is not found')
        return

    if isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(content=f"You are on cooldown for this command. Please retry in {int(exception.retry_after)} seconds", delete_after=10.0)
        return

    raise exception


if __name__ == '__main__':

    # use uvloop if on Unix machine
    if os.name != 'nt':
        import uvloop

        uvloop.install()

    bot.run(
        activity=hikari.Activity(
            name="Reimu clean the shrine",
            type=hikari.ActivityType.WATCHING
        )
    )
