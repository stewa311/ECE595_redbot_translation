from redbot.core import commands
import json
import os

class MyCog(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot
        self.filepath = "/home/nishantsk17/Desktop/ece595/mycog/user.json"
        #self.filepath = os.getcwd() + "/data_file.json"

    @commands.command()
    async def mycom(self, ctx):
        # Your code will go here
        await ctx.send("Hello World!")

    @commands.command()    
    async def register_user(self, ctx, username):
        if (username == None) or (username == ""):
            await ctx.send("Please enter a valid username after the command.")

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
        with open(self.filepath, "r") as file:
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
    
    def update_quizScore(self, score, username):
        with open(self.filepath, "r") as file:
            data = json.load(file)

        for user in data:
            if (user["username"].lower() == username.lower()):
                user["quiz"] = score
                break
        
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

    def update_wordleScore(self, score, username):
        with open(self.filepath, "r") as file:
            data = json.load(file)

        for user in data:
            if (user["username"].lower() == username.lower()):
                user["wordle"] = score
                break
        
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

        

