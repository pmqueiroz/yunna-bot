import discord
import asyncio
import pymongo
import os
import random
from pymongo import MongoClient
from discord.ext import commands
from discord.utils import get

mongourl = f"{os.environ['MONGO_URL']}?retryWrites=false"
mongo_url = mongourl
cluster = MongoClient(mongo_url)
db = cluster["heroku_hxb4kvx2"]

class Levelling(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        colletion = db["level"]
        author_id = ctx.author.id
        guild_id = ctx.guild.id
        level_id = f"{ctx.author.id}&{ctx.guild.id}"
        xp_gain = random.randint(15, 25)
        user_id = {"_id": level_id}
        user_exist = False
        is_command = ctx.content.startswith("$")

        author = f"{ctx.author.name}#{ctx.author.discriminator}"
        async for message in ctx.channel.history(limit = 2):
            user = f"{message.author.name}#{message.author.discriminator}"

        if author == user:
            return

        if ctx.author == self.bot.user:
            return
        
        if ctx.author.bot:
            return

        if is_command:
            return

        dups = colletion.find(user_id)
        for x in dups:
            user_exist = True

        if not user_exist:
            user_info = {"_id": level_id,"Level": 0, "Xp": 0}
            colletion.insert_one(user_info)

        exp = colletion.find(user_id)
        for xp in exp:
            cur_xp = xp["Xp"]

        colletion.update_one({"_id": level_id}, {"$inc":{"Xp": xp_gain}}, upsert=True)   

        level = colletion.find(user_id)
        for lvl in level:
            level_status = lvl["Level"]

            new_level = level_status + 1

        if cur_xp >= round(5 / 6 * new_level * (2 * new_level * new_level + 27 * new_level + 91)):
            colletion.update_one({"_id": level_id}, {"$inc":{"Level": 1}}, upsert =True)
            await ctx.channel.send(f"{ctx.author.mention} advanced to level  {new_level}")

    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member

        colletion = db["level"]
        author_id = ctx.author.id
        guild_id = ctx.guild.id
        level_id = f"{ctx.author.id}&{ctx.guild.id}"
        user_id = {"_id": level_id}

        status = colletion.find(user_id)
        for stats in status:
            level_status = stats["Level"]
            new_level = level_status + 1
            xp_status = stats["Xp"]
        
        next_xp_level = round(5 / 6 * new_level * (2 * new_level * new_level + 27 * new_level + 91))

        embed = discord.Embed(color=member.color)
        embed.set_author(name=f"Level - {member}", icon_url=member.avatar_url)
        embed.add_field(name="Level", value=level_status)
        embed.add_field(name="Experience", value=f"{xp_status}/{next_xp_level}")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Levelling(bot))

