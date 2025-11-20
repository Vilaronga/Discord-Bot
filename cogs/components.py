import discord
from discord import app_commands, ui
from discord.ext import commands

# Esta classe representa apenas um modelo base de um LayoutView que utiliza um recurso do discord chamado Components v2. O LayoutView nos permite ter maior controle de personalização da resposta quando em comparação com os outros tipos (embeds, respostas comuns...)

class Components(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='teste_layoutview', description='teste')
    async def layout_view(self, interact:discord.Interaction):
        layout = LayoutView()
        arquivos = [
            discord.File('cogs/images/github_logo_black.png', 'github_logo_black.png'),
            discord.File('cogs/documentos/Curriculo_LucasVilarongadeLima.pdf', 'Curriculo_LucasVilarongadeLima.pdf')
            ]
        await interact.response.send_message(view=layout, files=arquivos)

    @app_commands.command(name='ajuda', description='Exibe uma ajuda com todos os comandos do servidor.')
    async def ajuda(self, interact:discord.Interaction):
        await interact.response.defer(thinking=True, ephemeral=True)
        guild = interact.guild
        layout = Layout_Ajuda(guild)
        file = discord.File('cogs/images/bot.png', 'bot.png')
        await interact.followup.send(view=layout, file=file)

class LayoutView(ui.LayoutView):
    def __init__(self):
        super().__init__()

        #criação do container
        container = ui.Container(ui.TextDisplay('Esse é um componente de texto.'))
        container.accent_color = discord.Colour.yellow()
        container.spoiler = True
        container.add_item(ui.Separator(visible=True, spacing=discord.SeparatorSpacing.large))
        container.add_item(ui.TextDisplay('Teste linha 2')) #O textdisplay suporta markdown, então é possível editar estilos pelo próprio parâmetro.

        #botões com resposta - somente podem ser utilizado até 5 botões em uma actionrow, sendo que nenhum deve ser duplicado
        botao2 = ui.Button(label="olá") #cria um botão
        botao2.callback = self.botao2   #chama a respostas do botão
    
        botao22 = ui.Button(label="olá")
        botao22.callback = self.botao2
        
        botao222 = ui.Button(label="olá")
        botao222.callback = self.botao2

        linha_botoes = ui.ActionRow(botao2, botao22, botao222)

        #botões em sessão: Permite colocar um conteúdo junto com um botão ao lado.
        botao = ui.Button(label='Clique aqui', style=discord.ButtonStyle.link, url='https://github.com')
        botaosessao = ui.Section(ui.TextDisplay('Teste botão'), accessory=botao) #Coloca um botão ao lado de um texto

        #menu de selecao
        selecao = ui.Select(placeholder='Selecione uma opção', options=[
            discord.SelectOption(label='Opção 1', value='1'),
            discord.SelectOption(label='Opção 2', value='2')
        ])
        selecao.callback = self.resposta_selecao #chama a resposta da seleção
        linha_selecao = ui.ActionRow(selecao)
        
        #imagens
        imagem_github = ui.Thumbnail('attachment://github_logo_black.png') #essa imagem deve ser enviada no comando que chama esse componente através de discord.File('local da imagem', 'nome da imagem'). E aqui dentro deve-se apenas fazer a referência a ela. Pra cada imagem diferente deve-se fazer um envio através do comando que cria o componente.
        imagem_sessesao = ui.Section(ui.TextDisplay('# Imagem _nessa_ seção.'), accessory=imagem_github)

        ## Galeria de imagens
        galeria = ui.MediaGallery()  #limite de 10 imagens
        galeria.add_item(media='attachment://github_logo_black.png')
        galeria.add_item(media='attachment://github_logo_black.png')
        galeria.add_item(media='attachment://github_logo_black.png')
        galeria.add_item(media='attachment://github_logo_black.png')
        galeria.add_item(media='attachment://github_logo_black.png')
        galeria.add_item(media='attachment://github_logo_black.png')
        galeria.add_item(media='attachment://github_logo_black.png')
        galeria.add_item(media='attachment://github_logo_black.png')
        galeria.add_item(media='attachment://github_logo_black.png')
        galeria.add_item(media='attachment://github_logo_black.png')

        #arquivos
        curriculo = ui.File(media='attachment://Curriculo_LucasVilarongadeLima.pdf')

        #adicionando tudo ao container
        container.add_item(botaosessao)  #adiciona a sessão ao container
        container.add_item(linha_botoes) #adiciona o actionrow ao container
        container.add_item(linha_selecao)
        container.add_item(imagem_sessesao)
        container.add_item(galeria)
        container.add_item(curriculo)
        self.add_item(container)

    async def botao2(self, interact:discord.Interaction):
        await interact.response.send_message(f'Olá, {interact.user.mention}')

    async def resposta_selecao(self, interact:discord.Interaction):
        escolha = interact.data['values'][0]
        await interact.response.send_message(f'Você selecionou {escolha}')

async def setup(bot):
    await bot.add_cog(Components(bot))

############################################################ Layout Ajuda #####################################################################
class Layout_Ajuda(ui.LayoutView):
    def __init__(self, guild:discord.Interaction.guild):
        super().__init__()

        comandos = guild.get_channel(1436359098294603831)
        matematica = guild.get_channel(1436390421352939611)
        gemini = guild.get_channel(1437634502389141524)
        github = guild.get_channel(1437979512624123955)
        commits = guild.get_channel(1437979541510557706)
        pushs = guild.get_channel(1437979830707814561)
        issues = guild.get_channel(1437979851146530938)
        branches = guild.get_channel(1440948751496646726)

        #criação do container
        container = ui.Container()
        container.accent_color = discord.Colour.blue()

        imagem_bot = ui.Thumbnail('attachment://bot.png')
        container.add_item(ui.Section(ui.TextDisplay(f'# Painel de ajuda - Comandos.'), accessory=imagem_bot))
        container.add_item(ui.Separator(visible=True, spacing=discord.SeparatorSpacing.large))
        container.add_item(ui.TextDisplay('### Logo abaixo estão todos os comandos do Bot seguindo a seguinte estrutura:\n\n**Canal em que o comando pode ser utilizado**\n**/comando**: "O que o comando faz."\n**Usuários que podem utilizar**.')) 
        container.add_item(ui.Separator(visible=False, spacing=discord.SeparatorSpacing.large))
        container.add_item(ui.TextDisplay(f'**Canal**: {comandos.mention}')) 
        container.add_item(ui.TextDisplay('**/par_ou_impar**: Verifica se o número fornecido é par ou ímpar.\n**/inversor_string**: Inverte um texto (de trás para frente).\n**/celsius_fahrenheit**: Converte uma temperatura de Celsius para Fahrenheit.\n**/fahrenheit_celsius**: Converte uma temperatura de Fahrenheit para Celsius.'))   
        container.add_item(ui.Separator(visible=False, spacing=discord.SeparatorSpacing.large)) 
        container.add_item(ui.TextDisplay(f'**Canal**: {matematica.mention}')) 
        container.add_item(ui.TextDisplay('**/somar**: Realiza a soma entre 2 números\n**/subtrair**: Realiza a subtração entre 2 números.\n**/multiplicar**: Realiza a multiplicação entre 2 números.\n**/dividir**: Realiza a divisão entre 2 números (de trás para frente).'))
        container.add_item(ui.Separator(visible=False, spacing=discord.SeparatorSpacing.large)) 
        container.add_item(ui.TextDisplay(f'**Canal**: {gemini.mention}'))   
        container.add_item(ui.TextDisplay('**/gemini**: Faz uma pergunta ao gemini 2.5-Flash.')) 
        container.add_item(ui.Separator(visible=False, spacing=discord.SeparatorSpacing.large))  
        container.add_item(ui.TextDisplay(f'**Canal**: {github.mention}'))   
        container.add_item(ui.TextDisplay(f'**/vincular_github**: Vincula um perfil do github ao seu usuário do discord.\n**/registrar_repositorio**: Salva um repositório no banco de dados do Bot.\n**Apenas {guild.get_role(1436841614252441620).mention}**.\n\n**/remover_repositorio**: Remove um repositório do banco de dados.\n**Apenas {guild.get_role(1436841614252441620).mention}**.\n\n**/abrir_issue**: Permite a abertura de issues no repositório selecionado.'))  
        container.add_item(ui.Separator(visible=False, spacing=discord.SeparatorSpacing.large))  
        container.add_item(ui.TextDisplay(f'**Canal**: {commits.mention}'))   
        container.add_item(ui.TextDisplay('**/commits**: Mostra os 5 últimos commits de um repositório selecionado.'))  
        container.add_item(ui.Separator(visible=False, spacing=discord.SeparatorSpacing.large)) 
        container.add_item(ui.TextDisplay(f'**Canal**: {pushs.mention}'))   
        container.add_item(ui.TextDisplay('**/pushs**: Mostra os 5 últimos pushs de um repositório selecionado.'))  
        container.add_item(ui.Separator(visible=False, spacing=discord.SeparatorSpacing.large)) 
        container.add_item(ui.TextDisplay(f'**Canal**: {issues.mention}'))   
        container.add_item(ui.TextDisplay('**/issues**: Mostra as 5 últimas issues abertas de um repositório selecionado.'))  
        container.add_item(ui.Separator(visible=False, spacing=discord.SeparatorSpacing.large)) 
        container.add_item(ui.TextDisplay(f'**Canal**: {branches.mention}'))   
        container.add_item(ui.TextDisplay('**/branches**: Mostra as branches de um repositório selecionado.'))  
        container.add_item(ui.Separator(visible=False, spacing=discord.SeparatorSpacing.large)) 
        container.add_item(ui.TextDisplay(f'**Canal**: Qualquer canal'))     
        container.add_item(ui.TextDisplay(f'**/ola**: Responde com um Olá para o usuário.\n**/abrir_ticket**: Cria um canal de suporte para atender a uma dúvida ou problema.\n**/fechar_ticket**: Encerra um ticket aberto.\n**Apenas {guild.get_role(1436841614252441620).mention}**.'))    
        self.add_item(container)

async def setup(bot):
    await bot.add_cog(Components(bot))