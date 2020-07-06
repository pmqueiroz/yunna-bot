import discord
import asyncio
import random
import json
from discord.ext import commands

class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Running")

    # Comands
    @commands.command()
    async def sayd(self, ctx,*, arg):
        await ctx.channel.purge(limit=1)
        await ctx.send(arg)

    @commands.command()
    async def say(self, ctx,*, arg):
        await ctx.channel.purge(limit=1)
        await ctx.send(arg)

    @commands.command()
    async def hello(self, ctx):
        def openJson():
            with open("hello.json", "r") as f:
                lines = f.read()
                return lines

        hello_answers = openJson()
        answers = json.loads(hello_answers)
        answers
        hello = random.choice(answers['Hello'])
        hay = random.choice(answers['Hay'])
        await ctx.send(f"{hello} {ctx.author.mention} {hay}")

    @commands.command()
    async def info(self, ctx):
        await ctx.send("Yunna is a multi-purpose bot made as a test from an amateur that ended up becoming what we hope that you think as a great bot that now lies in your discord server. Please enjoy, and report to us any mistakes that you may encounter.")

    @commands.command(pass_context=True, aliases=('author', 'developer'))
    async def creator(self, ctx):
        author = ctx.message.author
        embed = discord.Embed(color=0x00ffff)
        embed.set_author(name="i just dont have what to do")
        embed.set_thumbnail(url='https://avatars0.githubusercontent.com/u/54639269?s=460&v=4')
        embed.add_field(name="What 'bout me :cowboy:", value="Just a guy bored w/ the web design class n' hated python but give it a try and dats what happened", inline=False)

        await ctx.channel.send(content="Thay's my creator", embed=embed)

    @commands.command(pass_context=True)
    async def avatar(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        embed=discord.Embed(title="Click on the picture to reveal bigger size", color=0xff4c5c)
        embed.set_author(name="I got the picture for you")
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)


    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
        embed.set_author(name=f"Level - {member}", icon_url=member.avatar_url)
        embed.add_field(name="Level", value="1")
        embed.add_field(name="Experience", value="0")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))
