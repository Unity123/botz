import dbl
import discord
from discord.ext import commands
import time as tim
import urllib
import os
import praw
import youtube_dl
from PyDictionary import PyDictionary
from gfycat.client import GfycatClient
import random
import asyncio

scounter = 1
dictionary = PyDictionary()
reddit = praw.Reddit(client_id="SgpnTCwJm3Hgag", client_secret="insert", user_agent="discord.bot.botz:v1.0.0 by DimBulb567")
gfycat = GfycatClient("2_cRBLwz", "insert")
bot = commands.Bot(command_prefix="b!")
submissions = []
chatpeeps = []
chatchannels = []
ischatting = False
msg = ""
newmsg = False

ydl_opts = {
    'format': 'bestaudio/best',
    'default_search': 'auto',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
    'prefer_ffmpeg': True,
    'outtmpl': '.\\music.mp4'
}

class TopGG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.token = "insert"
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True, webhook_path = "/", webhook_auth="spooksam", webhook_port=5000)
    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        if data["isWeekend"]:
            data["user"].send("All right! You voted for Botz during a weekend! Hooray!")
        else:
            data["user"].send("Cool. You voted for Botz. Remember to vote again!")
@bot.command(brief="About Botz", description="A brief description of Botz.")
async def about(ctx):
    await ctx.send("I am Botz.py, Botz rewritten using discord.py. I am your Discord butler. I can do many things, so just ask!\nVote for me here:\nhttps://top.gg/bot/594575656457601035/vote")
    return
@bot.command(brief="Reports the time", description="Reports the time. Takes a timezone to get the time from, if you enter nothing it will do GMT.")
async def time(ctx, timezone=""):
    if timezone.lower() == "ast" or timezone.lower() == "edt":
        await ctx.send(tim.strftime("%H:%M:%S", tim.gmtime(tim.time() - (3600*4))) + " AST & EDT")
        return
    if timezone.lower() == "est" or timezone.lower() == "cdt":
        await ctx.send(tim.strftime("%H:%M:%S", tim.gmtime(tim.time() - (3600*5))) + " EST & CDT")
        return
    if timezone.lower() == "cst" or timezone.lower() == "mdt":
        await ctx.send(tim.strftime("%H:%M:%S", tim.gmtime(tim.time() - (3600*6))) + " CST & MDT")
        return
    if timezone.lower() == "mst" or timezone.lower() == "pdt":
        await ctx.send(tim.strftime("%H:%M:%S", tim.gmtime(tim.time() - (3600*7))) + " MST & PDT")
        return
    if timezone.lower() == "pst" or timezone.lower() == "akdt":
        await ctx.send(tim.strftime("%H:%M:%S", tim.gmtime(tim.time() - (3600*8))) + " PST & AKDT")
        return
    if timezone.lower() == "akst" or timezone.lower() == "hadt":
        await ctx.send(tim.strftime("%H:%M:%S", tim.gmtime(tim.time() - (3600*9))) + " AKST & HADT")
        return
    if timezone.lower() == "hst" or timezone.lower() == "hast" or timezone.lower() == "sdt":
        await ctx.send(tim.strftime("%H:%M:%S", tim.gmtime(tim.time() - (3600*10))) + " HST & HAST & SDT")
        return
    if timezone.lower() == "sst":
        await ctx.send(tim.strftime("%H:%M:%S", tim.gmtime(tim.time() - (3600*11))) + " SST")
        return
    if timezone.lower() == "chst":
        await ctx.send(tim.strftime("%H:%M:%S", tim.gmtime(tim.time() + (3600*10))) + " CHST")
        return
    await ctx.send(tim.strftime("%H:%M:%S", tim.gmtime()) + " GMT")
    return
@bot.command(brief="Plays some lovely music", description="Plays a song in MP3 format. Just look up free MP3s.")
async def music(ctx, song, fmt):
    global scounter
    channel = ctx.author.voice.channel
    context = await channel.connect()
    if fmt == "mp3":
        urllib.request.urlretrieve(song, ".\\music" + str(scounter) + ".mp3")
    elif fmt == "yt":
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([song])
            try:
                os.rename(".\\music.mp3", ".\\music" + str(scounter) + ".mp3")
            except:
                purgecache(ctx=ctx)
    await ctx.send("b!leave to leave")
    context.play(discord.FFmpegPCMAudio(".\\music" + str(scounter) + ".mp3", executable="ffmpeg.exe"))
    scounter = scounter + 1
@bot.command(brief="Leaves a voice channel", description="Leaves a voice channel.")
async def leave(ctx):
    channel = ctx.author.voice.channel
    await ctx.voice_client.disconnect()
@bot.command(brief="Purges the MP3 cache", description="In order to play MP3 files, Botz must download them. But the computer it is running on has limited space, so you must run this command ever so often to clear up space")
async def purgecache(ctx):
    files = os.listdir(".\\")
    filtered = [file for file in files if file.endswith(".mp3")]
    for file in filtered:
        path = os.path.join(".\\",file)
        os.remove(path)
    await ctx.send("Cache purged")
@bot.command(brief="Gets the top posts from a subreddit", description="Gets the top posts from a subreddit. Can use still images and gifs, videos you have to click on the link at the top.")
async def topposts(ctx, subreddit, limit=10):
    i = 1
    cur = 0
    lmt = int(limit)
    sr = reddit.subreddit(subreddit)
    embeds = []
    for submission in sr.top(limit=int(limit)):
        if submission.over_18 == False:
            embed = discord.Embed(title="Top " + str(limit) + " posts from r/" + subreddit + ":", description=str(i) + ".", url=submission.url)
            embed.add_field(name=submission.title, value="https://www.reddit.com" + submission.permalink)
            newurl = ""
            if (submission.url.find("https://gfycat.com/") != -1):
                urll = submission.url.replace("https://gfycat.com/", "")
                newurl = gfycat.query_gfy(urll)["gfyItem"]["max5mbGif"]
            elif submission.url.find("v.redd.it") != -1:
                newurl = "https://image.freepik.com/free-icon/rounded-play-button_318-9366.jpg"
            else:
                newurl = submission.url
            embed.set_image(url=newurl)
            embeds.append(embed)
            i = i + 1
        else:
            lmt-=1
    message=await ctx.send(embed=embeds[cur])
    await message.add_reaction("\u25c0")
    await message.add_reaction("\u25b6")
    def check(reaction, user):
        return user != message.author
    emoji=""
    while True:
        if emoji == "\u25c0":
            if cur > 0:
                cur-=1
                await message.edit(embed=embeds[cur])
        if emoji == "\u25b6":
            if cur < lmt - 1:
                cur+=1
                await message.edit(embed=embeds[cur])
        try:
            reaction, user=await bot.wait_for("reaction_add",timeout=50000000,check=check)
        except:
            break
        emoji=str(reaction.emoji)
        await message.remove_reaction(reaction.emoji,user)
    await message.clear_reactions()
@bot.command(brief="Gets a word from the dictionary", description="Gets the word given from the dictionary.")
async def dict(ctx, word):
    df = dictionary.meaning(word)
    embed = discord.Embed(title=word)
    pos = ""
    defs = ""
    for key in iter(df):
        pos = key + ":"
        j = 1
        for mean in iter(df[key]):
            defs = defs + str(j) + ". " + mean + "\n"
            j = j + 1
        embed.add_field(name=pos, value=defs)
        defs=""
    await ctx.send(embed=embed)
@bot.command(brief="Commences a battle between two users", description="Commences a battle between the two users mentioned.")
async def battle(ctx, user1: discord.Member, user2: discord.Member):
    embed = discord.Embed(title="Battle", description=user1.name + " vs. " + user2.name)
    message = await ctx.send(embed=embed)
    hasWon = False
    curturn = user1
    curoff = user2
    curhp = 100
    offhp = 100
    limit = 0
    while True:
        await asyncio.sleep(2)
        rand = random.randint(1, 10)
        offhp -= rand
        embed.add_field(name=curturn.name + "'s attack!", value="\u2694"+curturn.name + " deals " + str(rand) + " damage\n" + curoff.name + " has " + str(offhp) + " health left!")
        if (offhp <= 0):
            break
        limit += 1
        if limit == 5:
            embed.remove_field(0)
            limit -= 1
        temp = curturn
        curturn = curoff
        curoff = temp
        temp2 = curhp
        curhp = offhp
        offhp = temp2
        await message.edit(embed=embed)
    embed.add_field(name="Winner", value=curturn.name + " has won!")
    await message.edit(embed=embed)
@bot.command(brief="Tells someone GG", description="DMs someone a non-anonymous GG message.")
async def gg(ctx, user: discord.Member):
    await user.send("GG from " + ctx.author.name + "!")
@bot.command(brief="Makes a gluesnifer", description="Makes a gluesnifer. Not much else.")
async def snifer(ctx):
    ch = await ctx.guild.create_text_channel("gluesnifing")
    f=open(".\\gluesnife.png", "rb")
    nm=f.read()
    f.close()
    emoji = await ctx.guild.create_custom_emoji(name="gluesnifer", image=nm)
    msg = await ch.send(content=emoji)
    await msg.add_reaction(emoji)
    await ctx.send("Glue has been snifed")
@bot.command(brief="Creates some teams", description="Creates some teams and randomly assigns people to them.")
async def teams(ctx, role1, role2):
    team1 = await ctx.guild.create_role(name=role1)
    team2 = await ctx.guild.create_role(name=role2)
    ow1 = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        team1: discord.PermissionOverwrite(read_messages=True)
    }
    ch1 = await ctx.guild.create_text_channel(role1, overwrites=ow1)
    ow2 = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        team2: discord.PermissionOverwrite(read_messages=True)
    }
    ch2 = await ctx.guild.create_text_channel(role2, overwrites=ow2)
    for member in ctx.guild.members:
        if random.randint(0, 1) == 0:
            await member.add_roles(team1)
        else:
            await member.add_roles(team2)
    await ctx.send("Teams setup")
@bot.command(brief="Shows servers bot is in", description="Shows what servers Botz is in. Owner only.")
@commands.is_owner()
async def servers(ctx):
    servers = list(bot.guilds)
    await ctx.author.send("\n".join(server.name for server in servers))
#@bot.command(brief="Tells everyone in every server the bot is in a message", description="Sends a message to a random text channel in each server Botz is in. Owner only.")
#@commands.is_owner()
#async def masssend(ctx, message):
#    servers = list(bot.guilds)
#    for server in servers:
#        for channel in server.channels:
#            try:
#                await channel.send(message)
#            except Exception:
#                continue
#            else:
#                break
@bot.command(brief="Chats with some peeps", description="Chats with random people who use Botz")
async def chat(ctx):
    chatpeeps.append(ctx.author)
    peep = random.choice(chatpeeps)
    await ctx.send("Waiting for a chat...")
    while True:
        if peep == ctx.author or peep == None:
            peep = random.choice(chatpeeps)
            continue
        break
    servers = list(bot.guilds)
    channel = None
    for server in servers:
        if peep in server.members:
            for ch in server.channels:
                try:
                    await ch.send(f"{peep.mention}, you are connected with {ctx.author.name}!")
                except Exception:
                    continue
                else:
                    channel = ch
                    break
            break
    await ctx.send(f"{ctx.author.mention}, you are connected with {peep.name}!")
    msg = None
    while True:
        try:
            msg = await bot.wait_for("on_message", check=lambda m: m.author == peep and m.channel == ch, timeout=60.0)
        except asyncio.TimeoutError:
            break
        else:
            ctx.send(msg.content)
async def checkmsg(msg, user):
    return msg.author == user
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="people misusing my bot, do b!help please"))
    
bot.run("insert")
