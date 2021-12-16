from recipe_scrapers import scrape_me
from discord.ext import commands
import config

bot = commands.Bot(command_prefix='!', case_insensitive=True,
                   owner_id=config.VOXELOST_ID, self_bot=False)


@bot.command()
async def title(ctx):
    print(ctx)
    scraper = scrape_me(
        'https://gwiazdywkuchni.pl/Przepis,smazona-cebulka-ze-skwarkami.php',
        wild_mode=True
    )

    await ctx.send(scraper.title())

bot.run(config.WHISKEY_TOKEN)
