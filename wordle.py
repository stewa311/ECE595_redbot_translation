from redbot.core import commands
from redbot.core.utils.chat_formatting import box, bordered, pagify, bold
import discord

class MyCog(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot
        self.word = 'tepid'
        self.count = 0

    @commands.command()
    async def mycom(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can do stuff!")
        await ctx.send(box(bold("I can do stuff!")))
        await ctx.send(bordered("I can do stuff!"))
        await ctx.send(bold("I can do stuff!"))
        await ctx.send(pagify("I can do stuff!"))
        text = str("""```\n\u001b[1;32m[Testing```""")
        text2 = str("""```\u001b[1;32m[Testing```""")
        text3 = str("""```ansi\n\u001b[0;32mThis is some colored Text```""")
        text4 = str("```ansi\n\u001b[0;40mThis is some colored Text```")

        await ctx.send(text)
        await ctx.send(text2)
        await ctx.send(text3)
        await ctx.send(text4)


    async def message(self, ctx, msg):
        if msg.equals('%start'):
            await ctx.send("I can do stuff!")

    @commands.command()
    async def guess(self, ctx, guess: str):
        #await ctx.send("Test " + guess)
        guess_list = list(guess.lower())
        if len(guess) != 5:
            await ctx.send("Please guess a 5 letter word!")
        if len(guess) == 5:
            result = ''
            # can maybe upgrade this to a hashmap
            for i in range(len(guess_list)):
                if guess_list[i] not in list(self.word):
                    result += " :red_square:"
                    #result += "```ansi\n\u001b[1;31m" + guess_list[i] + "```"
                    self.count += 1
                elif (guess_list[i] in list(self.word)) and (self.word[i] != guess_list[i]):
                    result += " :yellow_square:"
                    #result += "```ansi\n\u001b[1;33m" + guess_list[i] + "```"
                    self.count += 1
                elif guess_list[i] == self.word[i]:
                    result += " :green_square:"
                    #result += "```ansi\n\u001b[1;32m" + guess_list[i]
                    self.count += 1
            await ctx.send(result + "     " + " Tries: " + str(int(self.count / 5)))

            if result == " :green_square:" * 5:
                await ctx.channel.send(
                    "Congratulations. You have got the word in " + str(int(self.count / 5)) + " tries")
                #await ctx.send("The word has been reset. Start guessing again!")
                #word = random.choice(word_list)
                #count = 0
                print(self.word)
