import os
import discord
import requests
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
from lxml import html

client = discord.Client()
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


@client.event
async def on_ready():
    for guild in client.guilds:
        print(
            f'{client.user} is connected to the following guild:\n\n'
            f'{guild.name} (with id {guild.id})'
        )
        break


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "!afzal":
        gotoschool, raison = get_meteo()[0], get_meteo()[1]
        if not gotoschool:
            await message.channel.send("Pena lekol acoz ena " + raison)
            await message.channel.send("Copyright keethesh#4492, ban moV voler")
        elif gotoschool:
            await message.channel.send("Aret fer paresse, ena lekol demain.")
            await message.channel.send("Copyright keethesh#4492, ban moV voler")
    # elif message.content == "!screenshot":
    #     e = discord.Embed(title="Screenshot", description="http://metservice.intnet.mu/")
    #     download_screenshot()
    #     await message.channel.send_file("screenshot.jpeg", content="...", filename="...")
    #     file = discord.File("filepath.png", filename="...")
    #     await message.channel.send(embed=e)
    elif message.content == "!stp":
        await message.channel.send("!svp pour afficher ce message")
        await message.channel.send("!afzal pour voir si y'a ecole ou pas")
        # await message.channel.send("!screenshot pour avoir une screen du site de la meteo")


def get_meteo():
    response = requests.get("http://metservice.intnet.mu/")
    doc = html.fromstring(response.content)
    texte = doc.xpath("//*[@id=\"content\"]/div[2]/div/div[1]/p/marquee/a/span")[0].text.strip()

    if fuzz.partial_ratio(texte, "fortes") >= 75:
        ecole = False
        reason = "lapli fort"

    elif fuzz.partial_ratio(texte, "torrentielles") >= 75:
        ecole = False
        reason = "lapli torrentiel."

    elif fuzz.partial_ratio(texte, "classe I" or "classe 1") >= 75:
        ecole = True
        reason = "ene cyclone classe I."

    elif fuzz.partial_ratio(texte, "classe II" or "classe 2") >= 75:
        ecole = False
        reason = "ene cyclone classe II."

    elif fuzz.partial_ratio(texte, "classe III" or "classe 3") >= 75:
        ecole = False
        reason = "ene cyclone classe III."

    elif fuzz.partial_ratio(texte, "classe IV" or "classe 4") >= 75:
        ecole = False
        reason = "ene cyclone classe IV."

    elif fuzz.partial_ratio(texte, "classe V" or "classe 5") >= 75:
        ecole = False
        reason = "ene cyclone classe V."

    else:
        ecole = True
        reason = "Ena lekol"
    return ecole, reason


def download_screenshot():
    apiflash_access_key = "043019f3a4a84a86b4a6a7d4bf52e98c"
    url = "http://metservice.intnet.mu/"
    response = requests.get(
        "https://api.apiflash.com/v1/urltoimage?access_key=" + apiflash_access_key + "&url=" + url).content
    with open("screenshot.jpeg", "wb+") as f:
        f.write(response)
    return


client.run(TOKEN)
