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

        users_in_purge = {}

        async for message in ctx.channel.history(limit = real_amount):
            user = f"{message.author.name}#{message.author.discriminator}"
            if not user in users_in_purge:
                users_in_purge[user] = 1
            else:
                users_in_purge[user] += 1

        users_in_purge_str = ""

        for itens in users_in_purge.keys():
            values = users_in_purge.get(itens)
            users_in_purge_str += f"{itens}: {values}{n1}"
                        
        await ctx.channel.purge(limit=real_amount)
        count = 5
        embed = discord.Embed(color=0x00ffff)
        embed.add_field(name="Total messages deleted", value=f"```c{n1}{amount}```", inline=False)
        embed.add_field(name="Deleted messages by user", value=f"```c{n1}{users_in_purge_str}```", inline=False)
        embed.set_footer(text="This message will be deleted in 5 seconds.")
        temp = await ctx.channel.send(content="All done! Your messages have been deleted", embed=embed)

        for x in range(4, -1 , -1):
            await asyncio.sleep(1)
            count = x
            uptade_embed = discord.Embed(color=0x00ffff)
            uptade_embed.add_field(name="Total messages deleted", value=f"```c{n1}{amount}```", inline=False)
            uptade_embed.add_field(name="Deleted messages by user", value=f"```c{n1}{users_in_purge_str}```", inline=False)
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
