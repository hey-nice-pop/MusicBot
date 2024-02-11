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

# 音楽を再生するコマンド
@bot.command()
async def play(ctx, url):
    if ctx.voice_client is None:
        await ctx.send("Botがボイスチャンネルに接続していません。")
        return

    # Botがボイスチャンネルに接続していない場合、ユーザーがいるチャンネルに接続
    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()
    else:
        # Botが既に接続している場合は、現在の再生を停止
        ctx.voice_client.stop()

    YDL_OPTIONS = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'opus',
            'preferredquality': '192',
        }],
        'noplaylist': True,
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            url2 = info['url']  # yt-dlpでは直接urlキーにアクセスできます
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            ctx.voice_client.play(source)
            await ctx.send(f'**Now Playing:** {info["title"]}')
        except Exception as e:
            await ctx.send(f'エラーが発生しました: {e}')

bot.run(YOUR_BOT_TOKEN)
