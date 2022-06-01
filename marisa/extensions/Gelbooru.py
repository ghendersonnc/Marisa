import os
import hikari
import lightbulb
from dotenv import load_dotenv
import aiohttp

load_dotenv('../../.env')

plugin = lightbulb.Plugin('Gelbooru')


async def random_post(tags: list = None, exclude_tags: list = None):
    booru_tags = [tag.strip().lower().replace(' ', '_') for tag in tags] if tags else []
    booru_tags += ['-' + tag.strip().lstrip('-').lower().replace(' ', '_') for tag in
                   exclude_tags] if exclude_tags else []

    booru_tags.append('sort:random')
    booru_tags = ' '.join(booru_tags)
    request_url = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=1&tags={booru_tags}&api_key={os.getenv('GELBOORU_API_KEY')}&user_id={os.getenv('GELBOORU_USER_ID')}"

    async with aiohttp.ClientSession() as session:
        async with session.get(request_url) as response:
            if response.status != 200:
                return None
            result = await response.json()
            result = result if 'post' in result else None
    return result


async def respond(ctx: lightbulb.Context, payload: dict, marisa_invoked: bool):
    gb_url = 'https://gelbooru.com/index.php?page=post&s=view&id='
    GELBOORU_BLUE = 0x0773FB

    embed = hikari.Embed(
        title='Gelbooru Post',
        url=f"{gb_url}{payload['post'][0]['id']}",
        color=hikari.Color(GELBOORU_BLUE),
        description=f"{ctx.options.tags if ctx.options.tags else ''}"
    )

    if marisa_invoked:
        footer_content = f"Plain URL to post: {gb_url}{payload['post'][0]['id']}\n\n"
        footer_content += f"AMOUNT OF SFW MARISAS ON GELBOORU: {payload['@attributes']['count']}"
        embed.set_footer(footer_content)
        embed.set_image(payload['post'][0]['file_url'])
        await ctx.respond(embed=embed)
        return

    embed.set_footer(f"Plain URL to post: {gb_url}{payload['post'][0]['id']}")
    embed.set_image(payload['post'][0]['file_url'])
    await ctx.respond(embed=embed)


@plugin.command
@lightbulb.option(name='tags', description='Tags should be formated as such: tag_one tag_two', required=False)
@lightbulb.option(name='rating',
                  description='Rating. Pick between General, Sensitive, Questionable, Explicit',
                  required=False,
                  choices=['general', 'sensitive', 'questionable', 'explicit']
                  )
@lightbulb.add_cooldown(length=600.0, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command(name='gelbooru', description='Random image from gelbooru')
@lightbulb.implements(lightbulb.SlashCommand)
async def gelbooru(ctx: lightbulb.Context) -> None:
    owner_id = await ctx.command.app.fetch_owner_ids()

    if ctx.author.id == owner_id[0]:
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

    if ctx.options.tags:
        if any(tag in ctx.options.tags for tag in ['loli', 'shota']):
            await ctx.respond('Nice try.')
            return
        tags = ctx.options.tags.split(' ')
        tags.append(f"rating:{ctx.options.rating}") if ctx.options.rating else None
        payload = await random_post(tags=tags, exclude_tags=['loli', 'shota'])
    else:
        payload = await random_post(exclude_tags=['loli', 'shota'])

    if not payload:
        await ctx.respond('No post :(')
        return

    await respond(ctx, payload, False)


@plugin.command
@lightbulb.add_cooldown(length=600.0, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command(name='marisa', description='MARISA GELBOORU')
@lightbulb.implements(lightbulb.SlashCommand)
async def marisa(ctx: lightbulb.Context):
    owner_id = await ctx.command.app.fetch_owner_ids()

    if ctx.author.id == owner_id[0]:
        await ctx.command.cooldown_manager.reset_cooldown(ctx)

    payload = await random_post(tags=['kirisame marisa', 'rating:general', '1girl'], exclude_tags=['loli', 'shota'])

    await respond(ctx, payload, True)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
