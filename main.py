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
alivePlayers = []
rolesList = []
lovers = []
lovas = []
already_joined_amount = 0
testing = False
done = None
de_monarch = None
potentiele_monarch = []
jager_id = None
winnaars = None

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

levensdrank = False
gif = False

gameStart = False

monarch_message = False
cupidomessage = False
zienermessage = False
weerwolfmessage = False
heksmessage = False
stemmessage = False

cupido_done = False
ziener_done = False
weerwolf_done = False
heks_done = False
speech_done = False
monarch_done = False
potentie = True
stemmen_done = False
guild = None
game_active = False
dag_1 = False

heksAlive = True
zienerAlive = True


@client.event
async def on_message(message):
    message.content = message.content.lower()
    global testing
    global cupidomessage
    global ziener_done
    global guild
    global game_active
    global created_channels
    global players

    if client.user == message.author:
        return

    weerwolf_channel = discord.utils.get(message.guild.text_channels, name="weerwolf_channel")
    if message.channel == weerwolf_channel:
        await meisje(message)

    if message.content.startswith("delete channels"):
        text_channel_list = []
        for channel in message.guild.text_channels:
            text_channel_list.append(channel)
        for channel in text_channel_list:
            if channel.name in possible_channels:
                await channel.delete()

    if message.content.startswith("start weerwolven"):
        if not game_active:
            game_active = True
            await start(message)



created_channels = []
possible_channels = ["main_channel", "weerwolf_channel", "ziener_channel", "heks_channel",
                     "cupido_channel", "meisje_channel", "dood_channel"]


async def start(j):
    global guild
    global game_active
    global winnaars

    guild = j.guild
    bericht_gestuurd = j.channel
    await avond(j)
    await eerste_nacht(j)
    while game_active:
        await elke_nacht(j)
        await dag(j)

    if not game_active:
        text_channel_list = []
        for channel in j.guild.text_channels:
            text_channel_list.append(channel)
        for channel in text_channel_list:
            if channel.name in created_channels:
                await channel.delete()
    if not game_active:
        await bericht_gestuurd.send(f"{winnaars} hebben gewonnen!!")
        await bericht_gestuurd.send("Wil je nog een keer spelen?")

        def check(m):
            return client.user != m.author \
                   and m.content == "ja" \
                   or m.content == "nee" \
                   and m.guild == guild

        msg = await client.wait_for("message", check=check)
        msg.content = msg.content.lower()
        if msg.content.startswith("ja"):
            await start(j)

        if msg.content.startswith("nee"):
            await bericht_gestuurd.send("onaardig...")


async def create_channels(s):
    overwrites = {
        s.guild.default_role: discord.PermissionOverwrite(view_channel=False)}

    for e in range(0, len(possible_channels)):
        await s.guild.create_text_channel(name=possible_channels[e], reason="startup", overwrites=overwrites)
        created_channels.append(possible_channels[e])

    main_channel = discord.utils.get(s.guild.text_channels, name="main_channel")


async def playerjoining(s):
    global joining
    global players
    global alivePlayers

    main_channel = discord.utils.get(s.guild.text_channels, name="main_channel")
    await main_channel.send("Stuur \"ik\" om mee te doen! Als iedereen meedoet, stuur \"iedereen doet mee\"!")
    joining = True

    while joining:
        def check(m):
            return client.user != s.author \
                   and m.content == "ik" \
                   or m.content == "iedereen doet mee" \
                   and m.guild == guild

        msg = await client.wait_for("message", check=check)
        msg.content = msg.content.lower()

        if msg.author.id not in players and "ik" in msg.content and msg.channel == main_channel:
            await msg.channel.send(f"<@{msg.author.id}> is gejoined")
            players.update({msg.author.id: "geen rol"})
            alivePlayers.append(msg.author.id)

        elif msg.author.id in players and "ik" in msg.content and msg.channel == main_channel:
            await msg.channel.send(f"<@{msg.author.id}> already joined")

        if msg.content.startswith("iedereen doet mee"):
            if len(players) < 6:
                await msg.channel.send("Er zijn niet genoeg spelers, mensen kunnen nog joinen!")
            elif len(players) >= 6:
                await msg.channel.send("Er zijn genoeg spelers, rollen worden uitgedeeldpl!")
                joining = False
    await role_selector()


async def pre_game(r):
    main_channel = discord.utils.get(r.guild.text_channels, name="main_channel")
    await main_channel.send(
        "BELANGRIJK!!!!! Wanneer ik vraag om iemand te noemen, doe dat met !naam, tenzij anders vermeld!!"
        "Bijvoorbeeld !Rubot")
    await main_channel.send(
        "Het ingeslapen monarchische kakdorpje Wakkerdam wordt sinds enige tijd belaagd door weerwolven! "
        "Elke nacht veranderen bepaalde bewoners van het gehucht in mensverslindende wolven, "
        "die afschuwelijke moorden plegen... Moorden, die het daglicht niet kunnen verdragen... "
        "Wat pas nog een eeuwenoude legende was, is plotseling op onverklaarbare wijze brute "
        "realiteit geworden! Jullie dorpelingen zullen je moeten verenigen om je van deze "
        "plaag te ontdoen, en zo te zorgen, dat minstens enkelen van jullie dit griezelige avontuur"
        " overleven!")


async def dood(r):
    global players
    global deathlist
    global alivePlayers
    global guild
    global stemmen_done
    global jager_id
    global koning
    nieuwekoning = False

    all_channels = ["main_channel", "weerwolf_channel", "ziener_channel", "heks_channel",
                    "cupido_channel", "meisje_channel", "dood_channel"]

    if lovers[0] in deathlist:
        deathlist.append(lovers[1])
    elif lovers[1] in deathlist:
        deathlist.append(lovers[0])

    main_channel = discord.utils.get(r.guild.text_channels, name="main_channel")

    playerIdList = list(players)
    jager_slachtoffer = False
    jager_message = False

    if not stemmen_done:
        await main_channel.send("Het is dag in wakkerdam. Iedereen wordt wakker...")
        if len(deathlist) == 1:
            await main_channel.send(f"Behalve <@{deathlist[0]}>!!")

        if len(deathlist) == 2:
            await main_channel.send(f"Behalve <@{deathlist[0]}> en <@{deathlist[1]}>!!")

        if len(deathlist) == 3:
            await main_channel.send(f"Behalve <@{deathlist[0]}>, <@{deathlist[1]}> en <@{deathlist[2]}>!!")

    if lovers[0] in deathlist and lovers[1] in deathlist:
        await main_channel.send(f"<@{lovers[0]}> en <@{lovers[1]}> waren geliefden")

    for victim in deathlist:
        await main_channel.send(f"<@{victim}> was {players[victim]}")

    if jager_id in deathlist:
        while not jager_slachtoffer:
            if not jager_message:
                await main_channel.send("Jager, wie wordt je slachtoffer?")
                jager_message = True

            def check(m):
                return client.user != m.author \
                       and m.guild == guild

            msg = await client.wait_for("message", check=check)
            msg.content = msg.content.lower()

            if msg.content.startswith("!"):
                if players[msg.author.id] == "Jager":
                    for y in playerIdList:
                        mens = await client.fetch_user(y)
                        if mens.name.lower() in msg.content:
                            deathlist.append(y)
                            if players[mens.id] != "Dood":
                                await main_channel.send(
                                    f"De jager schiet <@{y}> door het hoofd."
                                    f" Iedereen weet dat lood je ware identiteit onthuld en dat "
                                    f"gebeurt nu ook. <@{y}> was {players[y]}.")
                                jager_slachtoffer = True
                            else:
                                await main_channel.send(
                                    "Uhm... Ik weet niet hoe ik dit moet vertellen... \n Hij is al dood...")

    await main_channel.send("Eventjes geduld s'il vous plaît.")

    if monarchvote:
        if koning in deathlist:
            await main_channel.send(f"<@{koning}>, kies je opvolger met ![naam]. (Hij moet levend zijn)...")

            def check(m):
                return client.user != m.author \
                       and m.content.startswith("!") \
                       and m.guild == guild

            while not nieuwekoning:
                msg = await client.wait_for("message", check=check)
                if msg.content.startswith("!") and msg.autor.id == koning:
                    for living in alivePlayers:
                        if living in deathlist:
                            break
                        opvolger = await client.fetch_user(living)
                        if opvolger.name in msg.content:
                            koning = living

    for i in range(len(deathlist)):
        override = discord.PermissionOverwrite()
        override.view_channel = True
        override.send_messages = False
        players[deathlist[i]] = "Dood"
        for y in range(0, len(all_channels)):
            name = all_channels[y]
            channel = discord.utils.get(r.guild.text_channels, name=name)
            victor = await client.fetch_user(deathlist[i])
            await channel.set_permissions(victor, overwrite=override)
    x = len(deathlist)
    for i in range(0, x):
        alivePlayers.remove(deathlist[i])
        deathlist.remove(deathlist[i])




# Gives each player a role. Returns a dict.
async def role_selector():
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

    playerRoles = await distribute_roles(players, rolesList)
    print(playerRoles)


# Distributes roles from rolesList to players
async def distribute_roles(gamers, roles):
    global jager_id
    playerNamesList = list(gamers)

    for j in range(0, len(gamers)):
        rNumber = random.randrange(len(roles))
        gamers[playerNamesList[j]] = roles[rNumber]
        del roles[rNumber]

    for i in playerNamesList:
        player = await client.fetch_user(i)
        player_dm = await player.create_dm()
        await player_dm.send(f"Je bent {gamers[i]}.")

    inverse_players = {value: key for key, value in players.items()}
    jager_id = inverse_players["Jager"]
    return gamers


async def cupido(g):
    global lovers
    global cupidomessage
    global players
    global cupido_done
    global lovas

    playerIdList = list(players)

    cupido_channel = discord.utils.get(g.guild.text_channels, name="cupido_channel")
    if not cupidomessage:
        await cupido_channel.send("Cupido, wie wil jij koppelen? Doe dat met !naam in twee verschillende berichten."
                                  " Dus eerst geliefde 1 in een bericht en dan geliefde 2 in het tweede bericht.")
        cupidomessage = True

    def check(m):
        return client.user != m.author \
               and m.content.startswith("!") \
               and m.guild == guild

    msg = await client.wait_for("message", check=check)
    if msg.channel == cupido_channel:
        for i in range(len(players)):
            lover = await client.fetch_user(playerIdList[i])
            loverid = playerIdList[i]
            if lover.name.lower() in msg.content.lower():
                if loverid not in lovers:
                    lovers.append(loverid)
                    lovas.append(lover)
                    await cupido_channel.send(f"{lover.name} is now in love")
                else:
                    await cupido_channel.send("Narcisten zijn niet toegestaan")
    if len(lovers) == 2:
        await cupido_channel.send(f"{lovas[0].name} en {lovas[1].name} zijn nu elkaars geliefden.")
        lover1_dm = await lovas[0].create_dm()
        await lover1_dm.send(f"Jij en {lovas[1].name} zijn geliefden.")
        lover2_dm = await lovas[1].create_dm()
        await lover2_dm.send(f"Jij en {lovas[0].name} zijn geliefden.")
        cupido_done = True


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
               and m.content.startswith("!") \
               and m.guild == guild

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
        for i in players:
            g = await client.fetch_user(i)
            if "Weerwolf" == players[i]:
                weerwolven.append(g.id)
        await weerwolf_channel.send(
            "Hallo wolfjes, wordt het met elkaar eens wie je dood wilt hebben! Doe dat met !naam.")
        weerwolfmessage = True

    def check(m):
        return client.user != m.author \
               and m.content.startswith("!") \
               and m.guild == guild

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
                    if players[playersIdList[i]] != "Dood":
                        slachtoffers.append(playersIdList[i])
                        alGestemd.append(msg.author.name)
                        await weerwolf_channel.send(f"{msg.author.name} heeft op {z.name} gestemd")
                    else:
                        await weerwolf_channel.send(
                            "Uhm... Ik weet niet hoe ik dit moet vertellen... \n Hij is al dood...")

        else:
            await weerwolf_channel.send(f"{msg.author.name} je hebt al gestemd.")
            return

        print(slachtoffers, weerwolven)

        if len(slachtoffers) == len(weerwolven):
            for i in slachtoffers:
                if i not in slachtoffers_dict:
                    slachtoffers_dict.update({i: 1})
                else:
                    slachtoffers_dict.update({i: slachtoffers_dict[i] + 1})

            slachtofferz = list(slachtoffers_dict)

            for i in range(0, len(slachtoffers_dict)):
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
                de_slachtoffer = await client.fetch_user(het_slachtoffer)
                await weerwolf_channel.send(f"{de_slachtoffer.name} is vermoord!")
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
    global levensdrank
    global gif

    playerIdList = list(players)
    heks_channel = discord.utils.get(b.guild.text_channels, name="heks_channel")

    weerwolf_slachtoffer = await client.fetch_user(deathlist[0])

    if not heksmessage:
        await heks_channel.send(
            f"Hallo geniepige gemenerik, wil je {weerwolf_slachtoffer.name} redden,"
            f" iemand anders vermoorden of lekker rustig blijven genieten van het moment?")
        await heks_channel.send(
            "Gebruik eenmaal in het spel \"red\" om het weerwolf slachtoffer te redden."
            " Gebruik eenmaal in het spel \"dood _naam_\" om het slachtoffer en nog een ander te vermoorden."
            " Gebruik \"ik geniet\" om je beurt voorbij te laten gaan!")
        heksmessage = True

    def check(m):

        return client.user != m.author \
               or m.content.startswith("red") \
               or m.content.startswith("dood") \
               or m.content.startswith("ik geniet") \
               and m.guild == guild

    msg = await client.wait_for("message", check=check)
    msg.content = msg.content.lower()

    if msg.content.startswith("red"):
        if not levensdrank:
            await heks_channel.send(f"{weerwolf_slachtoffer.name} is gered!")
            deathlist.remove(deathlist[0])
            heks_done = True
            levensdrank = True
        else:
            await heks_channel.send("Je hebt geen levensdrank meer...")

    if msg.content.startswith("dood"):
        if not gif:
            for i in range(len(players)):
                lijk = await client.fetch_user(playerIdList[i])
                if lijk.name.lower() in msg.content:
                    if players[playerIdList[i]] != "Dood":
                        if playerIdList[i] not in deathlist:
                            await heks_channel.send(f"{lijk.name} is ook gedood")
                            deathlist.append(playerIdList[i])
                            heks_done = True
                            gif = True
                    else:
                        await heks_channel.send(
                                "Uhm... Ik weet niet hoe ik dit moet vertellen... \n Hij is al dood...")
        else:
            await heks_channel.send("Je heb geen gif meer...")

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
    global alivePlayers
    global meeste_stemmen
    global tie_message
    global tie
    global tie_list
    global stemmen_done
    global monarchvote
    global koning
    vermoord = None
    print("stem functie is aanwezig")

    def check(m):
        return client.user != q.author \
               and m.content.startswith("!") \
               and m.guild == guild

    if not stemmessage:
        await main_channel.send(
            "Heeft iemand nog iets verdachts gemerkt gisteravond? "
            "Bespreek met elkaar verdachte dingen en als je eruit bent, stem dan door !naam te doen!")

    msg = await client.wait_for("message", check=check)
    msg.content = msg.content.lower()
    if msg.content.startswith("!") and msg.channel == main_channel:
        if msg.author.name not in alGestemd:
            print("staat niet in algestemd")
            for i in range(0, len(playerIdList)):
                z = await client.fetch_user(playerIdList[i])
                if z.name.lower() in msg.content.lower():
                    if monarchvote:
                        if koning == msg.author.id:
                            votes.append(playerIdList[i])
                    votes.append(playerIdList[i])
                    alGestemd.append(msg.author.name)
                    await main_channel.send(f"{msg.author.name} heeft op {z.name} gestemd")
        else:
            await main_channel.send(f"{msg.author.name} je hebt al gestemd.")
            return
        print("heeft iedereen gestemd?")
        if len(votes) == len(alivePlayers):
            print("jup")
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
                ded = await client.fetch_user(vermoord)
                await main_channel.send(f"{ded.name} is opgehangen!")
                deathlist.append(vermoord)
                stemmen_done = True
                votes_dict = {}
                votes = []
                alGestemd = []
                meeste_stemmen = 0
                tie_list = []


async def monarchspeeches(p):
    global guild
    global potentiele_monarch
    global potentie
    global speech_done
    spechniklaar = True
    main_channel = discord.utils.get(p.guild.text_channels, name="main_channel")

    def check(m):
        return client.user != m.author \
               and m.guild == guild

    await main_channel.send(
        "Wie wil een poging wagen om Koning te worden? Geinteresseerden sturen \"ik eis de monarchie op\". "
        "als iedereen erin zit stuur: Genoeg!")
    while potentie:
        msg = await client.wait_for("message", check=check)
        msg.content = msg.content.lower()
        if msg.content.lower().startswith("ik eis de monarchie op"):
            if msg.author in potentiele_monarch:
                await main_channel.send("Je staat al op de lijst.")
            else:
                potentiele_monarch.append(msg.author.id)
                await main_channel.send(f"<@{msg.author.id}> heeft (zo te zien) Koningklijk Bloed!")
        if msg.content.lower().startswith("genoeg"):
            potentie = False
    await p.guild.create_voice_channel(name="speech_voice", reason="monarch speeches")
    await main_channel.send("Ga nu allemaal in de speech_voice channel en geef jullie speeches op deze volgorde:")
    for i in range(0, len(potentiele_monarch)):
        monchar = await client.fetch_user(potentiele_monarch[i])
        await main_channel.send(f"{i + 1}. {monchar.name}")
    await main_channel.send("Als de speeches klaar zijn stuur: \"klaar\"")
    while spechniklaar:
        msg = await client.wait_for("message", check=check)
        msg.content = msg.content.lower()
        if msg.content.startswith("klaar"):
            speech_done = True
            speech_voice = discord.utils.get(p.guild.voice_channels, name="speech_voice")
            await speech_voice.delete()
            spechniklaar = False


async def monarchvoting(k):
    global players
    main_channel = discord.utils.get(k.guild.text_channels, name="main_channel")
    playerIdList = list(players)
    global alGestemd
    global meeste_stemmen
    global tie_message
    global tie
    global tie_list
    global monarchvote
    global monarch_dict
    global monarch_message
    global monarch_done
    global alivePlayers
    global de_monarch
    global koning

    if not monarch_message:
        await main_channel.send("Stem nu allemaal op je favoriete koning. Doe dat met !naam")
        monarch_message = True

    def check(m):
        return client.user != k.author \
               and m.content.startswith("!") \
               and m.guild == guild

    msg = await client.wait_for("message", check=check)
    msg.content = msg.content.lower()
    if msg.channel == main_channel:
        if msg.author.name not in alGestemd:
            if msg.author.name.lower() in msg.content.lower():
                await main_channel.send(f"{msg.author.name} je kan niet op jezelf stemmen")
                return
            else:
                for i in range(0, len(playerIdList)):
                    z = await client.fetch_user(playerIdList[i])
                    if z.name.lower() in msg.content.lower():
                        monarchvote.append(playerIdList[i])
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
                    if koning is not None and koning not in tie_list:
                        tie_list.append(koning)
                    tie = True

                if monarch_dict[monark[i]] > meeste_stemmen:
                    if tie:
                        tie = False
                        tie_list = []
                    koning = monark[i]
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
                await main_channel.send("Stem opnieuw maar nu op dezelfde a.u.b.")
                monarch_dict = {}
                monarchvote = []
                alGestemd = []
                meeste_stemmen = 0
                tie_list = []
                tie_message = "Het is gelijkspel tussen"
            else:
                kronig = await client.fetch_user(koning)
                await main_channel.send(f"{kronig.name} is gekroond!")
                de_monarch = koning
                monarch_done = True
                monarch_dict = {}
                monarchvote = []
                alGestemd = []
                meeste_stemmen = 0
                tie_list = []


def reset_dones():
    global ziener_done
    global weerwolf_done
    global heks_done
    global stemmen_done
    global heksmessage
    global weerwolfmessage
    global zienermessage

    ziener_done = False
    weerwolf_done = False
    heks_done = False
    stemmen_done = False
    zienermessage = False
    heksmessage = False
    weerwolfmessage = False


async def avond(a):
    await create_channels(a)
    if not testing:
        await playerjoining(a)
    await permissies(a)
    await pre_game(a)


async def eerste_nacht(j):
    while not cupido_done:
        await cupido(j)


async def elke_nacht(k):
    global players
    global heksAlive
    global zienerAlive
    playerIdList = list(players)
    main_channel = discord.utils.get(k.guild.text_channels, name="main_channel")

    override = discord.PermissionOverwrite()
    override.send_messages = False
    for i in range(0, len(playerIdList)):
        member = await client.fetch_user(playerIdList[i])
        await main_channel.set_permissions(member, overwrite=override)

    if zienerAlive:
        while not ziener_done:
            await ziener(k)

    while not weerwolf_done:
        await weerwolf(k)

    if heksAlive:
        while not heks_done:
            await heks(k)


async def dag(r):
    global players
    playerIdList = list(players)
    main_channel = discord.utils.get(r.guild.text_channels, name="main_channel")

    override = discord.PermissionOverwrite()
    override.send_messages = True

    for i in range(0, len(playerIdList)):
        member = await client.fetch_user(playerIdList[i])
        await main_channel.set_permissions(member, overwrite=override)

    reset_dones()
    await dood(r)

    win_check()

    if not game_active:
        return

    while not stemmen_done:
        await stemmen(r)

    await dood(r)

    win_check()

    if not game_active:
        return

    while not speech_done:
        await monarchspeeches(r)

    while not monarch_done:
        await monarchvoting(r)

    win_check()

def win_check():
    global game_active
    global lovers
    global winnaars
    livingRoles = []

    for living in alivePlayers:
        if players[living] not in livingRoles:
            livingRoles.append(players[living])

    if "Weerwolf" not in livingRoles:
        game_active = False
        winnaars = "De Burgers"
        return

    if len(livingRoles) == 1 and livingRoles[0] == "Weerwolf":
        game_active = False
        winnaars = "De Weerwolven"
        return

    if len(alivePlayers) == 2:
        if alivePlayers[0] == lovers[0] or alivePlayers[0] == lovers[1]:
            if alivePlayers[1] == lovers[0] or alivePlayers[1] == lovers[1]:
                game_active = False
                winnaars = "De Geliefden"


async def permissies(r):
    override = discord.PermissionOverwrite()
    override.view_channel = True

    for e in players:
        if "Cupido" == players[e]:
            cupido_channel = discord.utils.get(r.guild.text_channels, name="cupido_channel")
            cupidor = await client.fetch_user(e)
            await cupido_channel.set_permissions(cupidor, overwrite=override)

        if "Weerwolf" == players[e]:
            weerwolf_channel = discord.utils.get(r.guild.text_channels, name="weerwolf_channel")
            weerwolfor = await client.fetch_user(e)
            await weerwolf_channel.set_permissions(weerwolfor, overwrite=override)

        if "Ziener" == players[e]:
            ziener_channel = discord.utils.get(r.guild.text_channels, name="ziener_channel")
            zieneror = await client.fetch_user(e)
            await ziener_channel.set_permissions(zieneror, overwrite=override)

        if "Heks" == players[e]:
            heks_channel = discord.utils.get(r.guild.text_channels, name="heks_channel")
            heksor = await client.fetch_user(e)
            await heks_channel.set_permissions(heksor, overwrite=override)

        if "Het Onschuldige Meisje" == players[e]:
            meisje_channel = discord.utils.get(r.guild.text_channels, name="meisje_channel")
            meisjor = await client.fetch_user(e)
            await meisje_channel.set_permissions(meisjor, overwrite=override)


client.run(TOKEN)
