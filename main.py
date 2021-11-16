import os

import discord
import random
from discord.utils import get
from dotenv import load_dotenv
from discord.ext import commands
import botReplies as br
import asyncio
import soundEffects as se

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_NOAH_GUILD')

bot = commands.Bot(command_prefix='!snorlax ')

@bot.event
async def on_ready():
    print(f'{bot.user.name} is online.')
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
        print(f'{bot.user.name} is connected to {guild.name}. Guild id: {guild.id}')

@bot.command(name='start', help='Starts yawning.')
async def startCommand(ctx):
    user = ctx.message.author
    if ctx == bot.user.name:
        return
    voice_channel = ''
    if (getattr(user.voice, "channel")) is None:
        await ctx.channel.send(br.RESPONSES['noVoiceChannel'])
    else :
        voice_channel = discord.utils.get(ctx.guild.voice_channels, name=user.voice.channel.name)
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        
    channel = None
    done = False
    while not done:
        if voice_channel is not None:
            waitTime = random.randint(1, 10)
            
            channel = voice_channel.name

            await ctx.channel.send(br.RESPONSES['joiningChannel'])

            vc = await voice_channel.connect()
            yawnEffect = random.choice(se.EFFECTS)
            vc.play(discord.FFmpegPCMAudio(yawnEffect))
            # player = vc.create_ffmpeg_player('./audio/Yawn_Sound_Effects_1.mp3')
            # player.start()
            # while not player.player_is_done():
            #     await asyncio.sleep(1)
            await asyncio.sleep(9)
            print('done playing')

            # player.stop()
            await vc.disconnect()
            print('waiting for {time} minutes'.format(time=int(waitTime)))
            await asyncio.sleep(waitTime * 60)
        else :
            await ctx.channel.send(br.RESPONSES['userNotInChannel'])

bot.run(TOKEN)