from flask import Flask,render_template,json,make_response, request, current_app
import nlp,re
import unidecode
from flask_cors import CORS

app = Flask(__name__, template_folder='static')  # Change assignment here
CORS(app)
global maiuscula
maiuscula = 0
global palavra_digitada
palavra_digitada = ''
global comp_palavra
comp_palavra = 0
global proc_palavras
proc_palavras = []
global lista_atual
lista_atual = []
global imprimir_lista
imprimir_lista = []
global palavra_completa
palavra_completa = 0
global kb_antigo 
kb_antigo = ''
global proc_palavras1
proc_palavras1 = []


@app.route('/',methods=['POST','GET'])
def manda_palavras():
    global maiuscula
    global palavra_digitada
    global lista_atual
    global proc_palavras
    global palavra_completa
    global kb_antigo
    global proc_palavras1
    
    
    kb = request.get_json(force=True)['char']
    data = []
    
    # Ler e Verificar se a lista de palavras deve ser minuscula ou maiuscula
    kb = unidecode.unidecode(kb)
    if kb == kb_antigo:
        kb = kb+' '
    
    kb_lista = re.sub("[^\w]", " ",  kb).split()
    if not kb=='':
        if kb_lista[len(kb_lista)-1][0].isupper():
            maiuscula = 1
        else:
            maiuscula = 0
    if maiuscula and kb[-1:]==' ':
        maiuscula = 0
    
    # Ver se um botao de palavra foi apertado
    
    palavra_selec = request.get_json(force=True)['palavra_selec']
    kb2 = ' '.join(i.lower() for i in kb_lista)
    
    # Mostrar palavras recomendadas apenas se nao tiver sido apertado antes o botão limpar ou pontuação
    # Neste caso zerar variaveis. Chamar rotina de previsao
    
    if  kb=='' or kb[-1:]=='!' or kb[-1:]=='?' or kb[-1:]=='.' or kb[-1:]==',' or kb=='zerar':
        data = []
        proc_palavras1 = []
        proc_palavras = []
        lista_atual = []
        maiuscula = 1
        kb = ''
        if kb_antigo[:-1]== ',':
            maiuscula = 0
    else:
        data = nlp.previsao(kb[-1],kb2,lista_atual,proc_palavras,kb_antigo)
    if data== lista_atual:
        data= []
        lista_atual = data.copy()
    
    # Transformar a lista em maiuscula ou nao
        
    if maiuscula:
        
        for i in range(0,len(data)):
        	data[i]= data[i].title()
    kb_antigo = kb
    return render_template("settings.html", data=[json.dumps(i,ensure_ascii=False) for i in data])
    


if __name__ == "__main__":         
    
    app.debug = True
    app.run()  