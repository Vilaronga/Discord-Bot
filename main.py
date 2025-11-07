import discord #importa toda a api do discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
from datetime import time

#Importação de token do arquivo .env
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

#intents = permissões do discord que o bot necessita para operar
intents = discord.Intents.all() #essa variável armazena TODAS as permissões do discord
bot = commands.Bot(command_prefix='!', intents = intents) #variável objeto que armazena todo o bot

##########################################################################################################################################
## Events

@bot.event  #criação de um evento que é disparado quando o bot estiver pronto
async def on_ready():
    synced_commands = await bot.tree.sync()
    print(f'{len(synced_commands)} comandos sincronizados.')
    enviar_mensagem.start()
    print('bot inicializado com sucesso')

@bot.event
async def on_message(msg:discord.Message):
    if msg.author.bot:
        return
    await bot.process_commands(msg)
    #await msg.reply(f'Olá {msg.author.mention}')

@bot.event #evento que é disparado quando um novo usuário se junta ao discord
async def on_member_join(member:discord.Member): #o parâmetro member armazena: member:discord.Member 
    canal = bot.get_channel(1436358990069104821) #aqui é atribuido um canal específico para o bot enviar a mensagem de boas-vindas
    await canal.send(f'Bem vindo ao servidor {member.mention}!') #canal.send: envia a msg no canal específico mencionando o novo membro.

@bot.event
async def on_reaction_add(reacao:discord.Reaction, membro:discord.Member):
    await reacao.message.reply(f'O membro {membro.mention} reagiu a mensagem com {reacao.emoji}')

##########################################################################################################################################
## tasks
#tasks são tarefas que, por exemplo, podem ser programadas para serem realizadas constantemente
#tudo que for task é necessário inicializar ou seja, devo chamar essa função da task no inicializar do bot (on_ready)
#enviar_mensagem.start()

@tasks.loop(time=time(12,0)) #Nessa task, importamos a biblioteca time para obter um horário específico e programamos a task para enviar uma mensagem sempre naquele mesmo horário em um canal específico.
async def enviar_mensagem():
    canal = bot.get_channel(1349209863590514751)
    await canal.send(f'Olá')

##########################################################################################################################################
## Commands

@bot.command()
async def somar(ctx:commands.Context, num1:float, num2:float):
    soma = num1 + num2
    await ctx.reply(f'{ctx.author.mention}, a soma entre {num1} e {num2} é:  {soma}')

@bot.command()
async def ola(ctx:commands.Context):        #ctx variável que é do tipo Context - context - guarda todas as informações e processos relativos ao uso do comando, como por   exemplo canal em que foi chamado, quem chamou e etc.
    nome = ctx.author.name
    await ctx.reply(f'Olá, {nome}! Tudo bem?')

##########################################################################################################################################
## Slash Commands - Mais utilizados

#Invés de utilizar ctx - context, usaremos o interaction. Eles possuem os mesmos objetos, são parecidos no que fazem mas funcionam de forma diferente.

#O interection não representa o contexto, mas sim uma interação.
#Name define o nome do comando
#Dscription define a descrição do comando que estará visível no discord para o usuário
#Uma diferença que tem no Interaction e que não tem context, é o parametro ephemeral. 
#Ephemeral determina que aquela resposta somente será visível para o usuário que realizou a interação. Ou seja, quem chamou o comando.

#A limitação do interaction é que ele só pode mandar uma resposta, ou seja só pode haver um interact.response...
#Caso a resposta demore mais de 3 segundo para sair, o bot dará um erro, então para contornar isso, utilizamos interact.response.defer()
#para contornar isso, utilizamos o interact.followup.send(), onde ele entende que é uma continuação da mensagem.

@bot.tree.command(name='ola', description='Diz olá para o usuário.')
async def ola(interact:discord.Interaction): 
    await interact.response.defer(ephemeral=True)
    await interact.followup.send(f'Olá, {interact.user.mention}')

@bot.tree.command(name='somar', description='Realiza a soma entre 2 números.')
async def somar(interact:discord.Interaction, num1:float, num2:float):
    res = num1 + num2
    await interact.response.defer(ephemeral=True)
    await interact.followup.send(f'A soma entre {num1} e {num2} é igual a: {res}', ephemeral=True)

@bot.tree.command(name='subtrair', description='Realiza a subtração entre 2 números.')
async def subtrair(interact:discord.Interaction, num1:float, num2:float):
    res = num1 - num2
    await interact.response.defer(ephemeral=True)
    await interact.followup.send(f'A subtração entre {num1} e {num2} é igual a: {res}', ephemeral=True)

@bot.tree.command(name='multiplicar', description='Realiza a multiplicação entre 2 números.')
async def multiplicar(interact:discord.Interaction, num1:float, num2:float):
    res = num1 * num2
    await interact.response.defer(ephemeral=True)
    await interact.followup.send(f'A multiplicação entre {num1} e {num2} é igual a: {res}', ephemeral=True)

@bot.tree.command(name='dividir', description='Realiza a divisão entre 2 números.')
async def dividir(interact:discord.Interaction, num1:float, num2:float):
    res = num1 / num2
    await interact.response.defer(ephemeral=True)
    await interact.followup.send(f'A divisão entre {num1} e {num2} é igual a: {res}', ephemeral=True)

@bot.tree.command(name='par_ou_impar', description='Verifica se um número é par ou ímpar.')
async def par_ou_impar(interact:discord.Interaction, num1:int):
    if num1 % 2 == 0:
        res = 'par'
    else:
        res = 'impar'
    await interact.response.defer(ephemeral=True)
    await interact.followup.send(f'O número {num1} é {res}.', ephemeral=True)

@bot.tree.command(name='github', description='Divulge o seu GitHub')
async def github_slash(interact:discord.Interaction, url_github:str, seu_nome:str, descrição:str):
    embed = discord.Embed()
    embed.set_author(name=seu_nome)
    embed.title = 'Clique aqui para acessar meu GitHub'
    embed.url = url_github
    embed.description = descrição
    imagem = discord.File('images/github_logo_black.png', 'github_logo_black.png')
    embed.set_image(url='attachment://github_logo_black.png')
    embed.set_thumbnail(url='attachment://github_logo_black.png')
    embed.set_footer(text='Divulgação GitHub')
    embed.color = 16777215
    await interact.response.defer()
    await interact.followup.send(embed=embed, file=imagem)
##########################################################################################################################################
## Embeds ##

@bot.command()
async def enviar_embed(ctx:commands.Context):
    embed = discord.Embed() #criação do objeto embed
    embed.title = 'Olá'
    embed.description = 'Teste de criação de uma mensagem embed.'

    imagem = discord.File('images/tropa.jpg', 'tropa.jpg') #criação de um objeto imagem, primeiro parametro é a localização e depois nomeando a imagem
    embed.set_image(url='attachment://tropa.jpg')
    embed.set_thumbnail(url='attachment://tropa.jpg')
    embed.set_footer(text='Mensagem de teste')
    embed.set_author(name='Lucas Vilaronga', icon_url=ctx.author.avatar)

    await ctx.reply(embed=embed, file=imagem)

@bot.command()
async def github(ctx:commands.Context):
    embed = discord.Embed()
    embed.title = 'Github - Lucas Vilaronga'
    embed.description = 'Estudante do segundo período de Análise e Desenvolvimento de Sistemas pela Universidade Tirantes - UNIT. Confira meus projetos clicando na imagem abaixo.'
    embed.url = 'https://github.com/Vilaronga?tab=repositories'
    embed.set_author(name='Lucas Vilaronga', icon_url='https://avatars.githubusercontent.com/u/106574077?v=4&size=64')
    imagem = discord.File('images/github_logo_black.png', 'github_logo_black.png')
    embed.set_image(url='attachment://github_logo_black.png')
    embed.set_thumbnail(url='attachment://github_logo_black.png')
    embed.set_footer(text='Test footer')
    embed.color = 16777215
    await ctx.reply(embed=embed, file=imagem)

############################################################################################################################################
bot.run(TOKEN)