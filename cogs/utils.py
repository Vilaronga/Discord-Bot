import discord
from discord import app_commands
from discord.ext import commands

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='ola', description='Diz olá para o usuário.')
    async def ola(self, interact:discord.Interaction): 
        await interact.response.defer(ephemeral=True)
        await interact.followup.send(f'Olá, {interact.user.mention}')

    @app_commands.command(name='par_ou_impar', description='Verifica se um número é par ou ímpar.')
    async def par_ou_impar(self, interact:discord.Interaction, num1:int):
        if num1 % 2 == 0:
            res = 'par'
        else:
            res = 'impar'
        await interact.response.defer(ephemeral=True)
        await interact.followup.send(f'O número {num1} é {res}.', ephemeral=True)    

async def setup(bot):
    await bot.add_cog(Utils(bot))