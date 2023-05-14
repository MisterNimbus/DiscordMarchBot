import os
import discord
from discord.ext import commands
import asyncio
import yt_dlp as youtube_dl
import re

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

ytdl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ytdl = youtube_dl.YoutubeDL(ytdl_opts)

# initialize an empty list to hold the queued urls
queue = []


curr_channel = None
vc = None

def is_valid_audio_url(url):
    yt = re.compile(r'^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=))([\w\-]{11})(?:\S+)?$')
    return yt.match(url) is not None

@bot.command()
async def play(ctx, url):
    global curr_channel  
    global vc

    if not ctx.author.voice:
        await ctx.send(f'You are not in a voice Channel')
        return

    # join a channel or change the curr_channel
    if curr_channel != ctx.author.voice.channel:
        if curr_channel != None:
            await bot.get_command('leave')(ctx)

        # connect to the current voice channel
        curr_channel = ctx.author.voice.channel
        vc = await curr_channel.connect()
        await ctx.send(f'Joined to channel {curr_channel.name}')
    
    if not is_valid_audio_url(url=url):
        await ctx.send(f'This is not a valid url for me to use: {url}')
        return

    # check if the bot is already playing something
    if ctx.voice_client and ctx.voice_client.is_playing():
        # add the url to the queue and send a message to notify the user
        queue.append(url)
        with ytdl:
            info_dict = ytdl.extract_info(url, download=False)
        await ctx.send(f'Added {info_dict["title"]} to the queue.')
        return
    else:
        try:
            with ytdl:
                info_dict = ytdl.extract_info(url, download=False)
                audio_url = info_dict['url']

            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(audio_url))
            vc.play(source, after=lambda _: play_next(ctx))

            await ctx.send(f'Playing {info_dict["title"]}.')
        except Exception as e:
            await ctx.send(f'Anani sikim noluo lan: {str(e)}')

def play_next(ctx):
    # check if there are urls in the queue
    if queue:
        # get the next url and remove it from the queue
        url = queue.pop(0)

        try:
            with ytdl:
                info_dict = ytdl.extract_info(url, download=False)
                audio_url = info_dict['url']

            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(audio_url))
            ctx.voice_client.play(source, after=lambda _: play_next(ctx))

            # send a message to notify the user which song is playing
            asyncio.run_coroutine_threadsafe(ctx.send(f'Playing {info_dict["title"]} (from the queue)...'), bot.loop)
        except Exception as e:
            asyncio.run_coroutine_threadsafe(ctx.send(f'Lan noluo amk bisi oldu: {str(e)}'), bot.loop)


@bot.command(name='queue')
async def queue_(ctx):
    # check if there are urls in the queue
    if queue:
        # create a formatted string of the queued urls
        queue_str = '\n'.join([f'{i+1}. {url}' for i, url in enumerate(queue)])

        # send the queue to the user
        await ctx.send(f'Queue:\n{queue_str}')
    else:
        await ctx.send('The queue is empty.')

@bot.command(name='emptyq')
async def emptyq(ctx):
    queue.clear()
    await ctx.send('The queue is emptied.')

@bot.command(name='skip')
async def skip_(ctx):
    if ctx.voice_client:
        if queue:
            ctx.voice_client.stop()
            await ctx.send('Skipping the current audio...')
        else:
            await ctx.send('The queue is empty.')
    else:
        await ctx.send("I'm not in a voice channel.")


@bot.command(name='leave')
async def leave(ctx):
    try:
        # check if the bot is in a voice channel
        if not ctx.voice_client:
            await ctx.send("I'm not in a voice channel.")
            return

        ctx.voice_client.stop()
        queue.clear()
        # disconnect from the voice curr_channel
        await ctx.voice_client.disconnect()

        #clear channel variables
        global curr_channel, vc
        curr_channel = None
        vc = None

        await ctx.send("Leaving the channel")
    except Exception as e:
        await ctx.send(f'Anani emcükleyim bisi oldu herhalde amk: {str(e)}')


@bot.command(name='pause')
async def pause_(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send('Paused.')
    else:
        await ctx.send("I'm not currently playing anything.")

@bot.command(name='resume')
async def resume_(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send('Resumed.')
    else:
        await ctx.send("I'm not currently paused.")

@bot.command(name='stop')
async def stop(ctx):
    if ctx.voice_client:
        queue.clear()
        ctx.voice_client.stop()
        await ctx.send('Stopped audio and queue is cleared. Playing nothing')
    else:
        await ctx.send("I'm not in a voice channel.")

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord')
    channel = discord.utils.get(bot.get_all_channels(), name='bot')
    await channel.send('ASE! Celdum | Type !usage for the command hints')
   
@bot.command()
async def usage(ctx):
    response = ("Here are the available commands:\n\n"
                "!play [URL] - Play an audio track from the specified YouTube URL. Calling this while an audio is played adds the url to the queue\n"
                "!stop - Stop the current audio and play nothing (cleares also the queue).\n"
                "!queue - Display the current queue.\n"
                "!emptyq - Empties the queue.\n"
                "!skip  - Skip the current track and move to the next in the queue.\n"
                "!leave - Make the bot leave the voice channel it's currently in.\n"
                "!resume - Resume the current audio.\n"
                "!pause - Pause the current audio.\n"
                "!restart - Restart the bot.\n"
                "!usage - Display this message.\n"
                )
    await ctx.send(response)


@bot.command(name='restart')
async def restart_bot(ctx):
    await ctx.send('Restarting the bot...')
    os.system('source ./restart.sh')


# Run the bot
def getToken():
    with open("./token.txt", "r") as f:
        return f.read()


bot.run(getToken())
