import os
import discord
import requests
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
from lxml import html
import keep_alive
from datetime import datetime, timedelta

client = discord.Client()
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


@client.event
async def on_ready():
    for guild in client.guilds:
        print(f'{client.user} is connected to the following guild:\n'
              f'{guild.name} (with id {guild.id})\n')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    author = message.author
    message_time = (message.created_at + timedelta(hours=3)).strftime("%d/%m/%Y %H:%M")

    if message.content == "!afzal":
        print(str(message_time) + " | " + str(message.guild) + ": " + str(author) + " has sent command \"!afzal\"")
        title = "Kiken pe rode koner si ena lekol..."
        desc = "alors li ine ecrire !afzal\n" \
               "Source code available [here](https://github.com/keethesh/PenaLekolBot)"
        name = "Eski ena lekol?"
        embed = discord.Embed(title=title, url="http://metservice.intnet.mu/", description=desc, color=0x8564dd)
        embed.set_author(name="PenaLekolBot")
        embed.set_footer(text="Made by keethesh#4492")
        gotoschool, raison = get_meteo()[0], get_meteo()[1]
        time = datetime.now() + timedelta(hours=5)
        day = time.weekday()
        if not gotoschool and not day == (5 or 6):
            embed.add_field(name=name,
                            value="Pena lekol acoz ena " + raison + " Ek en plis weekend la, couyon!", inline=True)

        elif not gotoschool and day == (5 or 6):
            embed = discord.Embed(title=title, description=desc, color=0x8564dd)
            embed.set_author(name="PenaLekolBot")
            embed.add_field(name=name, value="Pena lekol acoz ena " + raison, inline=True)

        elif gotoschool and day == (5 or 6):
            embed = discord.Embed(title=title, description=desc, color=0x8564dd)
            embed.set_author(name="PenaLekolBot")
            embed.add_field(name=name, value="Ti kapav ena lekol, mais nous dans weekend. To bien gopia.",
                            inline=True)

        elif gotoschool and not day == (5 or 6):
            embed = discord.Embed(title=title, description=desc, color=0x8564dd)
            embed.set_author(name="PenaLekolBot")
            embed.add_field(name=name, value="Aret fer paresse, ena lekol demain.", inline=True)

        await message.channel.send(embed=embed)

    # elif message.content == "!screenshot":
    #     e = discord.Embed(title="Screenshot", description="http://metservice.intnet.mu/")
    #     download_screenshot()
    #     await message.channel.send_file("screenshot.jpeg", content="...", filename="...")
    #     file = discord.File("filepath.png", filename="...")
    #     await message.channel.send(embed=e)
    elif message.content == "!stp":
        await message.channel.send("!stp pour afficher ce message")
        await message.channel.send("!afzal pour voir si y'a ecole ou pas")
        # await message.channel.send("!screenshot pour avoir une screen du site de la meteo")


def get_meteo():
    response = requests.get("http://metservice.intnet.mu/")
    doc = html.fromstring(response.content)
    texte = doc.xpath("//*[@id=\"content\"]/div[2]/div/div[1]/p/marquee/a/span"
                      )[0].text.strip()

    if fuzz.partial_ratio(texte, "fortes") >= 75:
        ecole = False
        reason = "ene avis lapli fort"

    elif fuzz.partial_ratio(texte, "torrentielles") >= 75:
        ecole = False
        reason = "ene avis lapli torrentiel."

    elif fuzz.partial_ratio(texte, "classe I" or "classe 1") >= 75:
        ecole = True
        reason = "ene alert cyclone classe I."

    elif fuzz.partial_ratio(texte, "classe II" or "classe 2") >= 75:
        ecole = False
        reason = "ene alert cyclone classe II."

    elif fuzz.partial_ratio(texte, "classe III" or "classe 3") >= 75:
        ecole = False
        reason = "ene alert cyclone classe III."

    elif fuzz.partial_ratio(texte, "classe IV" or "classe 4") >= 75:
        ecole = False
        reason = "ene alert cyclone classe IV."

    elif fuzz.partial_ratio(texte, "classe V" or "classe 5") >= 75:
        ecole = False
        reason = "ene alert cyclone classe V."

    else:
        ecole = True
        reason = "Ena lekol"
    return ecole, reason


def download_screenshot():
    apiflash_access_key = "043019f3a4a84a86b4a6a7d4bf52e98c"
    url = "http://metservice.intnet.mu/"
    response = requests.get(
        "https://api.apiflash.com/v1/urltoimage?access_key=" +
        apiflash_access_key + "&url=" + url).content
    with open("screenshot.jpeg", "wb+") as f:
        f.write(response)


keep_alive.keep_alive()

try:
    client.run(TOKEN)
except AttributeError:
    raise ValueError("Token cannot be loaded")
