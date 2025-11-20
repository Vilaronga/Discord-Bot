import discord
from discord.ext import commands
from discord import app_commands, ui
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

    ######################################################################################################################################################## Métodos

    async def get_repos(self, interaction:discord.Interaction, current:str):
        sessao = sessaoAtual()
        repos = sessao.query(Repositorios).all()
        escolhas = []
        for repo in repos:
            escolhas.append(
                app_commands.Choice(name=f'📁 {repo.repo_nome}', value=str(repo.repo_url))
            )
        sessao.close()
        return escolhas
    
    ######################################################################################################################################################## Comandos
    '''
    #Comando /commits
    @app_commands.command(name="commits_v1", description="Mostra os commits mais recentes do repositório selecionado.")
    @app_commands.autocomplete(repositorio=get_repos)
    async def commits_v1(self, interaction:discord.Interaction, repositorio:str):
        url_formada = repositorio.rstrip('/').split('/')
        repo_dono = url_formada[-2]
        repo_nome = url_formada[-1]
        api = f"https://api.github.com/repos/{repo_dono}/{repo_nome}/commits"
        resposta = requests.get(api, headers=HEADERS)
        commits = resposta.json()

        if not commits:
            await interaction.response.send_message("⚠️ Nenhum commit encontrado.", ephemeral=True)

        embed = discord.Embed()
        embed.title=f'Últimos 5 commits em {repo_dono}/{repo_nome}'
        embed.color=16777215
        embed.set_footer(text='Dados obtidos via GitHub API.')

        for commit in commits[:5]:                      # mostra os 5 commits mais recentes
            autor = commit["commit"]["author"]["name"]
            mensagem = commit["commit"]["message"]
            data = commit["commit"]["author"]["date"]
            url_commit = commit["html_url"]

            embed.add_field(name=f"🔃 {autor} — {data[:10]}", value=f"[{mensagem}]({url_commit})", inline=False)

        botao = discord.ui.Button(label='Todos os commits', style=discord.ButtonStyle.link, url=f'https://github.com/{repo_dono}/{repo_nome}/commits')
        view = discord.ui.View()
        view.add_item(botao)

        await interaction.response.send_message(embed=embed, view=view)

    #Comando /pushs
    @app_commands.command(name="pushs_v1", description="Mostra quem enviou pushs recentes para o repositório selecionado.")
    @app_commands.autocomplete(repositorio=get_repos)
    async def pushs_v1(self, interaction: discord.Interaction, repositorio: str):
        url_formada = repositorio.rstrip('/').split('/')
        repo_dono = url_formada[-2]
        repo_nome = url_formada[-1]
        api = f"https://api.github.com/repos/{repo_dono}/{repo_nome}/events"
        resposta = requests.get(api, headers=HEADERS)
        eventos = resposta.json()
        pushs = []                             #criação de lista que irá armazenar todos os pushs
        for push in eventos:                   #loop para verificar se o tipo de evento foi um push, se sim ele armazena na lista pushs[]
            if push["type"] == "PushEvent":
                pushs.append(push)

        if not pushs:
            await interaction.response.send_message("⚠️ Nenhum push recente encontrado.", ephemeral=True)

        embed = discord.Embed()
        embed.title=f"Últimos 5 pushs em {repo_dono}/{repo_nome}"
        embed.color=16777215
        embed.set_footer(text='Dados obtidos via GitHub API.')

        for push in pushs[:5]:
            autor = push["actor"]["login"]
            pushid = push["payload"]["push_id"]
            data = push["created_at"]
            embed.add_field(name=f"📤 {autor} — {data[:10]}", value=f"Id do push: {pushid}.", inline=False)

        botao = discord.ui.Button(label='Insights', style=discord.ButtonStyle.link, url=f'https://github.com/{repo_dono}/{repo_nome}/pulse')
        view = discord.ui.View()
        view.add_item(botao)

        await interaction.response.send_message(embed=embed, view=view)

   #Comando /issues
    @app_commands.command(name="issues_v1", description="Lista as 5 últimas issues abertas do repositório selecionado.")
    @app_commands.autocomplete(repositorio=get_repos)
    async def issues_v1(self, interaction:discord.Interaction, repositorio:str):
        url_formada = repositorio.rstrip('/').split('/')
        repo_dono = url_formada[-2]
        repo_nome = url_formada[-1]
        api = f"https://api.github.com/repos/{repo_dono}/{repo_nome}/issues"
        resposta = requests.get(api, headers=HEADERS)
        issues = resposta.json()

        if not issues:
            await interaction.response.send_message("✅ Nenhuma issue aberta encontrada.", ephemeral=True)

        embed = discord.Embed()
        embed.title=f"Últimas 5 issues abertas em {repo_dono}/{repo_nome}"
        embed.color= 16777215
        embed.set_footer(text='Dados obtidos via GitHub API.')

        for issue in issues[:5]:
            titulo = issue["title"]
            autor = issue["user"]["login"]
            url_issue = issue["html_url"]
            data = issue["created_at"]
            embed.add_field(name=f"📋Por {autor} — {data[:10]}", value=f"[{titulo}]({url_issue})", inline=False)
        
        botao = discord.ui.Button(label='Todos as issues', style=discord.ButtonStyle.link, url=f'https://github.com/{repo_dono}/{repo_nome}/issues')
        view = discord.ui.View()
        view.add_item(botao)

        await interaction.response.send_message(embed=embed, view=view)
    
    #comando /branches
    @app_commands.command(name='branches_v1', description='Verifica as branches de um repositório selecionado.')
    @app_commands.autocomplete(repositorio=get_repos)
    async def branches_v1(self, interact:discord.Interaction, repositorio:str):
        url_formatada = repositorio.rstrip('/').split('/')
        repo_dono = url_formatada[-2]
        repo_nome = url_formatada[-1]
        api = f'https://api.github.com/repos/{repo_dono}/{repo_nome}/branches'
        resposta = requests.get(api, headers=HEADERS)
        branches = resposta.json()

        embed = discord.Embed()
        embed.title = f'Branches criadas em {repo_dono}/{repo_nome}'
        embed.color = 16777215
        embed.set_footer(text='Dados obtidos via GitHub API.')

        for branch in branches:
            nome = branch["name"]
            sha = branch["commit"]["sha"]
            embed.add_field(name=f'🌱 Branch: {nome}', value=f'SHA do último commit: {sha}', inline=False)

        botao = discord.ui.Button(label='Todas as Branches', style=discord.ButtonStyle.link, url=f'https://github.com/{repo_dono}/{repo_nome}/branches')
        view = discord.ui.View()
        view.add_item(botao)

        await interact.response.send_message(embed=embed, view=view)
    '''

    #comando /detalhes_repositorio
    @app_commands.command(name='detalhes_repositorio', description='Verifica os detalhes de um repositório selecionado.')
    @app_commands.autocomplete(repositorio=get_repos)
    async def detalhes(self, interact:discord.Interaction, repositorio:str):
        url_formatada = repositorio.rstrip('/').split('/')
        repo_dono = url_formatada[-2]
        repo_nome = url_formatada[-1]
        api = f'https://api.github.com/repos/{repo_dono}/{repo_nome}'
        resposta = requests.get(api, headers=HEADERS)
        detalhes = resposta.json()

        embed = discord.Embed()
        embed.set_author(name=detalhes["owner"]["login"])
        embed.set_thumbnail(url=detalhes["owner"]["avatar_url"])
        embed.title = f'Detalhes: {repo_dono}/{repo_nome}'
        embed.color = 16777215
        embed.set_footer(text='Dados obtidos via GitHub API.')
        embed.description = detalhes["description"]
        embed.add_field(name='', value='', inline=False)
        embed.add_field(name=f'🖥️ Linguagem principal:', value=f'{detalhes["language"]}', inline=True)
        embed.add_field(name=f'⭐ Avaliações:', value=f'{detalhes["stargazers_count"]} avaliações.', inline=True)
        embed.add_field(name=f'👁️ Visibilidade:', value=f'{detalhes["visibility"]}', inline=True)
        embed.add_field(name=f'⛓️‍💥 Forks:', value=f'{detalhes["forks"]}', inline=True)
        embed.add_field(name=f'📋 Issues abertas:', value=f'{detalhes["open_issues_count"]}', inline=True)
        embed.add_field(name=f'🔑 Licença:', value=f'{detalhes["license"]["name"]}', inline=True)

        botao = discord.ui.Button(label='Projeto completo', style=discord.ButtonStyle.link, url=f'https://github.com/{repo_dono}/{repo_nome}')
        view = discord.ui.View()
        view.add_item(botao)

        await interact.response.send_message(embed=embed, view=view)

    #comando /github
    @app_commands.command(name='github', description='Verifica o GitHub de algum usuário.')
    async def github(self, interact:discord.Interaction, usuario:discord.Member):
        discord_id = usuario.id
        sessao = sessaoAtual()
        possui_github = (sessao.query(Usuario).filter(Usuario.discord_id == discord_id)).first()
        if possui_github:
            url = possui_github.github_url
            url_formatada = url.rstrip('/').split('/') #remove a última barra se houver, assim como divide a string em substrings com base no carctere '/'. O [-1] retorna o ultimo elemento da lista. [-2] retornaria o penultimo e assim por diante.
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
            embed.add_field(name=f'Repositórios públicos: {num_repos}', value='', inline=True)
            embed.color = 16777215
            embed.set_footer(text='Dados obtidos via GitHub API.')

            #botão
            botao = discord.ui.Button(label='GitHub', style=discord.ButtonStyle.link, url=link)
            view = discord.ui.View()
            view.add_item(botao)
            sessao.close()
            await interact.response.defer(ephemeral=True)
            await interact.followup.send(embed=embed, file=imagem, view=view)
        else:
            await interact.response.send_message('O usuário não possui GitHub vinculado.', ephemeral=True)

    ######################################################################################################################################################### 
    # Modals:

    #comando /registrar_repositorio
    @app_commands.command(name='registrar_repositorio', description='Registra um repositório ao banco de dados.')
    async def rep_register(self, interact:discord.Interaction):
        guild = interact.guild
        adm = guild.get_role(1436841614252441620)
        channel = guild.get_channel(1437979512624123955)
        if adm in interact.user.roles and interact.channel_id == channel:
            await interact.response.send_modal(RegistrarRep_Modal())
            return
        await interact.response.send_message(f'Somente um administrador pode utilizar esse comando ou está sendo enviado no chat errado, tente {guild.get_channel(1437979512624123955).mention}.', ephemeral=True)

    #comando /remover_repositorio
    @app_commands.command(name='remover_repositorio', description='Remove um repositório do banco de dados.')
    @app_commands.autocomplete(repositorio=get_repos)
    async def remover_repositorio(self, interact:discord.Interaction, repositorio:str):
        sessao = sessaoAtual()
        remover = sessao.query(Repositorios).filter(Repositorios.repo_url == repositorio).first()
        nome_repo = remover.repo_nome
        sessao.delete(remover)
        sessao.commit()
        sessao.close()
        await interact.response.send_message(f'O repositório 📁{nome_repo} foi excluido do banco de dados.')

    #comando /vincular_github
    @app_commands.command(name='vincular_github', description='Vincula seu GitHub ao seu perfil do Discord')
    async def vincular_github(self, interact:discord.Interaction):
        await interact.response.send_modal(VincularGit_Modal())
    
    #########################################################################################################
    #comando commits v2
    @app_commands.command(name='commits', description='Verifica os últimos 5 commits de um repositório.')
    @app_commands.autocomplete(repositorio=get_repos)
    async def commits(self, interact:discord.Interaction, repositorio:str):
        arquivos = [
            discord.File('cogs/images/github_70px.png', 'github_70px.png')
        ]
        url_formada = repositorio.rstrip('/').split('/')
        repo_dono = url_formada[-2]
        repo_nome = url_formada[-1]
        api = f"https://api.github.com/repos/{repo_dono}/{repo_nome}/commits"
        resposta = requests.get(api, headers=HEADERS)
        commits = resposta.json()

        titulo = f'\n{repo_dono}/{repo_nome}\nÚltimos 5 commits:'
        lista = []
        for commit in commits[:5]:                      # mostra os 5 commits mais recentes
            autor = commit["commit"]["author"]["name"]
            mensagem = commit["commit"]["message"]
            data = commit["commit"]["author"]["date"]
            url_commit = commit["html_url"]
            botao = ui.Button(label='Ver', style=discord.ButtonStyle.link, url= url_commit)
            lista.append(ui.Section(ui.TextDisplay(f'\n🔃 *{autor}* — _{data[:10]}_\n • **{mensagem}**'),accessory=botao))
            lista.append(ui.Separator(visible=False, spacing=discord.SeparatorSpacing.large))
        labelbotao = f'Todos os commits'
        layout = LayoutView(titulo, repositorio, labelbotao, lista)
        await interact.response.send_message(view=layout, files=arquivos)

    #comando branches v2
    @app_commands.command(name='branches', description='Verifica as branches de um repositório.')
    @app_commands.autocomplete(repositorio=get_repos)
    async def branches(self, interact:discord.Interaction, repositorio:str):
        arquivos = [
            discord.File('cogs/images/github_70px.png', 'github_70px.png')
        ]
        url_formada = repositorio.rstrip('/').split('/')
        repo_dono = url_formada[-2]
        repo_nome = url_formada[-1]
        api = f"https://api.github.com/repos/{repo_dono}/{repo_nome}/branches"
        resposta = requests.get(api, headers=HEADERS)
        branches = resposta.json()

        titulo = f'{repo_dono}/{repo_nome}\nLista de branchs existentes:'
        lista = []
        for branch in branches:
            nome = branch["name"]
            sha = branch["commit"]["sha"]
            url_commit = branch["commit"]["url"]
            botao = ui.Button(label='Ver', style=discord.ButtonStyle.link, url=url_commit)
            lista.append(ui.Section(ui.TextDisplay(f'🌱 Branch: *{nome}*\n • SHA do último commit: **{sha}**'), accessory=botao))
            lista.append(ui.Separator(visible=False, spacing=discord.SeparatorSpacing.large))
        labelbotao = f'Todas as branches'
        layout = LayoutView(titulo, repositorio, labelbotao, lista)
        await interact.response.send_message(view=layout, files=arquivos)

    #comando issues v2
    @app_commands.command(name='issues', description='Verifica as issues abertas de um repositório.')
    @app_commands.autocomplete(repositorio=get_repos)
    async def issues(self, interact:discord.Interaction, repositorio:str):
        arquivos = [
            discord.File('cogs/images/github_70px.png', 'github_70px.png')
        ]
        url_formada = repositorio.rstrip('/').split('/')
        repo_dono = url_formada[-2]
        repo_nome = url_formada[-1]
        api = f"https://api.github.com/repos/{repo_dono}/{repo_nome}/issues"
        resposta = requests.get(api, headers=HEADERS)
        issues = resposta.json()

        if not issues:
            await interact.response.send_message("✅ Nenhuma issue aberta encontrada.", ephemeral=True)

        titulo=f'{repo_dono}/{repo_nome}\nÚltimas 5 issues abertas:'
        lista = []
        for issue in issues[:5]:
            titulo_issue = issue["title"]
            autor = issue["user"]["login"]
            url_issue = issue["html_url"]
            data = issue["created_at"]
            botao = ui.Button(label='Ver', style=discord.ButtonStyle.link, url=url_issue)
            lista.append(ui.Section(ui.TextDisplay(f"📋Por *{autor}* — *{data[:10]}*\n • **{titulo_issue}**"), accessory=botao))
            lista.append(ui.Separator(visible=False, spacing=discord.SeparatorSpacing.large))
        labelbotao = f'Todas as issues'
        layout = LayoutView(titulo, repositorio, labelbotao, lista)
        await interact.response.send_message(view=layout, files=arquivos)

    #comando pushs v2
    @app_commands.command(name='pushs', description='Verifica os últimos 5 pushs de um repositório.')
    @app_commands.autocomplete(repositorio=get_repos)
    async def pushs(self, interact:discord.Interaction, repositorio:str):
        arquivos = [
            discord.File('cogs/images/github_70px.png', 'github_70px.png')
        ]
        url_formada = repositorio.rstrip('/').split('/')
        repo_dono = url_formada[-2]
        repo_nome = url_formada[-1]
        api = f"https://api.github.com/repos/{repo_dono}/{repo_nome}/events"
        resposta = requests.get(api, headers=HEADERS)
        eventos = resposta.json()
        pushs = []                             
        for push in eventos:                   
            if push["type"] == "PushEvent":
                pushs.append(push)

        if not pushs:
            await interact.response.send_message("✅ Nenhuma issue aberta encontrada.", ephemeral=True)

        titulo=f'{repo_dono}/{repo_nome}\nÚltimos 5 pushs:'
        lista = []
        for push in pushs[:5]:
            autor = push["actor"]["login"]
            pushid = push["payload"]["push_id"]
            data = push["created_at"]
            head = push["payload"]["head"]
            before = push["payload"]["before"]
            lista.append(ui.TextDisplay(f"📤 *{autor}* — *{data[:10]}*\n • Id do push: **{pushid}**.\n • Head: **{head}**\n • Before: **{before}**"))
            lista.append(ui.Separator(visible=False, spacing=discord.SeparatorSpacing.large))
        labelbotao = f'Todos os pushs'
        layout = LayoutView(titulo, repositorio, labelbotao, lista)
        await interact.response.send_message(view=layout, files=arquivos)
    
    ########################################################################################################################################

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
        dados = Usuario(discord_id=interact.user.id, github_url=self.url.value)         #salva o id do discord do usuário e o link do github
        sessao.add(dados)                                                               #adiciona o id e a url no banco de dados               
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
        dados = Repositorios(repo_url = self.url.value, repo_nome=repositorio, repo_dono=dono_repositorio) #atribui os valores às colunas do banco de dados
        sessao.add(dados)                                                               #adiciona o id e a url no banco de dados               
        sessao.commit()                                                                 #faz o commit das alterações
        sessao.close()                                                                  #salva as alterações
        await interact.response.send_message(f'{interact.user.mention}, o repositório {self.url.value} foi registrado com sucesso.')

class LayoutView(ui.LayoutView):
    def __init__(self, titulo:str, repositorio:str, labelbotao:str, lista=[]):
        super().__init__()  

        container = ui.Container()
        imagem = ui.Thumbnail('attachment://github_70px.png')
        container.add_item(ui.Section(ui.TextDisplay(f'## {titulo}'), accessory=imagem))
        container.add_item(ui.Separator(visible=True, spacing=discord.SeparatorSpacing.large))
        container.accent_color=discord.Colour.lighter_grey()

        for item in lista:
            container.add_item(item)
        
        container.add_item(ui.Separator(visible=True, spacing=discord.SeparatorSpacing.large))

        botao = ui.Button(label=labelbotao, style=discord.ButtonStyle.link, url=repositorio)
        container.add_item(ui.Section(ui.TextDisplay(f'### Dados obtidos a partir da API do GitHub.'), accessory=botao))
        self.add_item(container)
        
    async def resposta_menu(self, interact:discord.Interaction):
        resposta = interact.data['values'][0]
        return resposta
        

##########################################################################################################################################################
async def setup(bot):
    await bot.add_cog(GitHubIntegração(bot))
