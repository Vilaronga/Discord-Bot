import discord
from discord.ext import commands, tasks
from datetime import time
from zoneinfo import ZoneInfo

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.enviar_mensagem.start()

    ############################################################################################################################################ tasks
    #tasks são tarefas que, por exemplo, podem ser programadas para serem realizadas constantemente
    #tudo que for task é necessário inicializar ou seja, devo chamar essa função da task no inicializar do bot (on_ready)
    #enviar_mensagem.start()

    #Nessa task, importamos a biblioteca time para obter um horário específico e programamos a task para enviar uma mensagem sempre naquele mesmo horário em um canal específico.

    @tasks.loop(time=time(21, 55, tzinfo=ZoneInfo('America/Sao_Paulo')))
    async def enviar_mensagem(self):
        canal = self.bot.get_channel(1437979561085370409)
        guild = self.bot.get_guild(1349209862751649862)
        usuario = guild.get_member(718883021960511549)
        await canal.send(f'⚠️ Lembre-se de realizar o commit no github, {usuario.mention}.')

async def setup(bot):
    await bot.add_cog(Tasks(bot))