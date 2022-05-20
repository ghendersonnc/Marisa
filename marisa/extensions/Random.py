import os
import random

import lightbulb
from dotenv import load_dotenv

load_dotenv('../')

plugin = lightbulb.Plugin('Random')


@plugin.command
@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@lightbulb.command(name='randomnumber', description='Random number between 1 and 99999', auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def random_number(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"{random.randint(1, 99999)}")


@plugin.command
@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@lightbulb.command(name='randomword', description='Pick a random word from 2000 choices', auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def random_word(ctx: lightbulb.Context) -> None:
    with open('marisa/assets/words.txt') as f:
        word = random.choice(f.read().splitlines())

    await ctx.respond(word)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
