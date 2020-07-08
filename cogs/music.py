import discord
from discord.ext import commands
from discord.utils import get

class music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

""" @bot.command()
async def join(self, ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(self.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.message.add_reaction('\U0001F44C')

@bot.command()
async def leave(self, ctx):
    channel = ctx.message.author.voice.channel
    voice = get(self.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await ctx.message.add_reaction('\U0001F44B')
        await voice.disconnect()
    else:
        await ctx.send("Im not connected") """

def setup(bot):
    bot.add_cog(music(bot))
