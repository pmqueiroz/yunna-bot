import discord
import os
import pymongo
from pymongo import MongoClient
from discord.ext import commands
from discord.utils import get

TOKEN = os.environ['DISCORD_TOKEN']
MONGO_URL = f"{os.environ['MONGO_URL']}?retryWrites=false"
CLUSTER = MongoClient(MONGO_URL)
COLLECTIONS = CLUSTER.heroku_hxb4kvx2

bot = commands.Bot(command_prefix='$')
bot.remove_command("help")
        
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name="$help", type=2))
    print("Bot running")

@bot.command()
async def log(ctx):
        tab_id = ctx.guild.id
        guild_table_name = COLLECTIONS[f"{tab_id}"]
        guild_table_name.insert_one({"_id": ctx.author.id, "Level":0, "Xp": 0})
        sla = 1


    # messages = await ctx.channel.history(limit=5)
    # print(messages)

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')    

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

    
bot.run(TOKEN)