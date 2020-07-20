import discord
import os
import pymongo
from pymongo import MongoClient
from discord.ext import commands
from discord.utils import get

MONGO_URL = f"{os.environ['MONGO_URL']}?retryWrites=false"
CLUSTER = MongoClient(MONGO_URL)
COLLECTIONS = CLUSTER.heroku_hxb4kvx2
server_preferences = {"_id": "server_preferences"}


def get_prefix(bot, ctx):
    if not ctx.guild:
        return commands.when_mentioned_or("$")(bot, ctx)

    guild_table = COLLECTIONS[f"{ctx.guild.id}"]
    server_preferences_table = guild_table.find(server_preferences)
    for pre in server_preferences_table:
        prefix = pre["prefix"]
        
    return commands.when_mentioned_or(prefix)(bot, ctx)


TOKEN = os.environ['DISCORD_TOKEN']

bot = commands.Bot(command_prefix = get_prefix)
bot.remove_command("help")
        
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name="$help", type=2))
    print("Bot running")

@bot.command()
@commands.is_owner()
async def prefix(ctx, *, prefix):
    guild_table = COLLECTIONS[f"{ctx.guild.id}"]
    server_preferences_table = guild_table.find(server_preferences)
    guild_table.update_one(server_preferences, {"$set":{"prefix": prefix}}, upsert =True)
    await ctx.channel.send(f"The prefix has been changend for `{prefix}` type `{prefix}help` to see all commands")

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