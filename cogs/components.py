import discord
from discord import app_commands, ui
from discord.ext import commands

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