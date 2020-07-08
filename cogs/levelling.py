import discord
import asyncio
import pymongo
import os
from pymongo import MongoClient
from discord.ext import commands
from discord.utils import get

mongourl = os.environ['MONGO_URL']

class Levelling(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        print("message was sent")
        mongo_url = mongourl
        cluster = MongoClient(mongo_url)
        db = cluster["heroku_hxb4kvx2"]
        colletion = db["level"]
        author_id = ctx.author.id
        guild_id = ctx.guild.id
        user_id = {"_id": author_id}

        if ctx.author == self.bot.user:
            return
        
        if ctx.author.bot:
            return

        if(colletion.count_documents({}) == 0):
            user_info = {"_id": author_id,"GuildID": guild_id, "Level": 1, "Xp": 0}
            colletion.insert_one(user_info)

        exp = colletion.find(user_id)
        for xp in exp:
            cur_xp = xp["Xp"]

            new_xp = cur_xp + 1

        colletion.update_one({"_id": author_id}, {"$set":{"Xp": new_xp}}, upsert=True)   

        level = colletion.find(user_id)
        for lvl in level:
            level_start = lvl["Level"]

            new_level = level_start + 1
        
        if cur_xp >= round(5 * (level_start ** 4 / 5)):
            colletion.update_one({"_id": author_id}, {"$set":{"Level": new_level}}, upsert =True)
            await ctx.channel.send(f"{ctx.author.mention} has leveled up to {new_level}")


def setup(bot):
    bot.add_cog(Levelling(bot))