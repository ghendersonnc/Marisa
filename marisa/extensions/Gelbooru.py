import hikari
import lightbulb
from dotenv import load_dotenv
from pygelbooru import Gelbooru as GB
import os

load_dotenv('../')

gb = GB(os.getenv('GELBOORU_API_KEY'), os.getenv('GELBOORU_USER_ID'))


plugin = lightbulb.Plugin('Gelbooru')


@plugin.command
@lightbulb.option(name='tags', description='Tags should be formated as such: tag_one tag_two', required=False)
@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@lightbulb.command(name='gelbooru', description='Random image from gelbooru', auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def gelbooru(ctx: lightbulb.Context) -> None:
    if ctx.options.tags:
        if any(tag in ctx.options.tags for tag in ['loli', 'shota']):
            await ctx.respond('Nice try.')
            return
        tags = ctx.options.tags.split(' ')
        post = await gb.random_post(tags=tags, exclude_tags=['loli', 'shota'])
    else:
        post = await gb.random_post(exclude_tags=['loli', 'shota'])

    gb_url = 'https://gelbooru.com/index.php?page=post&s=view&id='
    embed = hikari.Embed(title='GELBOORU IMAGE', url=f"{gb_url}{int(post)}")
    embed.set_image(str(post))
    await ctx.respond(embed=embed)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
