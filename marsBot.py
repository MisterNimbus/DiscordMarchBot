import discord
from discord.ext import commands
from discord.utils import get
import os

bot = commands.Bot(command_prefix='!')

sound_folder = './tracks/'  # change this to the folder where your soundtracks are stored

@bot.event
async def on_ready():
    print('Bot is online!')

@bot.command(name='list')
async def list_soundtracks(ctx):
    soundtracks = [f for f in os.listdir(sound_folder) if os.path.isfile(os.path.join(sound_folder, f)) and f.endswith('.mp3')]
    msg = "Available soundtracks:\n"
    for i, s in enumerate(soundtracks):
        msg += f"{i+1}. {s}\n"
    await ctx.send(msg)

@bot.command(name='play')
async def play_soundtrack(ctx, number: int):
    soundtracks = [f for f in os.listdir(sound_folder) if os.path.isfile(os.path.join(sound_folder, f)) and f.endswith('.mp3')]

    if number < 1 or number > len(soundtracks):
        await ctx.send('Invalid track number!')
        return

    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.send("You need to join a voice channel first!")
        return

    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client is None:
        voice_client = await voice_channel.connect()
    elif voice_client.is_playing():
        voice_client.stop()
    else:
        await voice_client.move_to(voice_channel)

    soundtrack = soundtracks[number - 1]
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(os.path.join(sound_folder, soundtrack)))
    voice_client.play(source, after=lambda e: print(f"Finished playing {soundtrack}"))
    await ctx.send(f"Now playing: {soundtrack}")

bot.run('MTEwNzI2ODQwNzg3NjkyMzUxNA.G755E1.okpFwhHUOneQ1e8H3nk0Qfa-ST3Tp7VwxqhnIA')
