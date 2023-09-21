import discord
import youtube_dl
import asyncio
from discord.ext import commands, tasks
from fonctionArchivage import *
from fonctionsMusic import *
from random import randrange

bot = commands.Bot(command_prefix="/")

#définition d'un mot de passe
alphabet = "abcdefghijklmnopqrstuvwxyz"
mdp = ""
nmbreCarac = randrange(5,12)*"a"
for carac in nmbreCarac:
    aleat = randrange(0,26)
    mdp += alphabet[aleat]
    
musics = {}

ytdl = youtube_dl.YoutubeDL()

class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video["formats"] [0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]
        
def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url
                                                                , before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))
    def next(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=next)
       
@bot.command()
async def play(ctx, url):
    print("play ok")
    client = ctx.guild.voice_client
    
    verifMusic = []
    lister("musics.txt", verifMusic)
    
    if url not in verifMusic:
        archiverMusic("musics.txt", url)
    
    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        channelVocal = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channelVocal.connect()
        await ctx.send(f"Lancement de : {video.url}")
        play_song(client, musics[ctx.guild], video)
        
@bot.command()
async def skip(ctx):
    client = ctx.guild.voice_client
    client.stop()

@bot.command()
async def pause(ctx):
    client = ctx.guild.voice_client
    if not client.is_paused():
        client.pause()

@bot.command()
async def resume(ctx):
    client = ctx.guild.voice_client
    if client.is_paused():
        client.resume()

@bot.command()
async def leave(ctx):
    client = ctx.guild.voice_client
    await client.disconnect()
    musics[ctx.guild] = []

@bot.event
async def on_ready():
    print(f"Yeet @everyone \n MDP : {mdp}")
    
    await bot.change_presence(activity = discord.Game("prendre le thé avec créateur-senpai"))
    
    
    readyMessageRoom = [749988628792344626] #bot-ready (HC), bot-Ready(alt-f4)
    for element in readyMessageRoom:
        channel = bot.get_channel(element)
        notifOnready = await channel.send("""@here, je suis en ligne ! Demandez moi tout ce que vous voulez !
    (Ce message est automatique, ajoutez une réaction si ça vous emmerde )""")
        await notifOnready.add_reaction("❌")

@bot.event
async def on_guild_join(guild):
    guildJoin = bot.get_channel(750295254321856532) #serveurs-rejoint
    await guildJoin.send(f"J'ai rejoint **{guild}**, **{guild.id}**")

@bot.command()
async def botinfo(ctx):
    #Liste des commandes du bot
    
    musicInfo = "Voir la liste des commandes permettant de jouer de la musique"
    salut = "Dire bonjour à tout le monde"
    trad = "Converti le message suivant la commande en caractères ASCII (!!Ne pas utiliser de majuscules!!)"
    suggest = "Suggérer une commande à ajouter au bot (exemple : /suggest une idée)"
    dm = "Envoyer un message privé à un utilisateur"
    talk = "Discuter avec le bot (Peut prendre plus ou moins de temps à répondre) (exemple : /talk Bonjour)"
    botinfo = "Afficher la liste des commandes"
    serverinfo = "Afficher les informations du serveur (liste non exhaustive)"
    shutdown = "Eteindre le bot (nécessite un mot de passe)"
    clear = "Effacer les messages qui précedent la commande (nécessite des droits admin) (exemple : /clear 3)"
    getmdp = "Obtenir le mot de passe du bot en message privé (Commande reservée à RƐi-san)"
    ans = " Répondre à /talk (Reservé à certains utilisateur sur certains serveurs)"
    aide = "Pour toute questions ou problèmes, contacter RƐi-san#1192"
    print(f"botinfo by {ctx.author}")
    botinfoEmbed = discord.Embed(title = "Botinfo", description = "Liste des commandes", color = 0x46dd0a)
    botinfoEmbed.set_thumbnail(url = "https://img1.picmix.com/output/stamp/normal/0/6/3/9/1249360_3666b.gif")
    botinfoEmbed.add_field(name = "/musicinfo", value = musicInfo, inline= True )
    botinfoEmbed.add_field(name = "/salut", value = salut, inline= True )
    botinfoEmbed.add_field(name = "/trad", value = trad, inline= True )
    botinfoEmbed.add_field(name = "/suggest", value = suggest, inline= True )
    botinfoEmbed.add_field(name = "/talk", value = talk, inline= True )
    botinfoEmbed.add_field(name = "/botinfo", value = botinfo, inline= True )
    botinfoEmbed.add_field(name = "/serverinfo", value = serverinfo, inline= True )
    botinfoEmbed.add_field(name = "/shutdown", value = shutdown, inline= True )
    botinfoEmbed.add_field(name = "/clear", value = clear, inline= True )
    botinfoEmbed.add_field(name = "/getmdp", value = getmdp, inline= True )
    botinfoEmbed.add_field(name = "/ans", value = ans, inline= True )
    botinfoEmbed.add_field(name = "/dm", value = dm, inline= True )
    botinfoEmbed.add_field(name = "aide", value = aide, inline= True)
    botinfoEmbed.set_footer(text = "Wow, t'as vraiment tout lu ? :D")
    await ctx.send(embed=botinfoEmbed)

@bot.command()
async def musicinfo(ctx):
    print(f"musicinfo by {ctx.author}")
    play = "Jouer une musique (Nécessite d'être dans une channel vocal avant de lancer la musique)(exemple : /play https://www.youtube.com/watch?v=tz82xbLvK_k)"
    pause = "Mettre la musique en pause"
    resume = "Reprendre la lecture"
    skip = "Passer à la musique suivante (si il y en une dans la file d'écoute, sinon arret du bot)"
    leave = "Déconnecter le bot du channel vocal"
    ajout = "[CECI N'EST PAS UNE COMMANDE] Pour ajouter un titre à la liste de lecture, retaper /play"
    musicinfoEmbed = discord.Embed(title = "Musicinfo", description = "Liste des commandes musicales", color = 0x1abab2)
    musicinfoEmbed.set_thumbnail(url = "https://i.pinimg.com/originals/9e/03/a6/9e03a65f07f0efdebbe291fccd718f4d.gif")
    musicinfoEmbed.add_field(name = "/play", value = play, inline = True)
    musicinfoEmbed.add_field(name = "/pause", value = pause, inline = True)
    musicinfoEmbed.add_field(name = "/resume", value = resume, inline = True)
    musicinfoEmbed.add_field(name = "/skip", value = skip, inline = True)
    musicinfoEmbed.add_field(name = "/leave", value = leave,inline = True)
    musicinfoEmbed.add_field(name = "ajout", value = ajout, inline = True )
    await ctx.send(embed=musicinfoEmbed)
    
    

@bot.command()
async def serverinfo(ctx):
    #Info du serveur courant
    
    print(f"serverinfo by {ctx.author} for {ctx.guild.name}")
    server = ctx.guild
    serverName = server.name
    numberTextChannel = len(server.text_channels)
    numberVoiceChannel = len(server.voice_channels)
    numberPersonne = server.member_count
    message = f"{serverName} posséde : \n {numberTextChannel} salons textuels \n {numberVoiceChannel} salons vocaux \n {numberPersonne} membres"
   
@bot.command()
async def getmdp(ctx):
    #Envoie le mot de passe généré
    
    print(f"getmdp by {ctx.author}")
    if ctx.author.id == 310773647985868800:
        await ctx.author.send(mdp)
        listMessage = await ctx.channel.history(limit = 1).flatten()
        for message in listMessage:
            await message.delete()
    else:
        print(f"getmdp by {ctx.author.id}")
        await ctx.send("action refusée.")   
 
@bot.command()
async def talk(ctx, *texte):
    #Parler avec le bot
    
    expediteur = ctx.author
    serveurExpediteur = ctx.guild.name
    roomExpediteurID = ctx.channel.id
    roomExpediteurName = ctx.channel.name
    identifiantRoom = f"{roomExpediteurID} {serveurExpediteur}/{roomExpediteurName}"
    
    #envoyé dans messages
    messageChannel = bot.get_channel(749024840811413587)
    message = " ".join(texte)
    await messageChannel.send(f"***{expediteur}*** from ***{serveurExpediteur}*** dit : {message}")
    
    #envoyé dans id-room
    idRoom = bot.get_channel(749279849906176142)
    message = await idRoom.send(f"{roomExpediteurID} by {expediteur} from **{roomExpediteurName}** in **{serveurExpediteur}**")
    archiver("channelsID.txt", identifiantRoom)
    
    #mettre à jour rappel-ans
    rappelAnsChannel = bot.get_channel(749429666594422814)
    listMessage = await rappelAnsChannel.history(limit = 1).flatten()
    for message in listMessage:
        await message.delete()
    await rappelAnsChannel.send(recupChannelsID())

@bot.command() 
async def ans(ctx, nbre:int, *texte):
    #répondre à /talk
    
    #récuperation des id dans une liste pour orienter le message avec le paramètre "nbre"
    listage = []                                # |
    listage = lister("channelsID.txt", listage) # | récupération du texte dans channelsID.txt
    roomActive = []
    indexRoomActive = ""
    
    #ajout des id uniquement dans roomActive
    for element in listage:
        for i, carac in enumerate(element):
            if i <= 18:
                indexRoomActive += carac
        roomActive.append(indexRoomActive)
        indexRoomActive = ""

    #renvoyer un message
    userAutorise = [310773647985868800, 334413361682972674] #R3i-san, Imperial
    serverAutorise = [749024840362623046] #Yeet's dms
    if (ctx.author.id in userAutorise) and (ctx.guild.id in serverAutorise) : 
        channel = bot.get_channel(int(roomActive[nbre - 1]))
        message = " ".join(texte)
        await channel.send(message)
    else : 
        await ctx.send("Action refusée.")

@bot.command()
async def salut(ctx):
    #Dire bonjour à tout le monde
    print(f"salut by {ctx.author}")
    await ctx.send("@everyone Salut bande de sacs à mer... merveilles")
    
@bot.command()
async def suggest(ctx, *texte):
    #Suggérer une idée dans le salon "suggest"
    print(f"suggest by {ctx.author}")
    expediteur = ctx.author.name
    serveurExpediteur = ctx.guild.name
    channel = bot.get_channel(749281156222156880) #salon suggest
    message = " ".join(texte)
    await channel.send(f"***{expediteur}*** from ***{serveurExpediteur}*** dit : {message}")
    await ctx.send("Suggestion envoyée ! Merci d'aider créateur-senpai à me développer !")
        
@bot.command()
async def trad(ctx, *texte):
    print(f"trad by {ctx.author}")
    carac = "丹书ㄈ力已下呂廾工丿片乚爪ㄇ口尸厶尺ㄎ丁凵人山父了乙"
    message = []
    for mot in texte:
        for caractere in mot:
            if caractere.isalpha():
                index = ord(caractere) - ord("a")
                traduc = carac[index]
                message.append(traduc)
            else:
                message.append(caractere)
        message.append(" ")
    await ctx.send("".join(message))
  
@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, nbre : int):
    print(f"clear by {ctx.author}")
    listMessage = await ctx.channel.history(limit = nbre + 1).flatten()
    for message in listMessage:
        await message.delete()

@bot.command()
async def shutdown(ctx, message):
    print(f"shutdown by {ctx.author}")
    if message == mdp:
        await ctx.send("@everyone A plus ! Je m'éteins.")
        exit()
    else: 
        await ctx.send("Action refusée.")
        
@bot.command()
async def dm(ctx, user:discord.User, *texte):
    message = " ".join(texte)
    await user.send(message)
   
bot.run("API KEY")