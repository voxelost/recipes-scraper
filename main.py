from recipe_scrapers import scrape_me
from discord.ext import commands
import config

bot = commands.Bot(command_prefix='!', case_insensitive=True,
                   owner_id=config.OWNER_ID, self_bot=False)


@bot.command()
async def recipe(ctx):

    await ctx.send('ą')

bot.run(config.BOT_TOKEN)
