from redbot.core import commands
from translate import Translator
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
                search = language to be searched
        """

        with open('data/mycog/info.json') as json_file:
            data = json.load(json_file)
        if search == None:
            await ctx.send(data['languages1'])
            await ctx.send(data['languages2'])
        else:
            for language in data['languages']:
                if language["English"] == search:
                    await ctx.send(language)
