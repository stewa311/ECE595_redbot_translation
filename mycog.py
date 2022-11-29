from redbot.core import commands
from translate import Translator
from random import randint
import json

class MyCog(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mycom(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can do stuff!")

    @commands.command()
    async def trans(self, ctx, lang, msg="This does something!"):
        """This translates a message to the given language
        
            inputs:
                lang = 2 letter abbrieviation of langauge to translate to 
                msg = message to be translated
        """
        
        #await ctx.send(lang)
        translator = Translator(to_lang=lang)
        await ctx.send(translator.translate(msg))
    
    @commands.command()
    async def langlist(self, ctx, search=None):
        """This lists languages and their 2 letter code, or searches a language code
        
            inputs:
                search = language to be searched (case sensative)
        """

        with open('data/mycog/info.json') as json_file:
            data = json.load(json_file)
        if search not in data['languages']:
            await ctx.send(data['languages1'])
            await ctx.send(data['languages2'])
        else:
            for language in data['languages']:
                if language["English"] == search:
                    await ctx.send(language["English"] +": " + language["alpha2"])


    @commands.command()
    async def quiz(self, ctx, lang, difficulty="1", length=1):
        """This command starts a quiz
        
            inputs:
                lang = language to be quized (case sensative)
                length = number of quiz questions to be asked
                difficulty = difficulty level (1-3)
        """

        with open('data/mycog/questions.json') as json_file:
            data = json.load(json_file)
        if lang in data['supported_languages'].keys():
            lang = data['supported_languages'][lang]
        if lang not in data['supported_languages'].values():
            await ctx.send("Error: Language not supported \nSupported Languages: " + ', '.join(data['supported_languages']))
        else:
            qn = randint(0,4)
            with open('data/mycog/currentQuestion.json', 'w') as outfile:
                json.dump({data[lang][difficulty][qn]:data[lang][difficulty+"a"][qn]}, outfile)
            await ctx.send(data[lang][difficulty][qn])
            #await ctx.send("Quiz Started")
            #for i in range(1,length + 1):
            #    qn = randint(1,10)
            #    await ctx.send("Question " + str(i) + ": " + str(qn))
                
    @commands.command()
    async def answer(self, ctx, answer=None):
        """This command sends an answer to the current quiz
        
            inputs:
                answer = the players answer to the current quiz
        """

        with open('data/mycog/currentQuestion.json') as json_file:
            question = json.load(json_file)
        if answer in question.values():
            await ctx.send("Correct!")
        elif answer == "__GIVEMETHEANSWER__":
            await ctx.send(', '.join(question.values()))
        else:
            await ctx.send("Thats not it. Try again!")
            
            
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
