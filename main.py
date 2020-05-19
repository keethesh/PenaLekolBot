import os
from datetime import datetime, timedelta

import discord
import requests
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
from lxml import html
# from timeloop import Timeloop

client = discord.Client()
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# tl = Timeloop()


def create_embed():
    title = "Verdict..."
    school, raison = get_meteo()
    # time = datetime.now() + timedelta(hours=5)
    time = datetime.now() + timedelta(seconds=10)
    weekend = False
    if time.weekday() == 5 or time.weekday() == 6:
        weekend = True

    if not school and weekend:
        desc = "Pena lekol acoz ena " + raison + " Ek en plis weekend la, couyon!"

    elif not school and not weekend:
        desc = "Pena lekol acoz ena " + raison

    elif school and weekend:
        if raison == "ene alert cyclone classe I.":
            desc = "Meme si ena ene cyclone classe I, ti pou ena lekol si nou pa ti dans weekend. To bien gopia."
        else:
            desc = "Ti kapav ena lekol, mais nous dans weekend. To bien gopia."

    else:
        if raison == "ene alert cyclone classe I.":
            desc = "Meme si ena ene cyclone classe I, ena lekol demain."
        else:
            desc = "Aret fer paresse, ena lekol demain."

    return title, desc


# @tl.job(interval=timedelta(hours=5))
# def automate_checks():
    # school, raison = get_meteo()[0], [1]
    # channel = client.get_channel(687591883643289624)
    # school = False
    # if not school:
    #     await channel.send("@everyone Pena lekol!!!!! ")

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
        title, desc = create_embed()
        embed = discord.Embed(title=title, description=desc, color=0x8564dd)
        embed.set_author(name="Pena Lekol Bot (click to view code)", url="https://github.com/keethesh/PenaLekolBot")
        embed.set_footer(text="Made by keethesh#4492")
        await message.channel.send("Kiken ine ecrire \"!afzal\", ala rezilta⬇️", embed=embed)

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
        reason = "ene avis lapli fort."

    elif fuzz.partial_ratio(texte, "torrentielles") >= 75:
        ecole = False
        reason = "ene avis lapli torrentiel."

    elif fuzz.partial_ratio(texte, "classe 4") >= 80:
        ecole = False
        reason = "ene alert cyclone classe IV."

    elif fuzz.partial_ratio(texte, "classe 3") >= 80:
        ecole = False
        reason = "ene alert cyclone classe III."

    elif fuzz.partial_ratio(texte, "classe 2") >= 80:
        ecole = False
        reason = "ene alert cyclone classe II."

    elif fuzz.partial_ratio(texte, "classe 1") >= 80:
        ecole = True
        reason = "ene alert cyclone classe I."

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


try:
    client.run(TOKEN)
except AttributeError:
    raise ValueError("Token cannot be loaded")
# tl.start()
