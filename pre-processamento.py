# Faz o pré-processamento do corpus e salva as variáveis chave


import nltk.corpus,re,keyboard,itertools
import pandas as pd

# Carregar o Corpus
c = []
palavras = nltk.corpus.mac_morpho.words()
palavras_limpas = []
palavras_originais = []
j = ''
for i in palavras:
    if i.isalpha():
        palavras_limpas.append(i.lower())
        palavras_originais.append(i)
    j = i.lower() 

# Criar as contrações artigo+preposição,já que o corpus nao possui contrações. Ex. 'de'+'o' = 'do'
for i in range(0,len(palavras_limpas)):
    if palavras_limpas[i] == 'o' and palavras_limpas[i-1] == 'de':
        palavras_limpas[i-1] = 'x'
        palavras_limpas[i]   = 'do'
    if palavras_limpas[i] == 'a' and palavras_limpas[i-1] == 'de':
        palavras_limpas[i-1] = 'x'
        palavras_limpas[i]   = 'da'
    if palavras_limpas[i] == 'o' and palavras_limpas[i-1] == 'em':
        palavras_limpas[i-1] = 'x'
        palavras_limpas[i]   = 'no'
    if palavras_limpas[i] == 'a' and palavras_limpas[i-1] == 'em':
        palavras_limpas[i-1] = 'x'
        palavras_limpas[i]   = 'na'
    if palavras_limpas[i] == 'aquilo' and palavras_limpas[i-1] == 'em':
        palavras_limpas[i-1] = 'x'
        palavras_limpas[i]   = 'naquilo'
    if palavras_limpas[i] == 'o' and palavras_limpas[i-1] == 'per':
        palavras_limpas[i-1] = 'x'
        palavras_limpas[i]   = 'pelo'
    if palavras_limpas[i] == 'a' and palavras_limpas[i-1] == 'per':
        palavras_limpas[i-1] = 'x'
        palavras_limpas[i]   = 'pela'
    if palavras_limpas[i] == 'os' and palavras_limpas[i-1] == 'de':
        palavras_limpas[i-1] = 'x'
        palavras_limpas[i]   = 'dos'
    if palavras_limpas[i] == 'o' and palavras_limpas[i-1] == 'a':
        palavras_limpas[i-1] = 'x'
        palavras_limpas[i]   = 'ao'
    if palavras_limpas[i] == 'as' and palavras_limpas[i-1] == 'de':
        palavras_limpas[i-1] = 'x'
        palavras_limpas[i]   = 'das'
    if palavras_limpas[i] == 'a' and palavras_limpas[i-1] == 'por':
        palavras_limpas[i-1] = 'x'
        palavras_limpas[i]   = 'pela'
    if palavras_limpas[i] == 'o' and palavras_limpas[i-1] == 'por':
        palavras_limpas[i-1] = 'x'
        palavras_limpas[i]   = 'pelo'
    if palavras_limpas[i] == 'o' and palavras_limpas[i-1] == 'a':
        palavras_limpas[i-1] = 'x'
        palavras_limpas[i]   = 'ao'
    if palavras_limpas[i] == 'a' and palavras_limpas[i-1] == 'a':
        palavras_limpas[i-1] = 'x'
        palavras_limpas[i]   = 'à'
    if palavras_limpas[i] == 'a' and palavras_limpas[i-1] == 'em':
        palavras_limpas[i-1] = 'x'
        palavras_limpas[i]   = 'na'
    if palavras_limpas[i] == 'o' and palavras_limpas[i-1] == 'em':
        palavras_limpas[i-1] = 'x'
        palavras_limpas[i]   = 'no'
    if palavras_limpas[i] == 'os' and palavras_limpas[i-1] == 'em':
        palavras_limpas[i-1] = 'x'
        palavras_limpas[i]   = 'nos'
    if palavras_limpas[i] == 'as' and palavras_limpas[i-1] == 'em':
        palavras_limpas[i-1] = 'x'
        palavras_limpas[i]   = 'nas'
    if palavras_limpas[i] == 'as' and palavras_limpas[i-1] == 'a':
        palavras_limpas[i-1] = 'x'
        palavras_limpas[i]   = 'às'
    if palavras_limpas[i] == 'os' and palavras_limpas[i-1] == 'a':
        palavras_limpas[i-1] = 'x'
        palavras_limpas[i]   = 'aos'
    
# Criar sequencia de duas palavras
    tuplas_palavras = []
j = ''
for i in range(0,len(palavras_limpas)):
    if palavras_limpas[i].isalpha() and palavras_limpas[i] != 'x' and j.isalpha() and j!= 'x':
        tuplas_palavras.append((j,palavras_limpas[i].lower()))
    if palavras_limpas[i].isalpha() and palavras_limpas[i] != 'x' and j.isalpha() and j== 'x' and palavras_limpas[i-2].isalpha() and palavras_limpas[i-2]!= 'x':
        tuplas_palavras.append((palavras_limpas[i-2].lower(),palavras_limpas[i].lower()))
    j = palavras_limpas[i].lower()
    
# Contar ocorrência de palavras no corpus
# As variáveis s e s0 contém as contagens de palavra isolada e sequencia de duas palavras respectivamente
c1 = pd.DataFrame(palavras_limpas)
s = pd.DataFrame()
s['palavra'] = c1[0].value_counts().index
s['contagem'] = c1[0].value_counts().values

# Contar ocorrência de sequencias de palavras no corpus
c2 = pd.DataFrame(tuplas_palavras)
c2['2'] = c2[0]+' '+c2[1]
s0 = pd.DataFrame()
s0['palavras'] = c2['2'].value_counts().index
s0['contagem'] = c2['2'].value_counts().values
s0['probab'] = s0['contagem']/s0['contagem'].sum()
s0['palavra1'] = s0['palavras'].str.split(" ", n = 1, expand = True)[0]
s0['palavra2'] = s0['palavras'].str.split(" ", n = 1, expand = True)[1]
s0['indice'] = range(0,len(s0))
p_dic_duas_palavras1 = s0.drop(['contagem','palavra1','palavra2'],axis=1).set_index('palavras').T.to_dict('list')
p_dic_duas_palavras = {k:(v[0],v[1]) for k,v in p_dic_duas_palavras1.items()}

import pytrie
global pt
pt = pytrie.Trie(p_dic_duas_palavras)

# Calcular probabilidades
palavras_selec_1 = pd.DataFrame()
palavras_selec_0 = pd.DataFrame()
palavras_selec_1['a'] = s0['palavra2']
palavras_selec_0['a'] = s['palavra']
palavras_todas_1 = s0['contagem']/s0['contagem'].sum()
palavras_todas_0 = s['contagem']/s['contagem'].sum()

# Descobrir se uma palavra se escreve em maiusculo ou minusculo
g = pd.DataFrame(palavras_originais)
g2 = pd.DataFrame()
g2['palavra'] = g[0].value_counts().index
g2['contagem'] = g[0].value_counts().values
g2d = g2.set_index('palavra').T.to_dict('list')
# 0 para palavra minuscula, 1 para maiúscula
d_mai_ou_min = {}
i = 0
for k,v in g2d.items():
    try:
        if k[0].islower() and g2d[k]>g2d[k.title()]:
            d_mai_ou_min[k.lower()] = 0
    except:
            d_mai_ou_min[k.lower()] = 0
            next
    try:
        if k[0].isupper() and g2d[k]>g2d[k.lower()]:
            d_mai_ou_min[k.lower()] = 1
    except:
            d_mai_ou_min[k.lower()] = 1
            
    i += 1
    
# Salvarr variáveis
import pickle
with open('p_dic_duas_palavras', 'wb') as handle:
    pickle.dump(p_dic_duas_palavras, handle)
with open('s0', 'wb') as handle:
    pickle.dump(s0, handle)
with open('s', 'wb') as handle:
    pickle.dump(s, handle)
with open('pt', 'wb') as handle:
    pickle.dump(pt, handle)
with open('palavras_selec_1', 'wb') as handle:
    pickle.dump(palavras_selec_1, handle)
with open('palavras_selec_0', 'wb') as handle:
    pickle.dump(palavras_selec_0, handle)
with open('palavras_todas_0', 'wb') as handle:
    pickle.dump(palavras_todas_0, handle)
with open('palavras_todas_1', 'wb') as handle:
    pickle.dump(palavras_todas_1, handle)
with open('d_mai_ou_min', 'wb') as handle:
    pickle.dump(d_mai_ou_min, handle)