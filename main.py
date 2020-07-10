import discord
import os
import pymongo
from pymongo import MongoClient
from discord.ext import commands
from discord.utils import get

token = os.environ['DISCORD_TOKEN']
mongourl = f"{os.environ['MONGO_URL']}?retryWrites=false"

bot = commands.Bot(command_prefix='$')
bot.remove_command("help")
        
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name="$help", type=2))
    print("Bot running")

@bot.command()
async def log(ctx):
    if not ctx.author.id == 361319158241165324:
        return

    users_in_purge = {}

    async for message in ctx.channel.history(limit = 100):
        user = f"{message.author.name}#{message.author.discriminator}"
        if not user in users_in_purge:
            users_in_purge[user] = 1
        else:
            users_in_purge[user] += 1

    print(users_in_purge)



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

    
bot.run(token)