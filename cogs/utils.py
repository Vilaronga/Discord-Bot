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
    @app_commands.describe(num1='Digite um número.')
    async def par_ou_impar(self, interact:discord.Interaction, num1:int):
        await interact.response.defer(thinking=True, ephemeral=True)
        guild = interact.guild
        canal = guild.get_channel(1436359098294603831)
        if interact.channel == canal:
            if num1 % 2 == 0:
                res = 'par'
            else:
                res = 'impar'
            return await interact.followup.send(f'O número **{num1}** é **{res}**.')
        await interact.followup.send(f'Este comando não pode ser utilizado nesse canal. Utilize {canal.mention}') 

    @app_commands.command(name='inversor_string', description='Retorna um texto de trás para frente.')
    @app_commands.describe(texto='Digite o texto a ser invertido')
    async def inversor_string(self, interact:discord.Interaction, texto:str):
        await interact.response.defer(thinking=True, ephemeral=True)
        guild = interact.guild
        canal = guild.get_channel(1436359098294603831)
        if interact.channel == canal:
            txtchar = list(texto)
            i = len(txtchar)-1
            lista = []
            while i >= 0:
                lista.append(txtchar[i])
                i -= 1
            listastr = "".join(lista)
            return await interact.followup.send(f'**Texto invertido**: {listastr}') 
        await interact.followup.send(f'Este comando não pode ser utilizado nesse canal. Utilize {canal.mention}') 

    @app_commands.command(name='celsius_fahrenheit', description='Converte uma temperatura de Celsius para Fahrenheit.')
    @app_commands.describe(celsius='Digite uma temperatura em Celsius.')
    async def celsius_fahrenheit(self, interact:discord.Interaction, celsius:float):
        await interact.response.defer(thinking=True, ephemeral=True)
        guild = interact.guild
        canal = guild.get_channel(1436359098294603831)
        if interact.channel == canal:
            fahrenheit = (celsius * (9 / 5)) + 32
            return await interact.followup.send(f'**{celsius}⁰C** correspondem a **{fahrenheit}⁰F**')  
        await interact.followup.send(f'Este comando não pode ser utilizado nesse canal. Utilize {canal.mention}')  

    @app_commands.command(name='fahrenheit_celsius', description='Converte uma temperatura de Fahrenheit para Celsius.')
    @app_commands.describe(fahrenheit='Digite uma temperatura em Fahrenheit.')
    async def fahrenheit_celsius(self, interact:discord.Interaction, fahrenheit:float):
        await interact.response.defer(thinking=True, ephemeral=True)
        guild = interact.guild
        canal = guild.get_channel(1436359098294603831)
        if interact.channel == canal:
            celsius = (fahrenheit -32) / 1.8
            return await interact.followup.send(f'**{fahrenheit}⁰F** correspondem a **{celsius}⁰C**')
        await interact.followup.send(f'Este comando não pode ser utilizado nesse canal. Utilize {canal.mention}')   

    @app_commands.command(name='abrir_ticket', description='Abre um ticket para relatar um problema')
    @app_commands.describe(assunto='Digite o assunto do seu ticket.')
    async def abrir_ticket(self, interact:discord.Interaction, assunto:str):
        await interact.response.defer(thinking=True, ephemeral=True)
        guild = interact.guild
        titulo = f'📢-ticket-{interact.user.name}'
        channels = guild.channels
        for channel in channels:
            if channel.name == titulo:
                return await interact.followup.send('Você já possui um ticket em aberto.', ephemeral=True)
        categoria = ''
        for category in guild.categories:
            if category.name == '📢 Suporte':
                categoria = category
        overwrite = { #Sobrescreve as permissões padrão de usuários e cargos padrões
            guild.default_role: discord.PermissionOverwrite(read_messages=False, view_channel=False, send_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True, view_channel=True, send_messages=True, attach_files=True),
            guild.get_role(1436841614252441620): discord.PermissionOverwrite(read_messages=True,view_channel=True, send_messages=True, attach_files=True),
            interact.user: discord.PermissionOverwrite(view_channel=True, read_messages=True, send_messages=True, attach_files=True)
        }
        canal = await guild.create_text_channel(name=f'{titulo}', category=categoria, overwrites=overwrite)
        await canal.send(f'{titulo}\n\n**Assunto**: {assunto}\n\nEm breve um {guild.get_role(1436841614252441620).mention} entrará em contato.')
        await interact.followup.send(f'✅ Ticket aberto com sucesso, verifique o canal {canal.mention} para acompanhar.', ephemeral=True)

    @app_commands.command(name='fechar_ticket', description='Encerra um ticket')
    async def fechar_ticket(self, interact:discord.Interaction):
        await interact.response.defer(thinking=True, ephemeral=True)
        guild = interact.guild
        cargo = guild.get_role(1436841614252441620)
        if cargo not in interact.user.roles:
            return interact.followup.send(f'Somente membros com permissão {cargo.mention} podem utilizar este comando.', ephemeral=True)
        #loop para determinar a categoria específica
        for category in guild.categories:
            if category.name == '📢 Suporte':
                categoria = category
        if interact.channel.category == categoria:       
            canal = interact.channel
            members = interact.channel.members
            #loop para pegar os membros do canal que não possuem cargo (o membro que abriu o ticket)
            for member in members:
                if cargo not in member.roles:
                    membro = member
            await canal.set_permissions(membro, send_messages=False, read_messages=True)
            return await interact.followup.send(f'✅ Ticket encerrado.')
        await interact.followup.send(f'⚠️ Este comando só pode ser utilizado em um canal da categoria {categoria.mention}', ephemeral=True)
        
async def setup(bot):
    await bot.add_cog(Utils(bot))