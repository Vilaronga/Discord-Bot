import discord #importa toda a api do discord
from discord.ext import commands
from dotenv import load_dotenv
import os

#Importação de token do arquivo .env
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
## Events 

@bot.event  #criação de um evento que é disparado quando o bot estiver pronto
async def on_ready():
    await carregar_cogs()
    synced_commands = await bot.tree.sync()
    print(f'{len(synced_commands)} comandos sincronizados.')
    print('bot inicializado com sucesso')

############################################################################################################################################
bot.run(TOKEN)