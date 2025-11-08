import discord #importa toda a api do discord
from discord.ext import commands
from dotenv import load_dotenv
import os

#Importação de tokens do arquivo .env
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

#intents = permissões do discord que o bot necessita para operar
intents = discord.Intents.all() #essa variável armazena TODAS as permissões do discord
bot = commands.Bot(command_prefix='!', intents = intents) #variável objeto que armazena todo o bot

#Ao atribuir commands.Bot para a variável bot, automaticamente a classe bot cria um atributo bot.tree (onde se encontram todos os comandos)
#em cada módulo do cogs, os comandos são criados à parte e somente são implementados bot.tree através do setup do módulo em bot.add_cogs

#Importação de módulos pessoais
#não se deve passar a extensão do arquivo para ser carregado, somente o nome
'''bot.load_extension('cogs.calculos')'''

#Essa função carrega todos os cogs presentes, é um loop que passa carregando de arquivo em arquivo sem a necessidade de carregar individualmente.
async def carregar_cogs():
    for arquivo in os.listdir('cogs'):
        if arquivo.endswith('.py'): #impede que leia qualquer coisa que não seja um arquivo .py
            await bot.load_extension(f'cogs.{arquivo[:-3]}') #caso seja passado somente {arquivo}, será identificado o .py, por isso utiliza-se p [:-3] para que os 3 ultimos indices não sejam lidos

#Importação de módulos pessoais
##bot.load_extension('cogs.calculos')

##########################################################################################################################################
## Evento de inicialização

@bot.event  #criação de um evento que é disparado quando o bot estiver pronto
async def on_ready():
    await carregar_cogs()
    sincs = await bot.tree.sync()  #não é recomendado realizar a sincronização dos comandos na inicializaçao do bot pois é possível que o limite de tráfego de dados do discord seja ultrapassado. Por isso, o mais recomendado é utilizar um comando manual de sincronização
    print(f'{len(sincs)} app_commands sincronizados!')
    print('Bot inicializado com sucesso')

##########################################################################################################################################
## Comando de sincronização

'''@bot.command()
async def sinc(ctx:commands.Context):
    if ctx.author.get_role(1436841614252441620) and ctx.channel.id == 1436850771336499311: #Verifica se o usuário possui o cargo de administrador e se está no canal correto para realizar.
        sincs = await bot.tree.sync()
        await ctx.reply(f'{ctx.author.mention}, {len(sincs)} app_commands sincronizados!')
    else:
        if ctx.author.get_role(1436841614252441620) == None:
            await ctx.reply('Apenas usuários administradores podem utilizar este comando.')
        elif ctx.channel.id != 1436850771336499311:
            await ctx.reply(f'O comando está sendo utilizado no canal errado, tente no canal {ctx.guild.get_channel(1436850771336499311).mention}')'''

############################################################################################################################################
bot.run(TOKEN)