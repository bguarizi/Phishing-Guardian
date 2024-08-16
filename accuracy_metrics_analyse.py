import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, classification_report
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import f1_score
import numpy as np
import time
import matplotlib.pyplot as plt
import csv
import re
import requests
import psutil

file_csv = "./teste.csv"

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

# Função para monitorar uso de CPU e RAM
def monitor_resources():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    return cpu_usage, ram_usage

start_time = time.time()
start_cpu, start_ram = monitor_resources()

modelo_rf.fit(X_treino, y_treino)

# Parar temporizador e monitoramento
end_time = time.time()
end_cpu, end_ram = monitor_resources()

training_time = end_time - start_time
print(f"Tempo de treinamento: {training_time:.2f} segundos")

print(f"Uso de CPU (inicial): {start_cpu}%")
print(f"Uso de RAM (inicial): {start_ram}%")
print(f"Uso de CPU (final): {end_cpu}%")
print(f"Uso de RAM (final): {end_ram}%")


# Fazendo previsões
y_pred = modelo_rf.predict(X_teste)

y_pred_treino = modelo_rf.predict(X_treino)

acuracia = accuracy_score(y_treino, y_pred_treino) * 100
print(f"Acurácia Treino: {acuracia:.2f}%")

print(f"Classification Report Treino: \n {classification_report(y_treino, y_pred_treino, digits=4)}")

# Calculando a acurácia do modelo
acuracia = accuracy_score(y_teste, y_pred) * 100
print(f"Acurácia Teste: {acuracia:.2f}%")

print(f"Classification Report Teste: \n {classification_report(y_teste, y_pred, digits=4)}")

y_new = data[["phishing", "url"]]

y_new = y_new.drop(columns=['url'])

dataframe = np.concatenate([x,y_new],axis=1)

CORRCOEF = np.corrcoef(dataframe,rowvar=False)

plt.figure()
plt.bar(x=["A1", "A2", "A3", "A4", "A5","A6","A7", "A8", "A9", "A10", "A11", "A12", "A13"], height=CORRCOEF[:-1,-1], zorder=2)
plt.grid(visible=True,zorder=1)
plt.ylabel('Coeficiente de Correlação')
plt.xticks(["A1", "A2", "A3", "A4", "A5","A6","A7", "A8", "A9", "A10", "A11", "A12", "A13"])
plt.xlabel('Variáveis de Entrada')
plt.title('Coeficiente de Correlação entre variáveis de entrada a as classes de saída')
plt.show()  

nfolds = 10
scoring = 'accuracy'

scores = cross_val_score(modelo_rf,
                         X = X_treino,
                         y = y_treino,
                         scoring = scoring,
                         cv = nfolds,
                         n_jobs = -1)

ax = plt.axes()
ax.plot(scores,'ro-')
ax.set_xticks(range(nfolds),labels=range(1,nfolds+1))
ax.set(title='Acurácia Média =' + f'{100*np.mean(scores):.2f}' + '%',
       xlabel='Divisão', 
       ylabel='Acurácia',
       xlim=[0,nfolds-1])
ax.grid(visible=True) 

cm = confusion_matrix(y_teste, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)


plt.show()

# disp.plot()
# plt.show()                      

