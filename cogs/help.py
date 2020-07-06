import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Comands
    @commands.command(pass_context=True, aliases=("commands", "cmd"))
    async def help(self, ctx):
        author = ctx.message.author

        embed = discord.Embed(title="There are all commands I know", description="If you want more informations about a command click here (vai ter rlx)", color=0xff4c5c)
        embed.set_author(name="Hey there", icon_url="https://user-images.githubusercontent.com/54639269/71168042-aa5bad00-2234-11ea-875f-5745cba18f6a.png")
        embed.set_thumbnail(url="https://user-images.githubusercontent.com/54639269/71168042-aa5bad00-2234-11ea-875f-5745cba18f6a.png")
        embed.add_field(name="General", value="`say`, `info`, `help`, `avatar`, `creator`, `author`, `commands`", inline=False)
        embed.add_field(name="Moderator", value="`prune`, `clear`, `purge`, `kick`, `ban`, `unban`", inline=False)
        embed.set_footer(text="use prefix '$' to this commands")
        await ctx.channel.send(content=None, embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
