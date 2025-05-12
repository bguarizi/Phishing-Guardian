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
from memory_profiler import profile
from sklearn.svm import SVC
from xgboost import XGBClassifier

file_csv = "./teste.csv"

seed = 100

data = pd.read_csv("./data_bases/data_base.csv")

x = data[["url_lenght", "is_https", "ip_format", "dot_count", "suspect_char","activate_days","page_rank", "html_input", "certificate", "redirect", "https_text", "caract_hifen", "iframe"]]
x_ = data[["url_lenght", "is_https", "dot_count","activate_days","page_rank", "html_input", "certificate", "https_text", "caract_hifen", "iframe"]]
y = data["phishing"]

X_treino, X_teste, y_treino, y_teste = train_test_split(x, y, train_size=0.85, random_state=seed, shuffle=True, stratify=y)

modelo = 0

def train_test():
    modelo.fit(X_treino, y_treino)

    # Fazendo previsões
    y_pred = modelo.predict(X_teste)

    # Calculando a acurácia do modelo
    acuracia = accuracy_score(y_teste, y_pred) * 100
    print(f"Acurácia: {acuracia:.2f}%")

    print(f"Classification Report: \n {classification_report(y_teste, y_pred, digits=4)}")

    nfolds = 10
    scoring = 'accuracy'

    scores = cross_val_score(modelo,
                            X = X_treino,
                            y = y_treino,
                            scoring = scoring,
                            cv = nfolds,
                            n_jobs = -1)

    print(f"Acurácia Média - Cross Validation = {100*np.mean(scores):.2f}%") 

    print("\n--------------------------------------\n")

while True:
    X_treino, X_teste, y_treino, y_teste = train_test_split(x, y, train_size=0.85, random_state=seed, shuffle=True, stratify=y)

    print("\nMenu de Métricas:")
    print("0 - Métricas Random Forest")
    print("1 - Métricas SVM")
    print("2 - Métricas XGBoost")
    print("3 - Métricas XGBoost e Random Forest - Removendo atributos A3, A5 e A10")
    print("4 - Exibir coeficiente de correlação")
    print("5 - Sair")
    
    opcao = input("Digite o número da opção desejada: ")
    
    if opcao == "0":
        print("\nExibindo Métricas do Random Forest...")

        modelo = RandomForestClassifier(
        n_estimators=100,  
        criterion='gini',               
        min_samples_split=2,   
        min_samples_leaf=1,     
        max_features='sqrt',    
        bootstrap=True,         
        random_state=seed,
        min_impurity_decrease=0.00001)

        train_test()
    elif opcao == "1":
        print("\nExibindo Métricas do SVM...")

        modelo = SVC(random_state=seed)
        train_test()
    elif opcao == "2":
        print("\nExibindo Métricas do XGBoost...")

        modelo = XGBClassifier(n_estimators=100)
        train_test()
    elif opcao == "3":
        X_treino, X_teste, y_treino, y_teste = train_test_split(x_, y, train_size=0.85, random_state=seed, shuffle=True, stratify=y)
        
        print("\nExibindo Métricas do Random Forest...")
        modelo = RandomForestClassifier(
        n_estimators=100,  
        criterion='gini',               
        min_samples_split=2,   
        min_samples_leaf=1,     
        max_features='sqrt',    
        bootstrap=True,         
        random_state=seed,
        min_impurity_decrease=0.00001)

        train_test()

        print("\nExibindo Métricas do XGBoost...")

        modelo = XGBClassifier(n_estimators=100)
        train_test()

    elif opcao == "4":
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
    elif opcao == "5":
        print("\nSaindo do programa...")
        break
    else:
        print("\nOpção inválida! Por favor, digite um número entre 0 e 3.")



                    

