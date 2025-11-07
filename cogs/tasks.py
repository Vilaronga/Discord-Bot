import discord
from discord.ext import commands, tasks
from datetime import time

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.enviar_mensagem.start()

    ############################################################################################################################################ tasks
    #tasks são tarefas que, por exemplo, podem ser programadas para serem realizadas constantemente
    #tudo que for task é necessário inicializar ou seja, devo chamar essa função da task no inicializar do bot (on_ready)
    #enviar_mensagem.start()

    #Nessa task, importamos a biblioteca time para obter um horário específico e programamos a task para enviar uma mensagem sempre naquele mesmo horário em um canal específico.

    @tasks.loop(time=time(22,3))
    async def enviar_mensagem(self):
        canal = self.bot.get_channel(1349209863590514751)
        await canal.send(f'ola')

async def setup(bot):
    await bot.add_cog(Tasks(bot))