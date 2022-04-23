import scraper
from dotenv import load_dotenv
import discord
from discord.ext import commands
import os

def main():
    description = 'Covid-19 pandemic tracker bot.'
    load_dotenv('.env')
    token = os.environ['bot_token']
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix='!', description=description, intents=intents)
    sc = scraper.CovidScraper()

    @bot.event
    async def on_ready():
        print('Logged in as:')
        print(bot.user.name)
        print(bot.user.id)
        print('-------------')

    @bot.command()
    async def covid(ctx, arg: str):
        try:
            sc.scrapeCountry(arg)
        except Exception as e:
           await ctx.send(e)
           return

        news = sc.getNews()
        message = '```\nLatest news from ' + arg + ':' + '\n'
        for n in news:
            message += '\t• ' + n["date"] + ': infected: ' + str(n["numbers"][0]) + ' dead: ' + str(n["numbers"][1]) + '\n'
        message += '\n```'
        await ctx.send(message)
        
    @bot.command()
    async def source(ctx):
        await ctx.send('https://www.worldometers.info/coronavirus/')

    bot.run(token)
    
if __name__ == "__main__":
    main()