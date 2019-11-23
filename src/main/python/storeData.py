import numpy as np
import pandas as pd
import pickle
from Course import *
from Period import *
from Trie import *

fileName = "data.csv"
data = pd.read_csv(fileName, sep=';')
courses = {}
periods = {}
added = []

root = TrieNode('*', Course(0,'*'))

# itera sobre as linhas do csv
for cod, nome, ano, periodo, vinculados, matriculados, ingressantes, diplomados, evadidos in zip(data["CodCurso"], data["NomeCurso"], data["Ano"], data["Periodo"], data["Vinculados"], data["Matriculados"], data["Ingressantes"], data["Diplomados"], data["Evadidos"]):
    date = str(ano) + "/" + str(periodo)

    # se ainda não registrou o curso
    if cod not in courses.keys():
        courses[cod] = Course(cod, nome.upper())

    # se ainda não registrou a data
    if date not in periods.keys():
        periods[date] = Period(ano, periodo)

    # Duplica os dados para as duas visualizações
    periods[date].addData(cod, vinculados, matriculados,
                        ingressantes, diplomados, evadidos)
    courses[cod].addData(date, vinculados, matriculados,
                        ingressantes, diplomados, evadidos)

    # só adiciona uma vez na árvore
    if cod not in added:    
        add_node(root, courses[cod])
        added.append(cod)

# Salva os cursos num arquivo binário pickle
with open('courses.p', 'wb') as f:
    pickle.dump(courses,f)    

# Salva os períodos num arquivo binário pickle
with open('periods.p', 'wb') as f:
    pickle.dump(periods,f)    

# Salva a árvore TRIE num arquivo binário pickle
with open('trie.p', 'wb') as f:
    pickle.dump(root, f)
