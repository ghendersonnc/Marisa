from datetime import datetime
from datetime import timedelta
from random import randrange
import os
import aiohttp
from pprint import pprint

import hikari
import lightbulb
from dotenv import load_dotenv

load_dotenv('../../.env')

plugin = lightbulb.Plugin('Twitter')

async def get_elon() -> dict:
    utc_24h_ago = (datetime.utcnow() - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")

    request_url = f"https://api.twitter.com/2/users/44196397/tweets?max_results=100&start_time={utc_24h_ago}&tweet.fields=created_at"
    async with aiohttp.ClientSession(headers={"Authorization": f"Bearer {os.getenv('TWITTER_BEARER_TOKEN')}"}) as session:
        async with session.get(url=request_url) as response:
            if response.status != 200:
                return None
            response_data = await response.json()

            if response_data['meta']['result_count'] == 0:
                return None

            return response_data['data'][randrange(0, response_data['meta']['result_count'])]


@plugin.command
@lightbulb.add_cooldown(length=600.0, uses=1, bucket=lightbulb.GuildBucket)
@lightbulb.command("elon", description="twittererer")
@lightbulb.implements(lightbulb.SlashCommand)
async def elon(ctx: lightbulb.Context):
    response = await get_elon()

    if not response:
        await ctx.respond("Could not get any tweets! He may not have tweeted in OVER 24 hours OR Twitter is rate limiting me.")
        return

    await ctx.respond(f"https://twitter.com/elonmusk/status/{response['id']}")


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
