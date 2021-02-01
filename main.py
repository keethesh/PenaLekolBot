import os
from datetime import datetime

import aiohttp
import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
from lxml import html

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = Bot(command_prefix='!', case_insensitive=True)


async def create_embed():
    title = "Eski ena lekol?"
    is_school, reason = await get_meteo()
    time = datetime.now()
    weekend = time.weekday() == 5 or time.weekday() == 6

    if weekend:
        if is_school:
            if reason == "ene alert cyclone classe I.":
                desc = "Meme si ena ene cyclone classe I, ti pou ena lekol si nou pa ti dans weekend. To bien gopia."
            else:
                desc = "Ti kapav ena lekol, mais nous dans weekend. To bien gopia."
        else:
            desc = "Pena lekol acoz ena " + reason + " Ek en plis weekend la, gopia"

    else:
        if not is_school:
            desc = "Pena lekol acoz ena " + reason
        else:
            if reason == "ene alert cyclone classe I.":
                desc = "Meme si ena ene cyclone classe I, ena lekol demain."
            else:
                desc = "Aret fer paresse, ena lekol demain."
    return title, desc


@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(f'{bot.user} is connected to the following guild:\n'
              f'{guild.name} (with id {guild.id})\n')


@bot.command(help="Pour voir si y'a école ou pas")
async def afzal(ctx):
    title, desc = await create_embed()
    embed = discord.Embed(title=title, description=desc, color=0x8564dd)
    embed.set_author(name='PenaLekolBot (click to view code)', url="https://github.com/keethesh/PenaLekolBot")
    embed.set_footer(text='Made by keethesh#4492')
    await ctx.send(embed=embed)


async def get_meteo():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://metservice.intnet.mu') as response:
            doc = html.fromstring(await response.read())
    meteo_text = doc.xpath("//div[@class='warning']//a/span")[0].text.strip()

    possible_states = (('fortes', 75, False, 'ene avis lapli fort.'),
                       ('torrentielles', 75, False, 'ene avis lapli torrentiel.'),
                       ('classe 4', 80, False, 'ene alert cyclone classe 4.'),
                       ('classe 3', 80, False, 'ene alert cyclone classe 3.'),
                       ('classe 2', 80, False, 'ene alert cyclone classe 2.'),
                       ('classe 1', 80, True, 'ene alert cyclone classe 1.'))

    for possibility in possible_states:
        to_match, match_ratio, is_school, description = possibility
        if fuzz.partial_ratio(meteo_text, to_match) >= match_ratio:
            return is_school, description

    return True, 'ena lekol'


try:
    bot.run(TOKEN)
except AttributeError:
    raise ValueError("Token cannot be loaded")
