import hikari
import lightbulb
from dotenv import load_dotenv
import os
import aiohttp

load_dotenv('../../.env')


plugin = lightbulb.Plugin('Gelbooru')


async def random_post(tags: list = None, exclude_tags: list = None):
    booru_tags = [tag.strip().lower().replace(' ', '_') for tag in tags] if tags else []
    booru_tags += ['-' + tag.strip().lstrip('-').lower().replace(' ', '_') for tag in exclude_tags] if exclude_tags else []

    booru_tags.append('sort:random')
    booru_tags = ' '.join(booru_tags)
    url = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=1&tags={booru_tags}&api_key={os.getenv('GELBOORU_API_KEY')}&user_id={os.getenv('GELBOORU_USER_ID')}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.json()
            result = result['post'][0] if 'post' in result else None
    return result


@plugin.command
@lightbulb.option(name='tags', description='Tags should be formated as such: tag_one tag_two', required=False)
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
        post = await random_post(tags=tags, exclude_tags=['loli', 'shota'])
    else:
        post = await random_post(exclude_tags=['loli', 'shota'])

    if not post:
        await ctx.respond('No post :(')
        return

    gb_url = 'https://gelbooru.com/index.php?page=post&s=view&id='
    embed = hikari.Embed(
        title='Gelbooru Image',
        url=f"{gb_url}{post['id']}",
        color=hikari.Color(0x0773FB),
        description=f"{ctx.options.tags if ctx.options.tags else ''}"
    )
    embed.set_footer(f"Plain URL to post: {gb_url}{post['id']}")
    embed.set_image(post['file_url'])
    await ctx.respond(embed=embed)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)


def check_for_marisa():
    ...
