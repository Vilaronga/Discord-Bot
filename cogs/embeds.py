import discord
from discord import app_commands, Embed
from discord.ext import commands

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

class Embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

############################################################################################################################################ Embed normal

    @app_commands.command(name='aaaaaaa', description='Divulge o seu GitHub')
    @app_commands.describe(seu_nome='Digite o seu nome. Ele ficará como título do post.', url_github='Digite a URL do seu GitHub. https://github.com/seu_nome', descricao='Digite uma descrição para o seu post.')
    async def aaaaaa(self, interact:discord.Interaction, seu_nome:str, url_github:str, descricao:str):
        try:
            embed = discord.Embed()
            embed.set_author(name=f'@{interact.user.name}')
            embed.title = seu_nome.lower().title()
            embed.description = descricao.lower().capitalize()
            imagem = discord.File('cogs/images/github_logo_black.png', 'github_logo_black.png') #a busca pelo file sempre deve partir do diretório do arquivo main.py
            embed.set_image(url='attachment://github_logo_black.png')
            embed.set_thumbnail(url=f'{interact.user.avatar}')
            embed.set_footer(text='Divulgação GitHub')
            embed.color = 16777215

            #botão
            botao = discord.ui.Button(label='GitHub', style=discord.ButtonStyle.link, url=url_github)
            view = discord.ui.View()
            view.add_item(botao)
    
            await interact.response.defer(ephemeral=True)
            await interact.followup.send(embed=embed, file=imagem, view=view)
        except discord.HTTPException as link_invalido:
            await interact.response.send_message(f'Infelizmente o link fornecido não é válido. Tente novamente!', ephemeral=True)
        
    @app_commands.command(name='aaaaaaaaaaaaaa', description='Divulgue seus projetos do GitHub.')
    async def aaaa(self, interact:discord.Interaction):
        await interact.response.send_modal(Git_Modal())

############################################################################################################################################ Embed com modal (Formulário) - Somente para mais comodidade

## Modal é meio que um formulário que faz parte de uma view, por isso utiliza-se o self.add_item(self.x), para adicionar dentro da view (visualização).

class Git_Modal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title='Publicar Git', timeout=None) #super é uma função especial do python que permite chamar métodos da classe-pai, dentro da classe filha. Nesse casso ele chama o __init__ que está dentro da classe discord.ui.Modal
        
        self.nome = discord.ui.TextInput(label='Nome', placeholder='Digite seu nome aqui', max_length=30)
        self.url_github = discord.ui.TextInput(label='URL GitHub', placeholder='https://github.com/seu_nome', max_length=80)
        self.sobre = discord.ui.TextInput(label='Conte-nos um pouco sobre você.', required=True, style=discord.TextStyle.long)

        self.add_item(self.nome)
        self.add_item(self.url_github)
        self.add_item(self.sobre)

    async def on_submit(self, interact:discord.Interaction):
        try:
            embed = discord.Embed()
            embed.title = self.nome.value.title()
            embed.set_author(name=interact.user.name)
            embed.description = self.sobre.value.lower().capitalize()
            imagem = discord.File('cogs/images/github_logo_black.png', 'github_logo_black.png') #a busca pelo file sempre deve partir do diretório do arquivo main.py
            embed.set_image(url='attachment://github_logo_black.png')
            embed.set_thumbnail(url=interact.user.avatar)
            embed.set_footer(text='Divulgação GitHub')
            embed.color = 16777215

            #botão
            botao = discord.ui.Button(label='GitHub', style=discord.ButtonStyle.link, url=self.url_github.value)
            view = discord.ui.View()
            view.add_item(botao)
            await interact.response.send_message(embed=embed, file=imagem, view=view)
        
        except discord.HTTPException as link_invalido:
            await interact.response.send_message(f'Infelizmente o link fornecido não é válido. Tente novamente!', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Embeds(bot))