import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener() #evento que é disparado quando um novo usuário se junta ao discord
    async def on_member_join(self, member:discord.Member): #o parâmetro member armazena: member:discord.Member 
        canal = commands.Bot.get_channel(1436358990069104821) #aqui é atribuido um canal específico para o bot enviar a mensagem de boas-vindas
        await canal.send(f'Bem vindo ao servidor {member.mention}!') #canal.send: envia a msg no canal específico mencionando o novo membro.

    @commands.Cog.listener()
    async def on_message(self, msg:discord.Message):
        if msg.author.bot:
            return
        elif msg.content == 'Ok':
            await msg.add_reaction('👌')

    @commands.Cog.listener()
    async def on_reaction_add(self, reacao:discord.Reaction, membro:discord.Member):
        if membro.bot:
            return
        else:
            await reacao.message.reply(f'O membro {membro.mention} reagiu a mensagem com {reacao.emoji}')

async def setup(bot):
    await bot.add_cog(Events(bot))