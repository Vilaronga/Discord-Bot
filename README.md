## Discord-Bot
O desenvolvimento desse bot tem como objetivo aprender e aplicar conceitos anteriormente vistos em sala de aula relacionados à Linguagem Python, assim como trata-se de um projeto avaliativo para a disciplina de Laboratório de Programação - E01.

**Atenção, mencionarei três tokens durante a configuração, cada token deve estar em uma linha no seu arquivo .env**
Ex:
* BOT_TOKEN="seu token"
* GITHUB_TOKEN="seu token"
* GEMINI_KEY="sua key"

## Configurando o Bot

1. Dentro da pasta principal do bot crie um arquivo chamado ".env"
    * 1.1. Dentro do seu arquivo .env crie uma varívavel chamada BOT_TOKEN='' (esta armazenará o token do seu bot)

2. Criar um novo aplitacativo (que será o seu bot)
    * 2.1. Acesse: https://discord.com/developers/applications, realize o login com sua conta do discord e crie um novo aplicativo./
    * 2.2. Após criar o aplicativo (bot), acesse ele pelo próprio site, vá até a o menu lateral "Bot" e copie o token gerado.
    * 2.3. Volte ao arquivo .env e atribua seu token à varíavel BOT_TOKEN. (BOT_TOKEN='SEU TOKEN AQUI')
    * 2.4. No mesmo menu Bot, desça um pouco a página e encontrará três opções para serem marcadas caso já não estejam (Presence Intent, Server Member * Intent e Message Content Intent), deixe todas ligadas.
    * 2.5. Vá até o menu lateral "OAuth2", e procure pela seção "OAuth2 URL Generator"
    * 2.6. Nesta seção, marque a seguinte caixa: "bot". Abrirá em baixo outra seção, marque "Administrator". 
    * 2.7. Copie a URL gerada mais abaixo, é através dela que você convidará o bot para o seu discord, basta acessa-la pelo navegador.

3. Faça as importações de bibliotecas necessárias
    * 3.1. Dentro do seu terminal, certifique-se de estar com o diretório selecionado na pasta do projeto.
    * 3.2. Digite no terminal pip install -r requirements.txt
    * 3.3. Aguarda a instalação das bibliotecas necessárias.
    * 3.4. Pode ser que alguma biblioteca ou outra não seja instalada corretamente, mas basta verificar nos arquivos qual não foi intalada e instalar manualmente.

4. (Opcional): O bot possui integração com a api do GitHub e a API do gemini, caso deseje vinculá-las siga os próximos passos.
    * 4.1. Acesse https://github.com/settings/personal-access-tokens e gere um novo token.
        * 4.1.1. Vá até o arquivo .env, crie uma variável GITHUB_TOKEN e atribua a chave a ela. (GITHUB_TOKEN="SUA CHAVE")
    * 4.2. Com o novo token gerado, clique no nome dele dentro do site para acessar as configurações do token.
    * 4.3. Provavelmente você verá alguns botões entitulados "Edit", clique no segundo, o que encontra-se à frente de 'Access on "Seu nome aqui"'.
    * 4.4. Abrirá algumas opções, selecione a terceira opção "Only selected repositories". 
    * 4.5. Selecione o repositório que você deseja no menu que aparecerá.
    * 4.6. Abaixo na seção "Permissions", clique em "Add permissions" e marque a opção "Issues".
    * 4.7. Após marcar a opção Issues, você verá que logo abaixo de "Add permissions" possui um campo "Acess: read only" ou parecido.
    * 4.8. Mude o acesso de read only para "Read and write".
    * 4.9. Clique no botão verde "Update" logo abaixo e o bot já estará funcional com o GitHub, você pode repetir essa ação parra cada repositório que salvar no banco de dados do bot.

5. (Opcional): Integração com gemini
    * 5.1. Acesse: https://aistudio.google.com/app/api-keys
    * 5.2. Crie uma chave API e copie ela.
    * 5.3. Vá até o arquivo .env, crie uma variável GEMINI_KEY
    * 5.4. Atribua a sua chave à variável GEMINI_KEY
    * 5.5. Ficará assim GEMINI_KEY="sua chave"
    * 5.6. Agora já está vinculado.

## Comandos do bot:

Logo abaixo estão todos os comandos do Bot seguindo a seguinte estrutura**

/comando: "O que o comando faz." - Usuários que podem utilizar.

* **/par_ou_impar**: Verifica se o número fornecido é par ou ímpar.
* **/inversor_string**: Inverte um texto (de trás para frente).
* **/celsius_fahrenheit**: Converte uma temperatura de Celsius para Fahrenheit.
* **/fahrenheit_celsius**: Converte uma temperatura de Fahrenheit para Celsius.
* **/somar**: Realiza a soma entre 2 números
* **/subtrair**: Realiza a subtração entre 2 números.
* **/multiplicar**: Realiza a multiplicação entre 2 números.
* **/dividir**: Realiza a divisão entre 2 números (de trás para frente).
* **/gemini**: Faz uma pergunta ao gemini 2.5-Flash.
* **/vincular_github**: Vincula um perfil do github ao seu usuário do discord.
* **/registrar_repositorio**: Salva um repositório no banco de dados do Bot.- Apenas @Administrador.
* **/remover_repositorio**: Remove um repositório do banco de dados. - Apenas @Administrador.
* **/abrir_issue**: Permite a abertura de issues no repositório selecionado.
* **/commits**: Mostra os 5 últimos commits de um repositório selecionado.
* **/pushs**: Mostra os 5 últimos pushs de um repositório selecionado.
* **/issues**: Mostra as 5 últimas issues abertas de um repositório selecionado.
* **/branches**: Mostra as branches de um repositório selecionado.
* **/ola**: Responde com um Olá para o usuário.
* **/abrir_ticket**: Cria um canal de suporte para atender a uma dúvida ou problema.
* **/fechar_ticket**: Encerra um ticket aberto. - Apenas @Administrador.
