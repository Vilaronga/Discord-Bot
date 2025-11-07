import discord
from discord import app_commands
from discord.ext import commands

#criamos uma classe de calculos e fazemos ela herdar de commands.Cog
class Calculos(commands.Cog):
    def __init__(self, bot): #quando essa classe for chamada, é esse init que irá rodar
        self.bot = bot

    @app_commands.command(name='somar', description='Realiza a soma entre 2 números.')
    async def somar(self, interact:discord.Interaction, num1:float, num2:float):
        res = num1 + num2
        await interact.response.defer(ephemeral=True)
        await interact.followup.send(f'A soma entre {num1} e {num2} é igual a: {res}', ephemeral=True)

    @app_commands.command(name='subtrair', description='Realiza a subtração entre 2 números.')
    async def subtrair(self, interact:discord.Interaction, num1:float, num2:float):
        res = num1 - num2
        await interact.response.defer(ephemeral=True)
        await interact.followup.send(f'A subtração entre {num1} e {num2} é igual a: {res}', ephemeral=True)

    @app_commands.command(name='multiplicar', description='Realiza a multiplicação entre 2 números.')
    async def multiplicar(self, interact:discord.Interaction, num1:float, num2:float):
        res = num1 * num2
        await interact.response.defer(ephemeral=True)
        await interact.followup.send(f'A multiplicação entre {num1} e {num2} é igual a: {res}', ephemeral=True)

    @app_commands.command(name='dividir', description='Realiza a divisão entre 2 números.')
    async def dividir(self, interact:discord.Interaction, num1:float, num2:float):
        res = num1 / num2
        await interact.response.defer(ephemeral=True)
        await interact.followup.send(f'A divisão entre {num1} e {num2} é igual a: {res}', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Calculos(bot))