import re
from random import randint
import hikari
import lightbulb
from dotenv import load_dotenv

load_dotenv('../')

plugin = lightbulb.Plugin('General')


def generate_response(user: hikari.Member) -> str:
    res = f"{user} info:\n"
    res += f"Join date: {user.created_at.strftime('%m/%d/%Y')}\n"
    res += f"id: {user.id}\n"
    res += f"Bot Status: {'Is a bot' if user.is_bot else 'Not a bot'}\n"
    res += f"Avatar URL: {user.avatar_url if user.avatar_url else user.default_avatar_url}\n"

    return res


@plugin.command
@lightbulb.option(name='user', description='User', required=False)
@lightbulb.add_cooldown(length=5.0, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command(name='info', description='Info on provided user. Enter user as @user#1234 OR their ID')
@lightbulb.implements(lightbulb.SlashCommand)
async def info(ctx: lightbulb.Context) -> None:
    if not ctx.options.user:
        user: hikari.User = ctx.author
        await ctx.respond(generate_response(user))
        return

    given_id = re.findall('[0-9]+', ctx.options.user)

    if not given_id:
        await ctx.respond("Option must be given using the user's ID (Right click their name then click 'Copy ID' at the bottom of the list) or @user#1234")
        return

    user: hikari.Member = await ctx.command.app.rest.fetch_member(
        guild=ctx.guild_id,
        user=given_id[0]
    )
    print(user.joined_at)
    await ctx.respond(generate_response(user))


@plugin.command
@lightbulb.option(name="message_id", description="ID for message you want to stutter")
@lightbulb.add_cooldown(length=120.0, uses=5, bucket=lightbulb.UserBucket)
@lightbulb.command(name="stutter", description="Stutter a message in the current channel")
@lightbulb.implements(lightbulb.SlashCommand)
async def stutter(ctx: lightbulb.Context):
    res = []
    message_id = None

    try:
        message_id = int(ctx.options.message_id)
    except ValueError:
        await ctx.respond("Input must be a number")
        return

    try:
        message = await ctx.command.app.rest.fetch_message(ctx.channel_id, message_id)
    except hikari.NotFoundError:
        await ctx.respond(f"Message not found. It MUST exist in this channel, which is <#{ctx.channel_id}>.")
        return

    for word in message.content.split():
        if not res:
            stutter_section = f"{word[0]}-{word[0]}-"
            res.append(f"{stutter_section}{word}")
            continue

        stutter_word = randint(1, 12) % 4 == 0

        if not stutter_word:
            res.append(word)
            continue

        stutter_section = f"{word[0]}-{word[0]}-"
        res.append(f"{stutter_section}{word}")
    res = ' '.join(res)
    await ctx.respond(res)

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
