import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import time
import matplotlib.pyplot as plt
import csv
import re
import requests
import whois
from datetime import date
from flask import Flask, request, jsonify

print("Iniciando software...")

app = Flask(__name__)

file_csv = "./teste.csv"

urls_ignore = ["chrome://", "127.0.0.1", "localhost"]

seed = 42

data = pd.read_csv("./data_bases/data_base.csv")

x = data[["url_lenght", "is_https", "ip_format", "dot_count", "suspect_char","activate_days","page_rank", "html_input", "certificate", "redirect", "https_text", "caract_hifen", "iframe"]]
y = data["phishing"]

# Dividindo os dados em conjuntos de treino e teste
X_treino, X_teste, y_treino, y_teste = train_test_split(x, y, train_size=0.85, random_state=seed, shuffle=True, stratify=y)

# Criando o modelo RandomForest
modelo_rf = RandomForestClassifier(
       n_estimators=100,       
       max_depth=10,           
       min_samples_split=10,   
       min_samples_leaf=4,     
       max_features='sqrt',    
       bootstrap=True,         
       random_state=seed,
       min_impurity_decrease=0.001)

# Treinando o modelo
modelo_rf.fit(X_treino, y_treino)

#Função responsável por executar a normalização mim-max dos dados coletados
def normalize_min_max(val, min, max):
    val = (val-min) / (max - min)
    return val

#Função que coleta o html na página
def get_html(url):
    try:
        resposta = requests.get(url, timeout=2) # Timeout de 2 segundos, caso haja demora na resposta da página
        
        resposta.raise_for_status()  # Verifica se houve algum erro na requisição

        html_content = resposta.text
        
        return html_content
    
    except requests.exceptions.RequestException as e:
        return None

#Função que verifica se a url possui formato IP
def verify_ip_format(string):
    padrao = r'^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$' # Define o formato IP como X.X.X.X 
    if re.match(padrao, string): # Analisa se o formato bate com a URL
        return True
    else:
        return False

#Executa acesso ao OpenPage Rank para coleta do page rank do domínio 
def acess_openpagerank(domains):
    url_pagerank = "https://openpagerank.com/api/v1.0/getPageRank"
    params = {"domains[]": domains}
    headers = {"API-OPR": "gs80ocksg4ccss48c0ccog0wsks8gksk48oc0kww"} # É necessário uma API Key para acesso
    try:
        response = requests.get(url_pagerank, params=params, headers=headers)
        data = response.json()
        return data
    except:
        return None

#Função que extrai o domínio da função e chama a função anterior para coleta do pagerank
def verify_page_rank(url):
    domain = url.replace("http://","").replace("https://","").replace("www.","")
    indice = domain.find('/') 
    if indice != -1:
        domain = domain[:indice] 
    indice = domain.find(':') 
    if indice != -1:
        domain = domain[:indice]

    data = acess_openpagerank(domain)

    valuePageRank = data["response"][0]["page_rank_decimal"]

    if (valuePageRank):
        return valuePageRank
    else:
        return 0

#Coleta as informações de certificado de páginas HTTPS
def certificate(dominio):
    context = ssl.create_default_context()
    with socket.create_connection((dominio, 443)) as sock: #Executa a conexão
        with context.wrap_socket(sock, server_hostname=dominio) as ssock:
            cert = ssock.getpeercert() #Coleta informações de certificado
            issuer = dict(x[0] for x in cert['issuer'])
            unidade_certificadora = issuer['organizationName'] #Coleta unidade certificadora
            data_emissao = datetime.strptime(cert['notBefore'], "%b %d %H:%M:%S %Y %Z").date() #Coleta data de emissão do certificado
            data_expiracao = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z").date() #Coleta data de validade do certificado
            return data_emissao, data_expiracao, unidade_certificadora

#Função geral que coleta todos os parâmetros e os organiza em uma lista
def verify_pages(url, html_input, html_iframe, valuePageRank):
    results = []

    #Adiciona a URL à lista
    results.append(str(url))

    url_d = url.replace("http://","").replace("https://","")

    domain = url.replace("http://","").replace("https://","").replace("www.","")
    indice = domain.find('/') 
    if indice != -1:
        domain = domain[:indice] 
    indice = domain.find(':') 
    if indice != -1:
        domain = domain[:indice] 

    # Tamanho da URL
    len_url = normalize_min_max(len(url), 0, 10000)
    results.append(str(len_url))

    # Se é Https ou Http
    if "https" in url:
        results.append("1") # 1, caso seja https
    else:
        results.append("0") # 0, caso não seja https


    # Se possui formato de IP ou não
    ip = verify_ip_format(domain)
    if (ip):
        results.append("1") # 1, se tem formato de IP
    else:
        results.append("0") # 0, se não tem formato de IP

    # Quantidade de pontos na string
    count_dot = url.count('.')
    count_dot = normalize_min_max(count_dot, 0, 100)
    results.append(str(count_dot))

    # Caracter suspeito "@"
    if '@' in url:
         results.append("1") # 1, se possui um caracter suspeito
    else:
        results.append("0") # 0, se não possui um caracter suspeito

    # Adiciona a flag sobre a existencia da tag input
    results.append(html_input)

    flag = 0

    # Verifica há quanto tempo um domínio existe através do whois
    try:
        info = whois.whois(domain)
        
        try:
            data_site = info.creation_date[0].date()
        except:
            data_site = info.creation_date.date()

        data_atual = date.today()
        dias_ativo = data_atual - data_site
        dias_ativo = normalize_min_max(dias_ativo.days, 0, 40000)
        results.append(str(dias_ativo)) # Adiciona os dias ativos à lista
        flag = 1
    except:
        flag = 0

    #Caso os dias ativos não tenham sido coletados, adiciona a flag 0 à lista
    if (flag == 0):
        results.append("0")
        

    # Adiciona o PageRank
    valuePageRank = normalize_min_max(valuePageRank, 0, 10)
    results.append(str(valuePageRank))

    # Tempo de validade do certificado da página
    try:
        if "https" in url:
            data_emissao, data_expiracao, unidade_certificadora = certificate(domain)
            certificate_days = (data_expiracao - data_emissao).days
            certificate_days = normalize_min_max(certificate_days, 0, 730)
            results.append(str(certificate_days)) # Adiciona o tempo de validade à lista
        else:
            results.append("0") #Caso não seja https adiciona 0 à lista
    except:
        results.append("0") #Caso não consiga coletar a informação adiciona 0 à lista

    #Verifica redirecionamento
    if '//' in url_d:
        results.append("1")
    else:
        results.append("0")

    #Verifica como texto na url https

    if 'https' in url_d:
        results.append("1")
    else:
        results.append("0")

    #Verifica hífen no domínio

    if '-' in domain:
        results.append("1")
    else:
        results.append("0")

    #Verifica iframe no html

    if html_iframe == 1:
        results.append("1")
    else:
        results.append("0")

    return results

predit = []

#Função que utiliza o Flask para acessar o servidor e coletar a URL acessada pelo usuário
@app.route('/receive_url', methods=['POST'])
def receive_url():
    data = request.get_json()
    url_intercept = data.get('url') # coleta a url

    ignore = 0

    # Verifica se a URL está na lista de URLs a serem ignoradas (para não gerar falsos positivos)
    for i in urls_ignore:
        if i in url_intercept:
            ignore = 1

    if ignore == 0:
        start_time = time.time()

        valuePageRank = verify_page_rank(url_intercept) #Coleta o page rank

        htmlCode = get_html(url_intercept)

        flag_html = 0
        flag_iframe = 0

        #Verifica as tags no código HTML
        if htmlCode:
            if "<input" in htmlCode:
                flag_html = 1
            if "<iframe" in htmlCode:
                flag_iframe = 1

        result = verify_pages(url_intercept, flag_html, flag_iframe, valuePageRank) #Realiza a coleta de todos os outros atributos

        #Escreve as informações coletadas em um arquivo para poder ler e enviar as informações ao classificador
        with open(file_csv, 'w+') as csvfile:
            csvfile.write("url,url_lenght,is_https,ip_format,dot_count,suspect_char,html_input,activate_days,page_rank,certificate,redirect,https_text,caract_hifen,iframe\n")
            escritor_csv = csv.writer(csvfile)
            escritor_csv.writerow(result)


        data_intercept = pd.read_csv(file_csv)

        # Coleta as informações adquiridas
        x = data_intercept[["url_lenght", "is_https", "ip_format", "dot_count", "suspect_char","activate_days","page_rank", "html_input","certificate","redirect", "https_text", "caract_hifen", "iframe"]]

        x = x.dropna(axis=1)

        # Executa a predição com o modelo (0 = legítimo; 1 = phishing)
        phish = modelo_rf.predict(x)

        end_time = time.time()

        total_time = end_time - start_time
        # Envia a mensagem de volta ao servidor
        if (phish[0] == 1):
            print(f"URL {url_intercept} é suspeita. Aconselhamos que não compartilhe dados ou informações sensíveis.")
            return jsonify({'message': f'O site acessado através do link {url_intercept} é suspeito. Aconselhamos que não compartilhe dados ou informações sensíveis.\nTempo de análise: {total_time:.2f} segundos'})
        else:
            print(f"URL {url_intercept} foi identificada como navegação segura.")
            return jsonify({'message': f'NAVEGAÇÃO SEGURA\nTempo de análise: {total_time:.2f} segundos'})

if __name__ == '__main__':
    app.run(debug=False)









