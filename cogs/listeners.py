import discord
import pymongo
import os
from pymongo import MongoClient
from discord.ext import commands
from discord.utils import get

MONGO_URL = f"{os.environ['MONGO_URL']}?retryWrites=false"
CLUSTER = MongoClient(MONGO_URL)
COLLECTIONS = CLUSTER.heroku_hxb4kvx2

class listerners(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guild_table_name = COLLECTIONS[f"{guild.id}"]
        guild_table_name.insert_one({"_id": "server_preferences", "prefix": "$", "levelling_enable": False})

def setup(bot):
    bot.add_cog(listerners(bot))