import discord
from discord.ext import commands
import yt_dlp
import config

YOUR_BOT_TOKEN = config.YOUR_BOT_TOKEN

# インテントを有効化
intents = discord.Intents.all()

# Botオブジェクトの生成
bot = commands.Bot(
    command_prefix='!', 
    intents=intents, 
    activity=discord.Game("外気浴")
)

@bot.event
async def on_ready():
    print(f'ログインしました。{bot.user.name}')

@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("ボイスチャンネルに接続していません。")
        return
    channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def play(ctx, url):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("ボイスチャンネルに接続していません。")
            return
    else:
        ctx.voice_client.stop()

    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format': 'bestaudio'}

    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        ctx.voice_client.play(source)

    await ctx.send(f'**Now Playing:** {url}')

bot.run(YOUR_BOT_TOKEN)
