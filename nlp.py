import re,keyboard,itertools,pickle,time
import pandas as pd

# Carregar variáveis
with open('C:\Projetos\Projeto- Previsao de Palavras\p_dic_duas_palavras', 'rb') as handle:
    p_dic_duas_palavras = pickle.load(handle)
with open('C:\Projetos\Projeto- Previsao de Palavras\s0', 'rb') as handle:
    s0 = pickle.load(handle)
with open('C:\Projetos\Projeto- Previsao de Palavras\s', 'rb') as handle:
    s = pickle.load(handle)
with open('C:\Projetos\Projeto- Previsao de Palavras\pt', 'rb') as handle:
     pt = pickle.load(handle)
with open('C:\Projetos\Projeto- Previsao de Palavras\palavras_selec_1', 'rb') as handle:
    palavras_selec_1 = pickle.load(handle)
with open('C:\Projetos\Projeto- Previsao de Palavras\palavras_selec_0', 'rb') as handle:
    palavras_selec_0 = pickle.load(handle)
with open('C:\Projetos\Projeto- Previsao de Palavras\palavras_todas_0', 'rb') as handle:
    palavras_todas_0 = pickle.load(handle)
with open('C:\Projetos\Projeto- Previsao de Palavras\palavras_todas_1', 'rb') as handle:
    palavras_todas_1 = pickle.load(handle)
with open('C:\Projetos\Projeto- Previsao de Palavras\d_mai_ou_min', 'rb') as handle:
    d_mai_ou_min = pickle.load(handle)

palavra_digitada = ''
proc_palavras = []
lista_atual = []
imprimir_lista = []
kb = '' 
lista_fim = []
proc_palavras1 = []

    
# Todas as funções

# Lida com erros de digitação
def erros_dig(kb,proc_palavras):
    proc_palavras2 = []
    keyblist = ["qwertyuiop","asdfghjklç","zxcvbnm"]
            
    for kbline in keyblist:
        if kb in kbline:
            i= kbline.index(kb)
            if (i-1) > -1:
                for j in proc_palavras:
                    proc_palavras2.append(j[0:-1]+kbline[i-1])
            if (i+1) <= len(kbline)-1:
                for j in proc_palavras:
                    proc_palavras2.append(j[0:-1]+kbline[i+1])
    return(proc_palavras2)

# Lida com erros de digitação gerando regex
def erros_regex(palavra_digitada):
    regexes = []
    for j in range(0,len(palavra_digitada)):
        reg = list(palavra_digitada)
        reg[j] = '.'
        reg.insert(0,'^')
        reg1 = ''.join(reg)
        regexes.append(reg1)
        reg = list(palavra_digitada)
        if j<len(palavra_digitada)-1:
            reg = list(palavra_digitada)
            reg[j] = '.'
            reg[j+1] = '.'
            reg.insert(0,'^')
            reg1 = ''.join(reg)
            regexes.append(reg1)
    reg = list(palavra_digitada)
    reg[0] = '.'
    reg[len(palavra_digitada)-1] = '.'
    reg.insert(0,'^')
    reg1 = ''.join(reg)
    regexes.append(reg1)    
    combined = "(" + ")|(".join(regexes) + ")"
    return(combined)


# Função que combina duas listas
def comb(x,y):
    lista_combinada = []
    if x:
        for combination in itertools.product(x,y):  #[str(*x)[:-1]]
            lista_combinada.append((''.join(combination[:])))
    else:
        lista_combinada = y
    return(lista_combinada)


# Função principal.Esta função considera todas as possíveis acentuações de vogais
def teclado(kb,palavra_digitada,lista_atual,proc_palavras):
    
    global imprimir_lista
    global palavras_originais
    global palavras_selec_0
    global palavras_todas_0
    global d_mai_ou_min
    global s
    
            
        
    # Considerar acentuações
    if palavra_digitada[-1] == 'a':
        variacoes = ['a','á','à','â','ã']
        proc_palavras = comb(proc_palavras,variacoes)
    elif palavra_digitada[-1] == 'e':
        variacoes = ['e','é','ê']
        proc_palavras = comb(proc_palavras,variacoes)
    elif palavra_digitada[-1] == 'i':
        variacoes = ['i','í']
        proc_palavras = comb(proc_palavras,variacoes)
    elif palavra_digitada[-1] == 'o':
        variacoes = ['o','ó','ô']
        proc_palavras = comb(proc_palavras,variacoes)
    elif palavra_digitada[-1] == 'u':
        variacoes = ['u','ú']
        proc_palavras = comb(proc_palavras,variacoes)
    elif palavra_digitada[-1] == 'c':
        variacoes = ['c','ç']
        proc_palavras = comb(proc_palavras,variacoes)
    else:
        if len(proc_palavras)==1:
            proc_palavras = [palavra_digitada]
            
        else:
            proc_palavras = [palavra_digitada]

           
    # Considerar erro de digitação quando se digita menos de 3 letras
    start_time = time.time()
    if len(palavra_digitada)<=3:
        #proc_palavras = proc_palavras+erros_dig(kb,proc_palavras)
        proc_palavras = proc_palavras
    # Usar regex para mais de 3 letras digitadas considerando erro de digitação
    else:
        s['selecao'] = 0
        s.loc[s['palavra'].str.contains(erros_regex(palavra_digitada)),'selecao'] = 1 
        s1 = s.loc[s.selecao==1,:]
    
    # Calcular Probabilidades
    if len(palavra_digitada)<=3:
        s['selecao'] = 0
        s.loc[s['palavra'].str.startswith(tuple(proc_palavras)),'selecao'] = 1
        s1 = s.loc[s.selecao==1,:]
        
        
    palavras_selec = s1['contagem'].sum()/s['contagem'].sum()
    palavras_selec_0['c'] = s['selecao']
    palavras_selec_0['b'] = (palavras_todas_0*palavras_selec/((palavras_todas_0*palavras_selec)+((1-palavras_selec)*(1-palavras_todas_0))))
    #palavras_selec_0.sort_values(by='a',ascending=True,inplace=True)
    palavras_selec_final = palavras_selec_0.loc[palavras_selec_0['c']==1,:]
    imprimir_lista = []
    for i in palavras_selec_final.sort_values(by='b',ascending=False)['a'][0:7].tolist():
        
        if i not in lista_atual and i!=palavra_digitada:
            if d_mai_ou_min[i]:
                imprimir_lista.append(i.title())
            else:
                imprimir_lista.append(i)
    
    lista_atual = imprimir_lista.copy()
    print(lista_atual)
    print(round(time.time() - start_time,2),'segundos')
    return(lista_atual,proc_palavras)

def teclado2(kb,comp_palavra,palavra_digitada,lista_atual,proc_palavras):
    
    global imprimir_lista
    global palavras_originais
    global palavras_selec_1
    global palavras_todas_1
    global d_mai_ou_min


    
        
    start_time = time.time()
       
    # Considerar acentuações
    if palavra_digitada[-1] == 'a':
        variacoes = ['a','á','à','â','ã']
        proc_palavras = comb(proc_palavras,variacoes)
    elif palavra_digitada[-1] == 'e':
        variacoes = ['e','é','ê']
        proc_palavras = comb(proc_palavras,variacoes)
    elif palavra_digitada[-1] == 'i':
        variacoes = ['i','í']
        proc_palavras = comb(proc_palavras,variacoes)
        
    elif palavra_digitada[-1] == 'o':
        variacoes = ['o','ó','ô']
        proc_palavras = comb(proc_palavras,variacoes)
    elif palavra_digitada[-1] == 'u':
        variacoes = ['u','ú']
        proc_palavras = comb(proc_palavras,variacoes)
        
    elif palavra_digitada[-1] == 'c':
        variacoes = ['c','ç']
        proc_palavras = comb(proc_palavras,variacoes)
    else:
        if len(proc_palavras)==1:
            proc_palavras = [palavra_digitada]
            
        else:
            proc_palavras = [palavra_digitada]
            
    # Considerar erro de digitação quando se digita menos de 3 letras
    
    if comp_palavra<=3:
        #proc_palavras = proc_palavras+erros_dig(kb,proc_palavras)
        proc_palavras = proc_palavras
        
    # Usar regex para mais de 3 letras digitadas considerando erro de digitação
    else:
        s0['selecao'] = 0
        s0.loc[s0['palavras'].str.contains(erros_regex(palavra_digitada),regex=False),'selecao'] = 1 
        s1 = s0.loc[s0.selecao==1,:]
        indices = s0.loc[s0.selecao==1,:].index.tolist()
        
    # Calcular Probabilidades
    if comp_palavra<=3:
        indices = []
        for i in proc_palavras:
            s1 = {pt[s] for s in [*pt.iterkeys(i)]}
            indices.append([int(s[1]) for s in sorted(s1,reverse=True)])
        indices = [item for sublist in indices for item in sublist]
        s1 = s0.iloc[indices,:]
        
        
    palavras_selec = s1['contagem'].sum()/s['contagem'].sum()
    palavras_selec_1['b'] = (palavras_todas_1*palavras_selec/((palavras_todas_1*palavras_selec)+((1-palavras_selec)*(1-palavras_todas_1))))
    palavras_selec_final = palavras_selec_1.iloc[indices,:]
    lista = palavras_selec_final.sort_values(by='b',ascending=False)['a'][0:7].tolist()
    imprimir_lista = []
    j = []    
    for i in lista:
        if i not in lista_atual and i!=palavra_digitada.split()[0] and i not in j:
            j.append(i)
            
            if d_mai_ou_min[i]:
                imprimir_lista.append(i.title())
            else:
                imprimir_lista.append(i)
            
    lista_atual = imprimir_lista.copy()
    end_time = time.time()
    print('2',round(end_time - start_time,2),'segundos')
    return(lista_atual,proc_palavras)

def previsao(kb,palavra_digitada,lista_atual,proc_palavras,kb_antigo):
    global imprimir_lista
    global comp_palavra 
    global proc_palavras1
    
    

    kb_lista = re.sub("[^\w]", " ",  palavra_digitada).split()
    if kb_antigo == '':
        lista_atual= []
        proc_palavras1= []
        
    # Procurar palavra isolada
    if (len(kb_lista)==1 and kb!=' '):
        lista_atual,proc_palavras1 = teclado(kb,kb_lista[len(kb_lista)-1],lista_atual,proc_palavras1)
        
    # Procurar a sequencia de palavras
    elif len(kb_lista)>1 and kb!=' ' and len(kb_lista[len(kb_lista)-1])<3:
        
        comp_palavra = len(kb_lista[len(kb_lista)-1])
        duas_ultimas = ' '.join(kb_lista[len(kb_lista)-2:len(kb_lista)])
        lista_atual,proc_palavras1 = teclado2(kb,comp_palavra,duas_ultimas,lista_atual,proc_palavras1)
        
    # Procurar a sequencia de palavras
    elif len(kb_lista)>=1 and kb==' ':
        kb_lista.append(' ')
        comp_palavra = len(kb_lista[len(kb_lista)-1])
        duas_ultimas = ''.join(kb_lista[len(kb_lista)-2:len(kb_lista)])
        lista_atual,proc_palavras1 = teclado2(kb,comp_palavra,duas_ultimas,lista_atual,[duas_ultimas])
        
    # Se a sequencias de palavras não é encontrada(comprimento>=2), procurar isoladamente
    elif len(kb_lista)>1 and kb!=' ' and len(kb_lista[len(kb_lista)-1])>=3:
         lista_atual,proc_palavras1 = teclado(kb,kb_lista[len(kb_lista)-1],lista_atual,proc_palavras1)
         
    return(lista_atual)