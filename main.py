import discord
import os
import pymongo
from pymongo import MongoClient
from discord.ext import commands
from discord.utils import get

token = os.environ['DISCORD_TOKEN']
mongourl = os.environ['MONGO_URL']

bot = commands.Bot(command_prefix='$')
bot.remove_command("help")
        
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name="$help", type=2))
    print("Bot running")

@bot.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.message.add_reaction('\U0001F44C')

@bot.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await ctx.message.add_reaction('\U0001F44B')
        await voice.disconnect()
    else:
        await ctx.send("Im not connected")

@bot.command()
async def secret(ctx):
    mongo_url = f"{mongourl}?retryWrites=false"
    cluster = MongoClient(mongo_url)
    db = cluster["heroku_hxb4kvx2"]
    colletion = db["new"]
    ping_cm = {"command":1}
    colletion.insert_one(ping_cm)

    await ctx.channel.send("you find the secret command")

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')    

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

    
bot.run(token)