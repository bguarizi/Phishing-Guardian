# FindPhishing - Detector de sites de Phishing

## Tópicos

- [Instalação](#instalação)
- [Uso](#uso)
- [Métricas](#metricas)

## Instalação

Para instalar o projeto, siga estes passos:

1. Garanta que você possui o Python instalado em sua máquina:

    Abra o terminal e digite: 

    ```bash
    python --version
    ```

    Caso seja retornada a versão do Python, está tudo ok. Caso você não tenha instalado ainda, siga os seguintes passos:

    - Windows ou MacOs:

    Acesse o site oficial:

    ```bash
    https://www.python.org/downloads/
    ```
    E clique no botão para fazer download, depois siga os passos de instalação e volte ao passo inicial para verificar a versão do Python e se certificar de que a instalação foi feita corretamente.

    - Linux:

    Acesse o site oficial e veja qual é a versão atual disponível do Python:

    ```bash
    https://www.python.org/downloads/
    ```

    Atualmente a versão mais recente é a 3.12.4.
    Em seguida, digite o seguinte comando no terminal:

    ```bash
    sudo apt-get install python3.12
    ```

    Troque o '3.12' pela versão mais atualizada.

    Refaça o passo inicial para verificar a versão instalada e garantir que a instalação ocorreu corretamente.

2. Clone o repositório através do comando:

    ```bash
    git clone https://github.com/bguarizi/findphishing.git
    ```

    Acesse o repositório baixado:

    ```bash
    cd findphishing/
    ```

3. Faça a instalação das bibliotecas necessárias:

   Instale o arquivo requirement.txt através do pip com o seguinte comando:

    ```bash
    pip install -r requirements.txt
    ```

4. Adicione a extensão ao seu navegador Google Chrome:

    Abra seu navegador e acesse:

    ```bash
    chrome://extensions/
    ```

    Clique no botão "Carregar sem compactação" e vá até o caminho da pasta que acabou de clonar do projeto.
    Selecione a pasta "url-collector-extension" e clique em "Abrir".

    Sua extensão já estará funcionando!


## Uso

Após a instalação ter sido realizada corretamente, basta apenas ativar a execução do código em Python:

1. Abra novamente o terminal na pasta do projeto que foi baixado:

    Após estar na pasta em questão, rode o seguinte comando:

    ```bash
    python code_analyse_trafic.py
    ```

    Aguarde até que a tela mostre que o servidor está ativo na porta 5000.

3. Teste seu navegador:

    Abra o Google Chrome e começe a navegar. 
    Serão emitidos alertas em tempo real sobre as páginas que estão sendo acessadas.

OBS1.: Os alertas podem demorar alguns segundos para serem emitidos. Tenha calma, esta ainda é a versão inicial do projeto!

OBS2.: A cada site acessado, um alerta será emitido e você precisará apertar o botão de confirmação.

OBS3: Caso queira desativar os alertas emitidos, basta cancelar a execução do script no terminal e desativar a extensão do navegador acessando novamente "chrome://extensions/" e desativando ou excluindo a extensão.

## Métricas

Além do código para ser executado, também é disponibilizado o código que mostra os valores finais das métricas do modelo: acurácia, recall, precisão e F1 Score. Além de também mostrar os gráficos de Matriz de Confusão, Validação Cruzada e Coeficiente de Correlação.

Para executá-lo, acesso no terminal a pasta do projeto e digite o seguinte comando:

    ```bash
    python accuracy_metrics_analyse.py
    ```

