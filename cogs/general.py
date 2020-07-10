import discord
import asyncio
import random
import json
import requests
from discord.ext import commands
from discord.utils import get

class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"{member} has joined in server")
        channel = get(member.guild.channels, name="general")
        await channel.send(f"{member.mention} has joined in server")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"{member} has left the server")
        channel = get(member.guild.channels, name="general")
        await channel.send(f"{member.mention} has left the server")

    # Comands
    @commands.command()
    async def sayd(self, ctx,*, arg):
        def is_author(ctx):
            return ctx.author
        await ctx.channel.purge(limit=1)
        await asyncio.sleep(5)
        await ctx.send(arg)

    @commands.command()
    async def say(self, ctx,*, arg):
        await ctx.send(arg)

    @commands.command()
    async def pin(self, ctx,*, arg):
        await ctx.message.add_reaction('\U0001F4CC')
        profile_url = ctx.author.avatar_url
        embed = discord.Embed(title=f"{ctx.message.content.replace('$pin', '')}", color=0xff4c5c)
        embed.set_author(name=f"{ctx.author.name} just pinned a message:", icon_url=profile_url)
        pin_message = await ctx.channel.send(embed=embed)
        await pin_message.pin()

        up_embed = discord.Embed(title=f"{ctx.message.content.replace('$pin', '')}", color=0xff4c5c)
        up_embed.set_author(name=f"{ctx.author.name} just pinned a message:", icon_url=profile_url)
        up_embed.set_footer(text=f"Use $unpin {pin_message.id} for unpin the message")
        await pin_message.edit(embed=up_embed)

    @commands.command()
    async def unpin(self, ctx,*, arg):
        message = await ctx.fetch_message(int(arg))
        await message.unpin()
        profile_url = ctx.author.avatar_url
        embed = discord.Embed(color=0xff4c5c)
        embed.set_author(name=f"{ctx.author.name} unpinned the message: {message.id}", icon_url=profile_url)
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def hello(self, ctx):
            
        hello_array = [
            "Hello,",
            "Hi,",
            "Hey,",
            "Hi there!",
            "Hey there!",
            "Hey man!",
            "Hey bro",
            "Hey dude!",
            "Hey buddy!",
            "Yo!",
            "Howdy!"
        ]

        hay_array = [
            "how are you?",
            "how are ya?",
            "how are things?",
            "how are things going?",
            "how's it going?",
            "what's going on?",
            "how have you been?",
            "what's up?",
            "sup?",
            "whazzup?",
            "what's happening?",
            "doing ok?"
        ]

        hello = random.choice(hello_array)
        hay = random.choice(hay_array)
        await ctx.send(f"{hello} {ctx.author.mention} {hay}")

    @commands.command(pass_context=True, aliases=('author', 'developer'))
    async def creator(self, ctx):
        embed = discord.Embed(color=0x00ffff)
        embed.set_author(name="i just dont have what to do")
        embed.set_thumbnail(url='https://avatars0.githubusercontent.com/u/54639269?s=460&v=4')
        embed.add_field(name="What 'bout me :cowboy:", value="Just a guy bored w/ the web design class n' hated python but give it a try and dats what happened", inline=False)

        await ctx.channel.send(content="Thay's my creator", embed=embed)

    @commands.command(pass_context=True)
    async def avatar(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        embed=discord.Embed(title=f"{member.name}#{member.discriminator}",color=0xff4c5c)
        embed.set_author(name="I got the picture for you")
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def bitcoin(self, ctx):
        url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
        price = requests.get(url)
        value = price.json()['bpi']['USD']['rate']
        await ctx.send(f"Bitcoin current price is: ${value}")
        reactions = ['\U0001F4B0', '\U0001F4B8', '\U0001F911']

        await ctx.message.add_reaction(random.choice(reactions))

    @commands.command() 
    async def info(self, ctx, *, member: discord.Member = None):
        member = ctx.author if not member else member
        date = member.joined_at.strftime("%A, %B %d %Y %H:%M")
        await ctx.channel.send(f"{member.mention} joined on {date} and has {len(member.roles)} roles.")

    @info.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.channel.send("I couldn't find that member")


def setup(bot):
    bot.add_cog(General(bot))
