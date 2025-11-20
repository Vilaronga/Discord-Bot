import discord
from discord import app_commands
from discord.ext import commands

#criamos uma classe de calculos e fazemos ela herdar de commands.Cog
class Calculos(commands.Cog):
    def __init__(self, bot): #quando essa classe for chamada, é esse init que irá rodar
        self.bot = bot

    @app_commands.command(name='somar', description='Realiza a soma entre 2 números.')
    @app_commands.describe(num1='Digite o primeiro número', num2='Digite o segundo número')
    async def somar(self, interact:discord.Interaction, num1:float, num2:float):
        await interact.response.defer(thinking=True)
        guild = interact.guild
        canal = 1436390421352939611
        if interact.channel_id == canal:
            res = num1 + num2
            return await interact.followup.send(f'Resultado da soma entre **{num1}** e **{num2}** é: **{res}**')
        await interact.followup.send(f'Este comando não pode ser utilizado neste canal. Utilize {guild.get_channel(canal).mention}')
        
    @app_commands.command(name='subtrair', description='Realiza a subtração entre 2 números.')
    @app_commands.describe(num1='Digite o primeiro número', num2='Digite o segundo número')
    async def subtrair(self, interact:discord.Interaction, num1:float, num2:float):
        await interact.response.defer(thinking=True)
        guild = interact.guild
        canal = 1436390421352939611
        if interact.channel_id == canal:
            res = num1 - num2
            return await interact.followup.send(f'Resultado da subtração entre **{num1}** e **{num2}** é igual a: **{res}**')
        await interact.followup.send(f'Este comando não pode ser utilizado neste canal. Utilize {guild.get_channel(canal).mention}')

    @app_commands.command(name='multiplicar', description='Realiza a multiplicação entre 2 números.')
    @app_commands.describe(num1='Digite o primeiro número', num2='Digite o segundo número')
    async def multiplicar(self, interact:discord.Interaction, num1:float, num2:float):
        await interact.response.defer(thinking=True)
        guild = interact.guild
        canal = 1436390421352939611
        if interact.channel_id == canal:
            res = num1 * num2
            return await interact.followup.send(f'Resultado da multiplicação entre **{num1}** e **{num2}** é igual a: **{res}**')
        await interact.followup.send(f'Este comando não pode ser utilizado neste canal. Utilize {guild.get_channel(canal).mention}')

    @app_commands.command(name='dividir', description='Realiza a divisão entre 2 números.')
    @app_commands.describe(num1='Digite o primeiro número', num2='Digite o segundo número')
    async def dividir(self, interact:discord.Interaction, num1:float, num2:float):
        await interact.response.defer(thinking=True)
        guild = interact.guild
        canal = 1436390421352939611
        if interact.channel_id == canal:
            if num2 == 0:
                return await interact.followup.send('❌ Operação inválida. Não é possível dividir qualquer número por 0, tente outro valor.')
            res = num1 / num2
            return await interact.followup.send(f'➗ Resultado da divisão entre **{num1}** e **{num2}** é igual a: **{res}**')
        await interact.followup.send(f'Este comando não pode ser utilizado neste canal. Utilize {guild.get_channel(canal).mention}')

async def setup(bot):
    await bot.add_cog(Calculos(bot))