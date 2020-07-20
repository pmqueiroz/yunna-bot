import discord
import os
import pymongo
from pymongo import MongoClient
from discord.ext import commands

MONGO_URL = f"{os.environ['MONGO_URL']}?retryWrites=false"
CLUSTER = MongoClient(MONGO_URL)
COLLECTIONS = CLUSTER.heroku_hxb4kvx2
server_preferences = {"_id": "server_preferences"}


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Comands
    @commands.command(pass_context=True)
    async def help(self, ctx):
        guild_table = COLLECTIONS[f"{ctx.guild.id}"]
        server_preferences_table = guild_table.find(server_preferences)
        for pre in server_preferences_table:
            prefix = pre["prefix"]
        embed = discord.Embed(title="There are all commands I know", description="Yunna is a multi-purpose bot made as a test from an amateur that ended up becoming what we hope that you think as a great bot that now lies in your discord server. Please enjoy, and report to us any mistakes that you may encounter.", color=0xff4c5c)
        embed.set_author(name="Hey there", icon_url="https://user-images.githubusercontent.com/54639269/71168042-aa5bad00-2234-11ea-875f-5745cba18f6a.png")
        embed.set_thumbnail(url="https://user-images.githubusercontent.com/54639269/71168042-aa5bad00-2234-11ea-875f-5745cba18f6a.png")
        embed.add_field(name="General", value="`say`, `sayd`, `info`, `help`, `avatar`, `hello`", inline=False)
        embed.add_field(name="Useful", value="`bitcoin`, `pin`, `unpin`, `level`, `rank`, `translate`", inline=False)
        embed.add_field(name="Moderator", value="`prune`, `kick`, `ban`, `unban`, `prefix`", inline=False)
        embed.add_field(name="Music", value="`join`, `leave`", inline=False)
        embed.set_footer(text=f"use prefix '{prefix}' to this commands")
        await ctx.channel.send(content=None, embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))