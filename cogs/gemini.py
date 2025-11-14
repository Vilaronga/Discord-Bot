import discord
from discord.ext import commands
from discord import app_commands
import os
from google import genai
from dotenv import load_dotenv
import textwrap

load_dotenv()

GEMINI_KEY=os.getenv("GEMINI_KEY")
client = genai.Client(api_key=GEMINI_KEY)

class Gemini(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='gemini', description='Faz uma pergunta ao chat gpt.')
    async def gpt(self, interact:discord.Interaction, pergunta:str):
        await interact.response.defer()
        resposta = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=pergunta
            )
        text = resposta.text

        texto_dividido = textwrap.wrap(text, width=1900, replace_whitespace=False)     #empacota a string com mais de 2000 caracteres em substrings com até 1900 char
        primeiro_texto = f'🤖 gemini-2.5-flash: Página 1/{len(texto_dividido)}\n\n{texto_dividido[0]}' #Pega a quantidade de sub-strings e a string contida no primeiro índice.
        await interact.followup.send(primeiro_texto) #enviar a primeira string
        for i, texto in enumerate(texto_dividido[1:], start=2): 
            await interact.channel.send(f'{i}/{len(texto_dividido)}:\n\n{texto}')

async def setup(bot):
    await bot.add_cog(Gemini(bot))