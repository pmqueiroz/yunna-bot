import discord
from discord.ext import flags, commands
from googletrans import Translator

class useful(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @flags.add_flag("--lan", default='en')
    @flags.add_flag("msg", nargs='+')
    @flags.command()
    async def translate(self, ctx, **flags):
        arg = flags["msg"]
        message = ' '.join(arg)
        dest = flags["lan"]
        translator = Translator(service_urls=['translate.google.com'])
        translation = translator.translate(message, dest=dest)
        await ctx.channel.send(translation.text)


def setup(bot):
    bot.add_cog(useful(bot))
