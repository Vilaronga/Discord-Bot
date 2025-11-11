import discord
from discord.ext import commands
from discord import app_commands
import requests
import os
from dotenv import load_dotenv
from database.models import *
from database.db_connection import sessaoAtual

#Autorização de acesso à api github
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} #O GitHub exige um header de autenticação para acessar a api com token. o "Autorization indica o tipo de autenticação, nesse caso é do tipo token e logo em seguida é informado o token. Todos os dados são retornado  em .json"

class GitHubIntegração(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ===============================================
    # /commits - mostra os commits mais recentes
    # ===============================================
    @app_commands.command(name="commits", description="Mostra os commits mais recentes de um repositório.")
    async def commits(self, interaction: discord.Interaction, usuario: str, repositorio: str):
        url = f"https://api.github.com/repos/{usuario}/{repositorio}/commits"
        resposta = requests.get(url, headers=HEADERS)

        if resposta.status_code != 200:
            await interaction.response.send_message("❌ Repositório não encontrado ou erro na API do GitHub.", ephemeral=True)
            return

        commits = resposta.json()
        if not commits:
            await interaction.response.send_message("⚠️ Nenhum commit encontrado.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"Últimos commits em {usuario}/{repositorio}",
            color=discord.Color.green()
        )

        for commit in commits[:5]:  # mostra os 5 mais recentes
            autor = commit["commit"]["author"]["name"]
            mensagem = commit["commit"]["message"]
            data = commit["commit"]["author"]["date"]
            url_commit = commit["html_url"]

            embed.add_field(
                name=f"🧑 {autor} — {data[:10]}",
                value=f"[{mensagem}]({url_commit})",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

    # ===============================================
    # /pushs - mostra quem fez pushs recentes
    # ===============================================
    @app_commands.command(name="pushs", description="Mostra quem enviou pushs recentes para o repositório.")
    async def pushs(self, interaction: discord.Interaction, usuario: str, repositorio: str):
        url = f"https://api.github.com/repos/{usuario}/{repositorio}/events"
        resposta = requests.get(url, headers=HEADERS)

        if resposta.status_code != 200:
            await interaction.response.send_message("❌ Erro ao buscar eventos do repositório.", ephemeral=True)
            return

        eventos = resposta.json()
        pushs = [e for e in eventos if e["type"] == "PushEvent"]

        if not pushs:
            await interaction.response.send_message("⚠️ Nenhum push recente encontrado.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"Últimos pushs em {usuario}/{repositorio}",
            color=discord.Color.blurple()
        )

        for push in pushs[:5]:
            autor = push["actor"]["login"]
            commits = push["payload"].get("commits", [])
            qtd_commits = len(commits)
            data = push["created_at"]

            embed.add_field(
                name=f"📤 {autor}",
                value=f"{qtd_commits} commit(s) — {data[:10]}",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

    # ===============================================
    # /issues - lista as issues abertas
    # ===============================================
    @app_commands.command(name="issues", description="Lista as issues abertas de um repositório.")
    async def issues(self, interaction: discord.Interaction, usuario: str, repositorio: str):
        url = f"https://api.github.com/repos/{usuario}/{repositorio}/issues"
        resposta = requests.get(url, headers=HEADERS)

        if resposta.status_code != 200:
            await interaction.response.send_message("❌ Erro ao buscar issues.", ephemeral=True)
            return

        issues = resposta.json()
        if not issues:
            await interaction.response.send_message("⚠️ Nenhuma issue aberta encontrada.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"Issues abertas em {usuario}/{repositorio}",
            color=discord.Color.orange()
        )

        for issue in issues[:5]:
            titulo = issue["title"]
            autor = issue["user"]["login"]
            url_issue = issue["html_url"]
            embed.add_field(name=f"🧩 {titulo}", value=f"Por {autor} — [Ver Issue]({url_issue})", inline=False)

        await interaction.response.send_message(embed=embed)
    





    @app_commands.command(name='github', description='Verifica o GitHub de algum usuário.')
    async def github(self, interact:discord.Interaction, usuario:discord.Member):
        discord_id = usuario.id
        sessao = sessaoAtual()
        possui_github = (sessao.query(Usuario).filter(Usuario.discord_id == discord_id)).first()
        if possui_github:
            url = possui_github.github_url
            url_formatada = url.rstrip('/').split('/')
            github_nome = url_formatada[-1]
            api = f"https://api.github.com/users/{github_nome}"
            requisicao = requests.get(api)
            dados = requisicao.json()
            nome = dados.get("name")
            desc = dados.get("bio")
            foto = dados.get("avatar_url")
            link = dados.get("html_url")
            num_repos = dados.get("public_repos")

            embed = discord.Embed()
            embed.set_author(name=f'@{interact.user.name}')
            embed.title = nome
            embed.description = desc
            imagem = discord.File('cogs/images/github_logo_black.png', 'github_logo_black.png') 
            embed.set_image(url='attachment://github_logo_black.png')
            embed.set_thumbnail(url=foto)
            embed.set_footer(text=f'Repositórios públicos: {num_repos}')
            embed.color = 16777215

            #botão
            botao = discord.ui.Button(label='GitHub', style=discord.ButtonStyle.link, url=link)
            view = discord.ui.View()
            view.add_item(botao)
    
            await interact.response.defer(ephemeral=True)
            await interact.followup.send(embed=embed, file=imagem, view=view)
        else:
            await interact.response.send_message('O usuário não possui GitHub vinculado.', ephemeral=True)

            






    ######################################################################################################################################################## Modals:

    @app_commands.command(name='registrar_repositorio', description='Registra um repositório ao banco de dados.')
    async def rep_register(self, interact:discord.Interaction):
        await interact.response.send_modal(RegistrarRep_Modal())

    @app_commands.command(name='vincular_github', description='Vincula o GitHub ao seu perfil do Discord')
    async def vincular_github(self, interact:discord.Interaction):
        await interact.response.send_modal(VincularGit_Modal())

class VincularGit_Modal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title='Vincular GitHub', timeout=None)

        self.url = discord.ui.TextInput(label='url', placeholder='Digite a URL do seu GitHub.')
        self.add_item(self.url)

    async def on_submit(self, interact:discord.Interaction):
        sessao = sessaoAtual() #Abre uma sessão do banco de dados
        usuario_existe = (sessao.query(Usuario).filter(Usuario.github_url == self.url.value)).first()
        if usuario_existe:
            await interact.response.send_message(f'Você já vinculou uma URL ou a URL já está em uso')  
            return
        dados = Usuario(discord_id=interact.user.id, github_url=self.url.value)       #salva o id do discord do usuário e o link do github
        sessao.add(dados)                                                             #adiciona o id e a url no banco de dados               
        sessao.commit()                                                                 #faz o commit das alterações
        sessao.close()                                                                  #salva as alterações
        await interact.response.send_message(f'{interact.user.mention}, o seu GitHub agora está vinculado à sua conta do discord. Digite /github e selecione um usuário para verificar seu GitHub.')
            
class RegistrarRep_Modal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title='Registrar Repositório', timeout=None)

        self.url = discord.ui.TextInput(label='Repositório', placeholder='Digite o URL do repositório.')
        self.add_item(self.url)

    async def on_submit(self, interact:discord.Interaction):
        formatacao = self.url.value.rstrip('/').split('/')
        repositorio = formatacao[-1]
        dono_repositorio = formatacao[-2]
        sessao = sessaoAtual()                                                          #Abre uma sessão do banco de dados
        repo_existe = (sessao.query(Repositorios).filter(Repositorios.repo_url == self.url.value)).first()
        if repo_existe:
            await interact.response.send_message(f'Este repositório já está registrado.')  
            return
        dados= Repositorios(repo_url = self.url.value, repo_nome=repositorio, repo_dono=dono_repositorio)                                  #salva o id do discord do usuário e o link do github
        sessao.add(dados)                                                               #adiciona o id e a url no banco de dados               
        sessao.commit()                                                                 #faz o commit das alterações
        sessao.close()                                                                  #salva as alterações
        await interact.response.send_message(f'{interact.user.mention}, o repositório {self.url.value} foi registrado com sucesso.')

##########################################################################################################################################################
async def setup(bot):
    await bot.add_cog(GitHubIntegração(bot))
