import discord
from discord.ext import commands
from discord.utils import get
import os

# intent for discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def read_bot_token(file_path):
    with open(file_path, 'r') as f:
        bot_token = f.read().strip()
    return bot_token

bot_token = read_bot_token('./bot_token.txt')


# initialize an empty list to hold the queued urls
queue = []

# current sound channel
curr_channel = None

# voice client
vc = None

# where the soundtracks are
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


@bot.command(name='queue')
async def queue_(ctx):
    # check if there are marches in the queue
    if queue:
        # create a formatted string of the queued march names
        queue_str = '\n'.join([f'{i+1}. {name}' for i, name in enumerate(queue)])

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
            await ctx.send('Skipping the current track...')
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

print(bot_token)

bot.run(bot_token)
