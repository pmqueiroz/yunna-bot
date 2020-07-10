import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Comands
    @commands.command(pass_context=True, aliases=("commands", "cmd"))
    async def help(self, ctx):
        embed = discord.Embed(title="There are all commands I know", description="Yunna is a multi-purpose bot made as a test from an amateur that ended up becoming what we hope that you think as a great bot that now lies in your discord server. Please enjoy, and report to us any mistakes that you may encounter.", color=0xff4c5c)
        embed.set_author(name="Hey there", icon_url="https://user-images.githubusercontent.com/54639269/71168042-aa5bad00-2234-11ea-875f-5745cba18f6a.png")
        embed.set_image(url="https://user-images.githubusercontent.com/54639269/71168042-aa5bad00-2234-11ea-875f-5745cba18f6a.png")
        embed.add_field(name="General", value="`say`, `info`, `help`, `avatar`, `creator`, `author`, `commands`", inline=False)
        embed.add_field(name="Useful", value="`bitcoin`", inline=False)
        embed.add_field(name="Moderator", value="`prune`, `clear`, `purge`, `kick`, `ban`, `unban`", inline=False)
        embed.set_footer(text="use prefix '$' to this commands")
        await ctx.channel.send(content=None, embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
