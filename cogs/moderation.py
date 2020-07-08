import asyncio
import discord
from discord.ext import commands
from discord.utils import get

n1 = '\n'

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Comands
    @commands.command(pass_context=True, aliases=('purge', 'cls'))
    @commands.has_permissions(manage_messages=True)
    async def prune(self, ctx, amount='1'):
        if amount == 'all':
            amount = '100'

        real_amount = int(amount)
        if int(amount) < 100:
            real_amount += 1
            
        print(f"prunning {amount} messages")
        await ctx.channel.purge(limit=real_amount)
        count = 5
        embed = discord.Embed(title="All done!", description="Your messages have been deleted")
        embed.add_field(name="Total messages deleted:", value=f"```c{n1}{amount}{n1}```")
        embed.set_footer(text="This message will be deleted after 5 seconds.")
        temp = await ctx.channel.send(content=None, embed=embed)

        for x in range(4, -1 , -1):
            await asyncio.sleep(1)
            count = x
            uptade_embed = discord.Embed(title="All done!", description="Your messages have been deleted")
            uptade_embed.add_field(name="Total messages deleted:", value=f"```c{n1}{amount}{n1}```")
            uptade_embed.set_footer(text=f"This message will be deleted in {count} seconds.")
            await temp.edit(embed=uptade_embed)
        await temp.delete()

    @prune.error
    async def about_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.channel.send("You don't have permissions to use that command")


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, members : commands.Greedy[discord.Member],*, reason=None):
        for member in members:
            await member.kick(reason=reason)
            await ctx.send(f"Member {member.mention} has been kicked from the server! Reason: {reason}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, members : commands.Greedy[discord.Member],*, reason=None):
        for member in members:
            await member.ban(reason=reason)
            await ctx.send(f"Member {member.mention} has been banned from the server! Reason: {reason}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx,*, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Member {member.mention} has been unbanned from the server!")
                return

def setup(bot):
    bot.add_cog(Moderation(bot))
