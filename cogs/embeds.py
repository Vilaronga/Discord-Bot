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
        
    @app_commands.command(name='criar_embed', description='Crie um embed personalizada.')
    async def criar_embed(self, interact:discord.Interaction):
        await interact.response.send_modal(Git_Modal())

############################################################################################################################################ Embed com modal (Formulário) - Somente para mais comodidade

## Modal é meio que um formulário (parecido com uma view), por isso utiliza-se o self.add_item(self.x), para adicionar o objeto dentro do objeto view (visualização).

class Git_Modal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title='Criar Embed', timeout=None) #super é uma função especial do python que permite chamar métodos da classe-pai, dentro da classe filha. Nesse casso ele chama o __init__ que está dentro da classe discord.ui.Modal
        
        self.titulo = discord.ui.TextInput(label='Titulo', placeholder='Digite o título do post', required=True, max_length=45)
        self.descricao = discord.ui.TextInput(label='Descrição', placeholder='Digite uma descrição do seu embed', required=True, style=discord.TextStyle.long)
        self.cor = discord.ui.TextInput(label=f'Cor - Cores em https://encurtador.com.br/BWfN', placeholder='Utilize o "Int value" da cor.', max_length=10)
        self.url = discord.ui.TextInput(label='URL - Imagem', placeholder='Digite um link de alguma imagem para seu Embed.')
        self.link = discord.ui.TextInput(label='URL', placeholder='Digite um link de redirecionamento para outro local se houver.')

        self.add_item(self.titulo)
        self.add_item(self.descricao)
        self.add_item(self.cor)
        self.add_item(self.url)
        self.add_item(self.link)

    async def on_submit(self, interact:discord.Interaction):
        try:
            embed = discord.Embed()
            embed.title = self.titulo.value.title()
            embed.set_author(name=interact.user.name)
            embed.description = self.descricao.value.lower().capitalize()
            embed.set_image(url=self.url.value)
            embed.set_thumbnail(url=interact.user.avatar)
            embed.set_footer(text='Embed gerado com sucesso.')
            cor = int(self.cor.value.strip())
            embed.color = cor

            #botão
            if self.link.value:
                botao = discord.ui.Button(label='Saiba mais', style=discord.ButtonStyle.link, url=self.link.value)
                view = discord.ui.View()
                view.add_item(botao)
                await interact.response.send_message(embed=embed, view=view)
        
        except discord.HTTPException as link_invalido:
            await interact.response.send_message(f'Infelizmente o link fornecido não é válido. Tente novamente!', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Embeds(bot))