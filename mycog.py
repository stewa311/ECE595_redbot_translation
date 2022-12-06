from redbot.core import commands
from translate import Translator
from random import randint
import json
import os

# Wordle
import discord
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

squareSize = 62
width = 330
height = 397

ColorAbsent = Image.new('RGB', size=(squareSize, squareSize), color=(58, 58, 60))
EmptySquare = Image.new('RGB', size=(squareSize, squareSize), color=(197, 197, 195))
GreenSquare = Image.new('RGB', size=(squareSize, squareSize), color=(83, 141, 78))
YellowSquare = Image.new('RGB', size=(squareSize, squareSize), color=(181, 159, 59))


class MyCog(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot
        self.numanswers = 0
        self.maxtries = 2
        self.filepath = 'data/mycog/user.json' #Change it to the right user filepath
        
        #Wordle
        self.word = ""
        self.count = 0
        self.background = None
        self.rowOffset = 0
        self.lang = "eng"
        self.fp = None

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

        with open('data/mycog/languages.json') as json_file:
            data = json.load(json_file)

        for language in data['languages']:
            if language["English"] == search:
                await ctx.send(language["English"] +": " + language["alpha2"])
                return

        temp = [language["English"] + ": " + language["alpha2"] + "\n" for language in data['languages1']]
        await ctx.send("".join(temp))
        temp = [language["English"] + ": " + language["alpha2"] + "\n" for language in data['languages2']]
        await ctx.send("".join(temp))

    @commands.command()
    async def quiz_settings(self, ctx, maxtries=2):
        """This sets quiz settings
        
            inputs:
                maxtries = max number of tries per question to set
        """

        self.maxtries = maxtries
        await ctx.send("Max tries set to " + str(self.maxtries))

    @commands.command()
    async def quiz(self, ctx, lang, difficulty="1"):
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
            qn = randint(0,len(data[lang][difficulty])-1)
            with open('data/mycog/currentQuestion.json', 'w') as outfile:
                json.dump({data[lang][difficulty][qn]:data[lang][difficulty+"a"][qn]}, outfile)
            await ctx.send(data[lang][difficulty][qn])

    @commands.command()
    async def answer(self, ctx, answer=None):
        """This command sends an answer to the current quiz
        
            inputs:
                answer = the players answer to the current quiz
        """

        try:
            with open('data/mycog/currentQuestion.json') as json_file:
                question = json.load(json_file)
            if question == None:
                await ctx.send("No active quiz")
                return
        except FileNotFoundError:
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
            if self.numanswers >= self.maxtries:
                await ctx.send("Too many incorrect tries, ending quiz")
                with open('data/mycog/currentQuestion.json', 'w') as outfile:
                    json.dump(None, outfile)
                return
            await ctx.send("Thats not it. Try again!")
    
    #Wordle
    @commands.command()
    async def start(self, ctx, lang):
        # load in word, how to do decide which

        # Error check the language? Or should we sync with quiz game
        lang_dict = {"English": "eng", "French": "fra", "Italian": "ita", "Latin": "lat", "Portugese": "por", "Spanish": "spa"}
        if lang in lang_dict.keys():
            lang = lang_dict[lang]
            self.lang = lang
        else:
            await ctx.send("Error: Language not supported \nSupported Languages: " + ', '.join(lang_dict.keys()))
            return

        self.fp = str(os.path.dirname(os.path.abspath(__file__))) + '/' + str(self.lang) + '.json'
        #fp = 'ECE595_redbot_translation/' + str(lang) + '.json'

        with open(self.fp) as json_file:
            data = json.load(json_file)

        self.word = data[randint(0, len(data)-1)]
        self.count = 0
        self.background = Image.new('RGB', size=(width, height))
        self.rowOffset = 0

        rowOffset_setup = 0
        buffer = 0

        for i in range(6):
            row = []
            for j in range(5):
                square = EmptySquare
                self.background.paste(square, (j * squareSize + buffer, rowOffset_setup))
                buffer += 5
                row.append("")

            rowOffset_setup += squareSize + 5
            buffer = 0

        with BytesIO() as image_binary:
            self.background.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.send(file=discord.File(image_binary, "abc.png"))
    
    @commands.command()
    async def guess(self, ctx, guess: str):
        # Validate guess
        if self.invalid_check(guess):
            await ctx.send(self.invalid_check(guess))
            return

        # Guess is valid
        guess_list = list(guess.lower())
        square = ColorAbsent
        buffer = 0

        for j in range(5):
            if guess_list[j] not in list(self.word):
                square = EmptySquare
            elif (guess_list[j] in list(self.word)) and (self.word[j] != guess_list[j]):
                square = YellowSquare
            elif guess_list[j] == self.word[j]:
                square = GreenSquare

            # Update grid
            x_offset = j * squareSize + buffer
            self.background.paste(square, (x_offset, self.rowOffset))

            myFont = ImageFont.truetype('arial.ttf', 42)
            editable = ImageDraw.Draw(self.background)
            _, _, w, h = editable.textbbox((0, 0), str(guess_list[j]), font=myFont)
            editable.text(((squareSize - w) // 2 + x_offset, (squareSize - h) // 2 + self.rowOffset),
                          str(guess_list[j]), font=myFont, fill=(40, 37, 35))

            buffer += 5

        self.rowOffset += squareSize + 5
        self.count += 1

        with BytesIO() as image_binary:
            self.background.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.send(file=discord.File(image_binary, "abc.png"))

        if len(self.endgame(guess)) > 0:
            await ctx.send(self.endgame(guess))

    def endgame(self, guess):
        msg = ""
        if guess == self.word and self.count <= 6:
            msg = "Congrats!!! You won in " + str(self.count) + " tries"
        elif self.count == 6:
            msg = "Darn, the word was: " + self.word + "\nTo play a new game enter ' %start <lang>'"
        return msg

    def invalid_check(self, guess):
        msg = ""
        with open(self.fp) as json_file:
            data = json.load(json_file)

        if self.count >= 6:
            # Count needs to be less than 5
            msg = "Please start a new game by entering ' %start <lang>'"
        elif len(guess) != 5:
            # Length needs to be 5
            msg = "Please guess a 5 letter word!"
        elif guess not in data:
            msg = "Please guess a valid word!"

        return msg
    
    # End Wordle  
                
                

    @commands.command()
    async def register_user(self, ctx, username=None):

        if (username == None) or (username == ""):
            username = str(ctx.message.author)

        input_data = {"username": username,
                "wordle":0,
                "quiz":0}

        with open(self.filepath, "a+") as file:
            file.seek(0)
            if not file.read():
                json.dump([], file, indent=4)

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
    
