# bot.py
import os

import discord
from dotenv import load_dotenv
import random

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} im in')


joining = None
players = {}  # voor de dictiony
spelers = []  # voor de permissions
roleNumbers = []
playerNames = []
rolesList = []
lovers = []
already_joined_amount = 0
testing = False
done = None

cupidomessage = False
zienermessage = False
weerwolfmessage = False
heksmessage = False
stemmessage = False

weerwolven = []
votes = []
votes_dict = {}
deathlist = []
slachtoffers = []
slachtoffers_dict = {}
meeste_stemmen = 0
alGestemd = []
tie_message = "Het is gelijkspel tussen"
tie = False
tie_list = []
monarchvote = []
monarch_dict = {}
monarch_message = False

cupido_done = False
ziener_done = False
weerwolf_done = False
heks_done = False
monarch_done = False
stemmen_done = False


@client.event
async def on_message(message):
    message.content = message.content.lower()
    global testing
    global cupidomessage
    global ziener_done

    if client.user == message.author:
        return

    weerwolf_channel = discord.utils.get(message.guild.text_channels, name="weerwolf_channel")
    if message.channel == weerwolf_channel:
        await meisje(message)

    if message.content.startswith("wolfies"):
        print("wolfies")
        players.update({398769543482179585: "Burger"})
        players.update({440892872867184640: "Burger"})
        players.update({481456565254225920: "Burger"})
        players.update({627172201082388500: "Weerwolf"})

        weerwolven.append(125979540924268544)
        weerwolven.append(627172201082388500)
        weerwolven.append(497826023707115522)

        print(players)
        while not geweerwolved:
            print("geweerwolvd")
            await weerwolf(message)

    if message.content.startswith("start weerwolven"):
        await playerjoining(message)

    global created_channels
    text_channel_list = []
    if message.content.startswith("delete channels"):
        for channel in message.guild.text_channels:
            text_channel_list.append(channel)
        for channel in text_channel_list:
            if channel.name in created_channels:
                await channel.delete()

    if message.content.startswith("reveal"):
        await permissies(message)

    if message.content.startswith("meesa cupido"):
        cupidomessage = False
        while len(lovers) < 2:
            await cupido(message)

    ziener_channel = discord.utils.get(message.guild.text_channels, name="ziener_channel")
    if message.content.startswith("fifafofum"):
        print("a")
        ziener_done = False
        players.update({message.author.id: "Ziener"})
        players.update({398769543482179585: "Weerwolf"})
        while not ziener_done:
            print("---")
            await ziener(message)
            if not ziener_done:
                await ziener_channel.send("Dat is geen speler.")


created_channels = []
possible_channels = ["main_channel", "weerwolf_channel", "burger_channel", "ziener_channel", "heks_channel",
                     "jager_channel",
                     "cupido_channel", "meisje_channel", "dood_channel"]


async def create_channels(s):
    overwrites = {
        s.guild.default_role: discord.PermissionOverwrite(view_channel=False)}

    for e in range(0, len(possible_channels)):
        await s.guild.create_text_channel(name=possible_channels[e], reason="startup", overwrites=overwrites)
        created_channels.append(possible_channels[e])

    main_channel = discord.utils.get(s.guild.text_channels, name="main_channel")
    main_over = discord.PermissionOverwrite()
    main_over.view_channel = True
    await main_channel.set_permissions(s.guild.default_role, overwrite=main_over)


async def playerjoining(s):
    global joining
    global players

    main_channel = discord.utils.get(s.guild.text_channels, name="main_channel")
    await main_channel.send("Stuur \"ik\" om mee te doen!")
    joining = True

    while joining:
        def check(m):
            return client.user != s.author \
                   and m.content == "ik" \
                   or m.content == "disable joining"

        msg = await client.wait_for("message", check=check)
        msg.content = msg.content.lower()

        if msg.author not in players and "ik" in msg.content and msg.channel == main_channel:
            await msg.channel.send(f"<@{msg.author.id}> is gejoined")
            players.update({msg.author.id: "geen rol"})

        elif msg.author in players and "ik" in msg.content and msg.channel == main_channel:
            await msg.channel.send(f"<@{msg.author.id}> already joined")

        if msg.content.startswith("disable joining"):
            if len(players) < 6:
                await msg.channel.send("Er zijn niet genoeg spelers, mensen kunnen nog joinen!")
            if len(players) >= 6:
                await msg.channel.send("Er zijn genoeg spelerNames, rollen worden uitgedeelt!")
                joining = False
            break
    role_selector()
    await permissies(s)
    print("Done")
    await pre_game(main_channel)


async def pre_game(r):
    await r.send(
        "Het ingeslapen kakdorpje Wakkerdam wordt sinds enige tijd belaagd door weerwolven! "
        "Elke nacht veranderen bepaalde bewoners van het gehucht in mensverslindende wolven, "
        "die afschuwelijke moorden plegen... Moorden, die het daglicht niet kunnen verdragen... "
        "Wat pas nog een eeuwenoude legende was, is plotseling op onverklaarbare wijze brute "
        "realiteit geworden! Jullie dorpelingen zullen je moeten verenigen om je van deze "
        "plaag te ontdoen, en zo te zorgen, dat minstens enkelen van jullie dit griezelige avontuur"
        " overleven!")


async def dood(r):
    global players
    global deathlist

    all_channels = ["main_channel", "weerwolf_channel", "burger_channel", "ziener_channel", "heks_channel",
                    "jager_channel", "cupido_channel", "meisje_channel", "dood_channel"]
    for victim in deathlist:
        override = discord.PermissionOverwrite()
        override.view_channel = True
        override.send_messages = False
        players[victim] = "Dood"
        for i in range(0, len(all_channels)):
            name = all_channels[i]
            channel = discord.utils.get(r.guild.text_channels, name=name)
            victor = await client.fetch_user(victim)
            await channel.set_permissions(victor, overwrite=override)


# Gives each player a role. Returns a dict.
def role_selector():
    print(players)
    global rolesList
    rolesList = []

    roles = {"Weerwolf": len(players) // 6,
             "Burger": 1,
             "Ziener": 1,
             "Heks": 1,
             "Jager": 1,
             "Cupido": 1,
             "Het Onschuldige Meisje": 1}
    roles["Burger"] = len(players) - roles["Weerwolf"] - (len(roles) - 2)

    # maakt een lijst met de rollen en hoe vaak ze er zijn

    for role in roles:
        for g in range((int(roles[role]))):
            rolesList.append(role)

    playerRoles = distribute_roles(players, rolesList)
    print(playerRoles)


# Distributes roles from rolesList to players
async def distribute_roles(gamers, roles):
    playerNamesList = list(gamers)
    global weerwolven

    for j in range(0, len(gamers)):
        rNumber = random.randrange(len(roles))
        gamers[playerNamesList[j]] = roles[rNumber]
        del roles[rNumber]

    for i in players:
        g = await client.fetch_user(i)
        if "Weerwolf" == players[i]:
            weerwolven.append(g.name)

    return gamers


async def cupido(g):
    global lovers
    global cupidomessage
    global players

    playerIdList = list(players)

    cupido_channel = discord.utils.get(g.guild.text_channels, name="cupido_channel")
    if not cupidomessage:
        await cupido_channel.send("Cupido, wie wil jij koppelen?")
        cupidomessage = True

    def check(m):
        return client.user != g.author \
               and m.content.startswith("!")

    msg = await client.wait_for("message", check=check)
    if msg.channel == cupido_channel:
        for i in range(len(players)):
            lover = await client.fetch_user(playerIdList[i])
            if lover.name.lower() in msg.content.lower():
                if lover.name.lower() not in lovers:
                    lovers.append(lover)
                    await cupido_channel.send(f"{lover.name} is now in love")
                    print(lovers)
                else:
                    await cupido_channel.send("Narcisten zijn niet toegestaan")
    if len(lovers) == 2:
        await cupido_channel.send(f"{lovers[0].name} en {lovers[1].name} zijn nu elkaars geliefden.")
        lover1_dm = await lovers[0].create_dm()
        await lover1_dm.send(f"Jij en {lovers[1].name} zijn geliefden.")
        lover2_dm = await lovers[1].create_dm()
        await lover2_dm.send(f"Jij en {lovers[0].name} zijn geliefden.")


async def ziener(e):
    global players
    global zienermessage
    global ziener_done

    playerIdList = list(players)
    ziener_channel = discord.utils.get(e.guild.text_channels, name="ziener_channel")

    if not zienermessage:
        await ziener_channel.send("Wiens identiteit wil jij ontrafelen?")
        zienermessage = True

    def check(m):
        return client.user != e.author \
               and m.content.startswith("!")

    msg = await client.wait_for("message", check=check)
    if msg.content.startswith("!") and msg.channel == ziener_channel:
        if msg.author.name.lower() in msg.content.lower():
            await ziener_channel.send("Dat ben je zelf.")
        else:
            for i in range(len(players)):
                gepaparazzod = await client.fetch_user(playerIdList[i])
                if gepaparazzod.name.lower() in msg.content.lower():
                    await ziener_channel.send(f"{gepaparazzod.name} is {players[playerIdList[i]]}!")
                    ziener_done = True


async def weerwolf(j):
    global weerwolfmessage
    global weerwolf_done
    global deathlist
    global weerwolven
    global slachtoffers
    global slachtoffers_dict
    global meeste_stemmen
    global alGestemd
    global tie_message
    global tie
    global tie_list
    het_slachtoffer = None

    weerwolf_channel = discord.utils.get(j.guild.text_channels, name="weerwolf_channel")
    if not weerwolfmessage:
        await weerwolf_channel.send(
            "Hallo wolfjes, wordt het met elkaar eens wie je dood wilt hebben en geef dan hun naam met ![name]")
        weerwolfmessage = True

    def check(m):
        return client.user != j.author \
               and m.content.startswith("!")

    playersIdList = list(players)

    msg = await client.wait_for("message", check=check)
    if msg.content.startswith("!") and msg.channel == weerwolf_channel:
        for i in range(0, len(weerwolven)):
            y = await client.fetch_user(weerwolven[i])
            if y.name.lower() in msg.content.lower():
                await weerwolf_channel.send("Je kunt geen weerwolf vermoorden")
                return
        if msg.author.name not in alGestemd:
            for i in range(0, len(playersIdList)):
                z = await client.fetch_user(playersIdList[i])
                if z.name.lower() in msg.content.lower():
                    slachtoffers.append(z)
                    alGestemd.append(msg.author.name)
                    await weerwolf_channel.send(f"{msg.author.name} heeft op {z.name} gestemd")
        else:
            await weerwolf_channel.send(f"{msg.author.name} je hebt al gestemd.")
            return

        if len(slachtoffers) == len(weerwolven):
            for i in slachtoffers:
                if i not in slachtoffers_dict:
                    slachtoffers_dict.update({i: 1})
                else:
                    slachtoffers_dict.update({i: slachtoffers_dict[i] + 1})
            print(slachtoffers_dict)

            slachtofferz = list(slachtoffers_dict)

            for i in range(0, len(slachtoffers_dict)):
                print(slachtoffers_dict[slachtofferz[i]])

                if slachtoffers_dict[slachtofferz[i]] == meeste_stemmen:
                    tie_list.append(slachtofferz[i])
                    if het_slachtoffer is not None and het_slachtoffer not in tie_list:
                        tie_list.append(het_slachtoffer)
                    tie = True

                if slachtoffers_dict[slachtofferz[i]] > meeste_stemmen:
                    if tie:
                        tie = False
                        tie_list = []
                    het_slachtoffer = slachtofferz[i]
                    meeste_stemmen = slachtoffers_dict[slachtofferz[i]]

            if tie:
                for i in range(0, len(tie_list)):
                    if i == len(tie_list) - 1:
                        tie_message = tie_message + " & " + str(tie_list[i]) + "."
                    elif i == 0:
                        tie_message = tie_message + " " + str(tie_list[i])
                    else:
                        tie_message = tie_message + ", " + str(tie_list[i])
                await weerwolf_channel.send(tie_message)
                await weerwolf_channel.send("stem opnieuw maar nu op dezelfde aub")
                slachtoffers_dict = {}
                slachtoffers = []
                alGestemd = []
                meeste_stemmen = 0
                tie_list = []
                tie_message = "Het is gelijkspel tussen"
            else:
                await weerwolf_channel.send(f"{het_slachtoffer.name} is vermoord!")
                deathlist.append(het_slachtoffer)
                print(deathlist)
                weerwolf_done = True
                slachtoffers_dict = {}
                slachtoffers = []
                alGestemd = []
                meeste_stemmen = 0
                tie_list = []


async def heks(b):
    global players
    global heksmessage
    global heks_done

    playerIdList = list(players)
    heks_channel = discord.utils.get(b.guild.text_channels, name="heks_channel")

    if heksmessage:
        await heks_channel.send(
            f"Hallo geniepige gemenerik, wil je liever {deathlist[0].name} redden,"
            f" iemand anders ook te vermoorden of lekker rustig blijven genieten van het moment?")
        await heks_channel.send(
            "Gebruik eenmaal in het spel \"red\" om het weerwolf slachtoffer te redden."
            " Gebruik eenmaal in het spel \"dood _naam_\" om het slachtoffer en nog een ander te vermoorden."
            " Gebruik \"ik geniet\" om je beurt voorbij te laten gaan!")
        heksmessage = False

    def check(m):

        return client.user != b.author \
               or m.content.startswith("red") \
               or m.content.startswith("dood") \
               or m.content.startswith("ik geniet")

    msg = await client.wait_for("message", check=check)
    msg.content = msg.content.lower()

    if msg.content.startswith("red"):
        heks_channel.send(f"{deathlist[0].name} is gered!")
        heks_done = True

    slachtoffer = deathlist[0]

    if msg.content.startswith("dood"):
        heks_channel.send(f"{slachtoffer.name} is gedood")
        for i in range(len(players)):
            lijk = await client.fetch_user(playerIdList[i])
            if lijk.name.lower() in msg.content:
                await heks_channel.send("")
                deathlist.append(lijk)
        heks_done = True

    if msg.content.startswith("ik geniet"):
        await heks_channel.send("Een goede keuze is gemaakt.")
        heks_done = True


async def meisje(x):
    meisje_channel = discord.utils.get(x.guild.text_channels, name="meisje_channel")
    await meisje_channel.send(x.content)


async def stemmen(q):
    global players
    main_channel = discord.utils.get(q.guild.text_channels, name="main_channel")
    playerIdList = list(players)
    global votes
    global votes_dict
    global alGestemd
    global meeste_stemmen
    global tie_message
    global tie
    global tie_list
    vermoord = None
    global stemmen_done

    def check(m):
        return client.user != q.author \
               and m.content.startswith("!")

    msg = await client.wait_for("message", check=check)
    msg.content = msg.content.lower()

    if msg.content.startswith("!") and msg.channel == main_channel:
        for i in range(0, len(weerwolven)):
            y = await client.fetch_user(weerwolven[i])
            if y.name.lower() in msg.content.lower():
                await main_channel.send("Je kunt geen weerwolf vermoorden")
                return
        if msg.author.name not in alGestemd:
            for i in range(0, len(playerIdList)):
                z = await client.fetch_user(playerIdList[i])
                if z.name.lower() in msg.content.lower():
                    votes.append(z)
                    alGestemd.append(msg.author.name)
                    await main_channel.send(f"{msg.author.name} heeft op {z.name} gestemd")
        else:
            await main_channel.send(f"{msg.author.name} je hebt al gestemd.")
            return

        if len(votes) == len(weerwolven):
            for i in votes:
                if i not in votes_dict:
                    votes_dict.update({i: 1})
                else:
                    votes_dict.update({i: votes_dict[i] + 1})
            print(votes_dict)

            votez = list(votes_dict)

            for i in range(0, len(votes_dict)):
                print(votes_dict[votez[i]])

                if votes_dict[votez[i]] == meeste_stemmen:
                    tie_list.append(votez[i])
                    if vermoord is not None and vermoord not in tie_list:
                        tie_list.append(vermoord)
                    tie = True

                if votes_dict[votez[i]] > meeste_stemmen:
                    if tie:
                        tie = False
                        tie_list = []
                    vermoord = votez[i]
                    meeste_stemmen = votes_dict[votez[i]]

            if tie:
                for i in range(0, len(tie_list)):
                    if i == len(tie_list) - 1:
                        tie_message = tie_message + " & " + str(tie_list[i]) + "."
                    elif i == 0:
                        tie_message = tie_message + " " + str(tie_list[i])
                    else:
                        tie_message = tie_message + ", " + str(tie_list[i])
                await main_channel.send(tie_message)
                await main_channel.send("stem opnieuw maar nu op dezelfde aub")
                votes_dict = {}
                votes = []
                alGestemd = []
                meeste_stemmen = 0
                tie_list = []
                tie_message = "Het is gelijkspel tussen"
            else:
                await main_channel.send(f"{vermoord.name} is opgehangen!")
                stemmen_done = True
                votes_dict = {}
                votes = []
                alGestemd = []
                meeste_stemmen = 0
                tie_list = []


async def monarchvoting(k):
    global players
    global gestemd
    main_channel = discord.utils.get(k.guild.text_channels, name="main_channel")
    playerIdList = list(players)
    global alGestemd
    global meeste_stemmen
    global tie_message
    global tie
    global tie_list
    global monarchvote
    global monarch_dict
    global monarchspeech_message
    vermoord = None

    if not monarchspeech_message:
        await main_channel.send("Stem nu allemaal op je favoriete koning.")
        monarchspeech_message = True

    def check(m):
        return client.user != k.author \
               and m.content.startswith("!")

    msg = await client.wait_for("message", check=check)
    msg.content = msg.content.lower()

    if msg.content.startswith("!") and msg.channel == main_channel:
        if msg.author.name not in alGestemd:
            if msg.author.name.lower() in msg.content.lower():
                await main_channel.send(f"{msg.author.name} je kan niet op jezelf stemmen")
                return
            else:
                for i in range(0, len(playerIdList)):
                    z = await client.fetch_user(playerIdList[i])
                    if z.name.lower() in msg.content.lower():
                        monarchvote.append(z)
                        alGestemd.append(msg.author.name)
        else:
            await main_channel.send(f"{msg.author.name} je hebt al gestemd.")
            return

        if len(monarchvote) == len(alivePlayers):
            for i in monarchvote:
                if i not in monarch_dict:
                    monarch_dict.update({i: 1})
                else:
                    monarch_dict.update({i: monarch_dict[i] + 1})

            monark = list(monarch_dict)

            for i in range(0, len(monarch_dict)):
                print(monarch_dict[monark[i]])

                if monarch_dict[monark[i]] == meeste_stemmen:
                    tie_list.append(monark[i])
                    if vermoord is not None and vermoord not in tie_list:
                        tie_list.append(vermoord)
                    tie = True

                if monarch_dict[monark[i]] > meeste_stemmen:
                    if tie:
                        tie = False
                        tie_list = []
                    vermoord = monark[i]
                    meeste_stemmen = monarch_dict[monark[i]]

            if tie:
                for i in range(0, len(tie_list)):
                    if i == len(tie_list) - 1:
                        tie_message = tie_message + " & " + str(tie_list[i]) + "."
                    elif i == 0:
                        tie_message = tie_message + " " + str(tie_list[i])
                    else:
                        tie_message = tie_message + ", " + str(tie_list[i])
                await main_channel.send(tie_message)
                await main_channel.send("stem opnieuw maar nu op dezelfde aub")
                monarch_dict = {}
                monarchvote = []
                alGestemd = []
                meeste_stemmen = 0
                tie_list = []
                tie_message = "Het is gelijkspel tussen"
            else:
                await main_channel.send(f"{vermoord.name} is opgehangen!")
                gestemd = True
                monarch_dict = {}
                monarchvote = []
                alGestemd = []
                meeste_stemmen = 0
                tie_list = []

async def avond(a):
    await create_channels(a)
    await playerjoining(a)


async def eerste_nacht(j):
    await cupido(j)


async def elke_nacht(k):
    global players
    playerIdList = list(players)
    main_channel = discord.utils.get(k.guild.text_channels, name="main_channel")

    override = discord.PermissionOverwrite()
    override.view_channel = False
    for i in playerIdList:
        member = client.fetch_user(i)
        await main_channel.set_permissions(member, overwrite=override)

    await ziener(k)
    await weerwolf(k)
    await heks(k)


async def dag(r):
    global players
    playerIdList = list(players)
    main_channel = discord.utils.get(r.guild.text_channels, name="main_channel")

    for i in playerIdList:
        member = client.fetch_user(i)
        await main_channel.set_permissions(member, overwrite=None)

    await stemmen(r)


async def permissies(r):
    override = discord.PermissionOverwrite()
    override.view_channel = True

    for e in players:
        if "Cupido" == players[e]:
            print(f"<@{e}> is cupido")
            cupido_channel = discord.utils.get(r.guild.text_channels, name="cupido_channel")
            cupidor = await client.fetch_user(e)
            await cupido_channel.set_permissions(cupidor, overwrite=override)

        if "Weerwolf" == players[e]:
            print(f"<@{e}> is weerwolv")
            weerwolf_channel = discord.utils.get(r.guild.text_channels, name="weerwolf_channel")
            weerwolfor = await client.fetch_user(e)
            await weerwolf_channel.set_permissions(weerwolfor, overwrite=override)

        if "Burger" == players[e]:
            print(f"<@{e}> is Burger")
            burger_channel = discord.utils.get(r.guild.text_channels, name="burger_channel")
            burger = await client.fetch_user(e)
            await burger_channel.set_permissions(burger, overwrite=override)

        if "Ziener" == players[e]:
            print(f"<@{e}> is Ziener")
            ziener_channel = discord.utils.get(r.guild.text_channels, name="ziener_channel")
            zieneror = await client.fetch_user(e)
            await ziener_channel.set_permissions(zieneror, overwrite=override)

        if "Heks" == players[e]:
            print(f"<@{e}> is Heks")
            heks_channel = discord.utils.get(r.guild.text_channels, name="heks_channel")
            heksor = await client.fetch_user(e)
            await heks_channel.set_permissions(heksor, overwrite=override)

        if "Jager" == players[e]:
            print(f"<@{e}> is Jager")
            jager_channel = discord.utils.get(r.guild.text_channels, name="jager_channel")
            jageror = await client.fetch_user(e)
            await jager_channel.set_permissions(jageror, overwrite=override)

        if "Het Onschuldige Meisje" == players[e]:
            print(f"<@{e}> is Het Onschuldige Meisje")
            meisje_channel = discord.utils.get(r.guild.text_channels, name="meisje_channel")
            meisjor = await client.fetch_user(e)
            await meisje_channel.set_permissions(meisjor, overwrite=override)


client.run(TOKEN)
