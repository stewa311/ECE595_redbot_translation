from .culture import culture


def setup(bot):
    bot.add_cog(culture(bot))