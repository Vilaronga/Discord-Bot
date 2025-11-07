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

    @app_commands.command(name='github', description='Divulge o seu GitHub')
    async def github(self, interact:discord.Interaction, seu_nome:str, url_github:str, descricao:str):
        embed = discord.Embed()
        embed.set_author(name=f'@{interact.user.name}')
        embed.title = seu_nome.title()
        embed.description = descricao.lower().capitalize()
        imagem = discord.File('cogs/images/github_logo_black.png', 'github_logo_black.png')
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

async def setup(bot):
    await bot.add_cog(Embeds(bot))