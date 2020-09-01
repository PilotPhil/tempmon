import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='assets/discord.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

@bot.command(name='temp', help='retrieve current temp from TempMon')
async def send_current_temp(ctx, *args):
    await ctx.send("We'll get there, too.")
    await ctx.send(f"For now, here's your args: {args}")

@bot.command(name='make-channel', help='Makes a new channel. Usage: !make-channel <channel-name>')
@commands.has_role('admin')
async def create_channel(ctx, channel_name='oh, default.'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        await ctx.send("I'll make that right away!")
        await guild.create_text_channel(channel_name)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

# @bot.event
# async def on_message(message):
#     if message.author == client.user:
#         return
    
#     if message.content == '!get temp':
#         response = "We're getting there."
#         await message.channel.send(response)
#     elif message.content == 'raise-exception':
#         raise discord.DiscordException

# @bot.event
# async def on_error(event, *args, **kwargs):
#     with open('err.log', 'a') as f:
#         if event == 'on_message':
#             f.write(f'Unhandled message: {args[0]}\n')
#         else:
#             raise


bot.run(TOKEN)