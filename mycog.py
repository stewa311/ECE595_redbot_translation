from redbot.core import commands
from translate import Translator
from random import randint
import json

class MyCog(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot
        self.numanswers = 0
        self.filepath = 'data/mycog/user.json' #Change it to the right user filepath

    def update_quizScore(self, score, username):
        with open(self.filepath, "r") as file:
            data = json.load(file)

        for user in data:
            if (user["username"].lower() == username.lower()):
                user["quiz"] += score
                break
        
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

    def update_wordleScore(self, score, username):
        with open(self.filepath, "r") as file:
            data = json.load(file)

        for user in data:
            if (user["username"].lower() == username.lower()):
                user["wordle"] += score
                break
        
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)    

    @commands.command()
    async def trans(self, ctx, lang, msg="This translates messages!"):
        """This translates a message to the given language
        
            inputs:
                lang = 2 letter abbrieviation of langauge to translate to 
                msg = message to be translated
        """
        
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
                lang = language to be quized (lowercase)
                length = number of quiz questions to be asked
                difficulty = difficulty level (1-3)
        """

        self.numanswers = 0
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
                
    @commands.command(pass_context=True)
    async def answer(self, ctx, answer=None):
        """This command sends an answer to the current quiz
        
            inputs:
                answer = the players answer to the current quiz
        """

        with open('data/mycog/currentQuestion.json') as json_file:
            question = json.load(json_file)
        if question == None:
            await ctx.send("No active quiz")
            return
        if answer in question.values():
            await ctx.send("Correct! Quiz complete.")
            MyCog.update_quizScore(self, 1, str(ctx.message.author))
            with open('data/mycog/currentQuestion.json', 'w') as outfile:
                json.dump(None, outfile)
        elif answer == "__GIVEMETHEANSWER__":
            await ctx.send(', '.join(question.values()))
        else:
            self.numanswers +=1
            if self.numanswers >= 4:
                await ctx.send("Too many incorrect tries, ending quiz")
                with open('data/mycog/currentQuestion.json', 'w') as outfile:
                    json.dump(None, outfile)
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

    @commands.command()
    async def register_user(self, ctx, username=None):

        if (username == None) or (username == ""):
            username = str(ctx.message.author)

        input_data = {"username": username,
                "wordle":0,
                "quiz":0}

        with open(self.filepath, "r") as file:
            data = json.load(file)
            
        for user in data:
            if (user["username"].lower() == username.lower()):
                real_id = user["username"]
                await ctx.send(f"{real_id} is already registered!")
                return
                
        data.append(input_data)
        
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)
            await ctx.send(f"{username} is registered")

    @commands.command()    
    async def delete_user(self, ctx, username):
        if (username == None) or (username == ""):
            await ctx.send("Please enter a valid username after the command.")

        with open(self.filepath, "r") as file:
            data = json.load(file)
            
        for user in data:
            if (user["username"].lower() == username.lower()):
                real_id = user["username"]
                data.remove(user)
                with open(self.filepath, "w") as file:
                    json.dump(data, file, indent=4)
                await ctx.send(f"{real_id} is deleted.")
                return
        
        await ctx.send(f"{real_id} doesn't exist!")

    @commands.command()    
    async def leaderboard(self, ctx):
        with open('data/mycog/user.json', "r") as file:
            data = json.load(file)
        
        board = []
        width_name = 0
        width_num = 5
        for user in data:
            total_score = {"username":user["username"], "score":user["wordle"] + user["quiz"]}
            board.append(total_score)
            length = len(user["username"])
            if length > width_name:
                width_name = length
            length = len(str(total_score["score"]))
            if length > width_num:
                width_num = length

        sort_board = sorted(board, key=lambda k: k["score"], reverse=True)
        table = ""
        table += "-"*width_name*3+"\n"
        pad_name = 0 if 4 == width_name else (width_name-4)
        pad_num = 0 if 5 == width_num else (width_num-5)
        table += "| " + " "*pad_name + "User" + " "*pad_name + " | " + " "*pad_num + "Score" + " "*pad_num + " |" + "\n"
        table += "-"*width_name*3+"\n"

        for row in sort_board:
            name_len = len(row["username"])
            pad_name = 0 if name_len == width_name else (width_name-name_len)
            num_len = len(str(row["score"]))
            pad_num = 0 if num_len == width_num else (width_num-num_len)
            table += "| "+" "*pad_name+row["username"]+" "*pad_name+" | "+" "*pad_num+str(row["score"])+" "*pad_num+" |"+"\n"
        table += "-"*width_name*3+"\n"

        await ctx.send(table)
    