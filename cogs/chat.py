import discord
from discord.ext import commands
import wikipedia,os
from chatbot import Chat, register_call

class ChatCog(commands.Cog, name='event'):
    def __init__(self, bot):
        self.bot = bot
        global bot_
        bot_ = self.bot
        
    @register_call("whoIs")
    
    def who_is(query, session_id="general"):
        try:
            return wikipedia.summary(query)
        except Exception:
            for new_query in wikipedia.search(query):
                try:
                    return wikipedia.summary(new_query)
                except Exception:
                    pass
        return "I don't know about "+query


    template_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"chatbotTemplate","chatbottemplate.template")

    global chat
    chat=Chat(template_file_path)
    
    #The next code is for the bot can reply
    @bot_.command(pass_context = True)
    async def chatbot(ctx, *, message):
        result = chat.respond(message)
        if(len(result)<=2048):
            embed=discord.Embed(title="ChatBot AI", description = result, color = (0xF48D1))
            await ctx.send(embed=embed)
        else:
            embedList = []
            n=2048
            embedList = [result[i:i+n]for i in range(0, len(result), n)]
            for num, item in enumerate(embedList, start = 1):
                if(num == 1):
                    embed = discord.Embed(title="ChatBot AI", description = item, color = (0xF48D1))
                    embed.set_footer(text="Page{}".format(num))
                    await ctx.send(embed = embed)
                else:
                    embed = discord.Embed(description = item, color = (0xF48D1))
                    embed.set_footer(text = "Page {}".format(num))
                    await ctx.send(embed = embed)
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ChatCog(bot))