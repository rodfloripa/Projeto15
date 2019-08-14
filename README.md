# Projeto15
Previsão de Palavras

Neste projeto é calculada a probabilidade de uma palavra estar sendo digitada
em um navegador de internet,exatamente o que o teclado virtual dos celulares faz.
O corpus adotado constitui-se de textos extraídos da Folha de S. Paulo no período 
de 12/01/2010 a 12/02/2011, com 1,1 milhão de palavras. Este corpus está disponível
na biblioteca nltk. O projeto não utiliza nenhuma biblioteca de nlp, apenas o módulo
nltk.corpus. 

Arquivos:
main2.py :                         programa principal
nlp.py:                            biblioteca que criei,é utilizada pelo programa principal
previsao.html:                     o programa final em html
pre-processamento.py:              processa o corpus e gera as variáveis utilizadas no programa nlp.py
p_dic_duas_palavras,s0
s,pt,palavras_selec_1,
palavras_selec_0,d_mai_ou_min,
palavras_todas_0,palavras_todas_1: variáveis geradas por pre-processamento.py, são utilizadas por nlp.py
