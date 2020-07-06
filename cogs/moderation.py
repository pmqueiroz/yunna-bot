import asyncio
import discord
from discord.ext import commands


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Comands
    @commands.command(pass_context=True, aliases=('purge', 'clear'))
    @commands.has_permissions(manage_messages=True)
    async def prune(self, message, amount='1'):
        if amount == 'all':
            amount = '100'
        print(f"prunning {amount} messages")
        await message.channel.purge(limit=int(amount))
        embed = discord.Embed(title="All done!", description="Your messages have been deleted")
        embed.add_field(name="Total messages deleted:", value=amount)
        embed.set_footer(text="This message will be deleted after 5 seconds.")

        await message.channel.send(content=None, embed=embed)
        await asyncio.sleep(5)

        def is_bot(ctx):
            return ctx.author.id == 635227108335157268

        await message.channel.purge(limit=3, check=is_bot)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member,*, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"Member {member.mention} has been kicked from the server! Reason: {reason}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member,*, reason=None):
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
