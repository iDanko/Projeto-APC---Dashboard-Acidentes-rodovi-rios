import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px 
import json
import csv
from dash import dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

df=pd.read_csv('datatran.2020.csv', sep=';') #leitura do dataframe em csv.
data_list = df.values.tolist()

#Sunburst

meses=pd.read_csv('meses-.csv') #leitura da planilha de meses 
meses_list=meses.values.tolist() #tranformar a base de meses em uma lista

#separar a coluna 'data' da meses_list para comparar com as datas da base de dados (coluna [1] = "data-inversa")
compara_mes=[] #criar lista pra armazenar a coluna 'data'
for linha in meses_list: #laço de repetição para percorrer a lista de meses 
    compara_mes.append(linha[1]) # incluir so a coluna de datas na lista "compara_mes'(coluna de datas tem o indice [1] na lista de meses)
compara_mes #lista com apenas a coluna 'datas'

#separar a coluna de datas (dia/mes/ano).
data_2020 = [] #criando uma lista para datas
for linha in data_list: #laço de repetição para percorrer a lista do dataframe inteira
    data_2020.append(linha[1]) # incluir so a coluna de datas na lista de datas (coluna de datas tem o indice da coluna [1] da lista data_list)
data_2020 #lista com somente as datas da base de dados

#substituindo as datas (mes/dia/ano) pelos seus respectivos meses
meses_2020 = [] #lista vazia que ira receber o elementos do laço.
for c in range(0,len(compara_mes)): #percorrer a lista de meses
    for d in range(0,len(data_2020)): #percorrer a lista de datas (mes/dia/ano)
        if compara_mes[c][0]==data_2020[d][5] and compara_mes[c][1]==data_2020[d][6]: #comparar os algarismos de cada string presente na lista, linha [c] e caractere [0]. ex: compara_mes[c] para c=0 == compara_mes[0] = '1/'; compara_mes[0][0]="1" e compara_[0][1]='/'. o mesmo ocorre com a lista data_2020 (datas da base de dados) que se inicia com o mês. Fazendo então a comparação do primeiro e do segundo caracterie de cada lista, caso o mes tenha um algarismo (janeiro = 1, fevereiro = 2), o segundo algarismo comparado será a barra (1 = 1 ; / = /; 1/ = janeiro), caso o mes tenham 2 algarismos (dezembro=12; novermbro=11), a segunda comparação sera a comparação do segundo algarismo do mes (1 = 1; 2 = 2; 12/ = Dezembro).
            meses_2020.append(meses_list[c][0]) #adicionar o mes correspondente à data na lista, de acordo com a comparação feita no laço if
meses_2020 #lista de meses correspondentes a cada data
# separar a coluna de data_list
tipos=[] #criar uma lista vazia para receber a coluna de tipos de acidentes 
for linha in data_list: #percorrer toda a base de dados
    tipos.append(linha[9]) #acrescentar à lista somente a coluna [9] == tipo de acidentes

# separar a coluna de feridos graves
feridos=[] #criar lista para receber os elementos da coluna de feridos graves
for linha in data_list: #percorrer toda a base de dados
    feridos.append(linha[20]) #acrescentar à lista somente a coluna [20] == feridos_graves
feridos #lista de feridos graves 
inteiros_feridos=list(map(int, feridos))
total = sum(inteiros_feridos)
#CONTRUÇÃO DO GRÁFICO
#grafico de rosca
# TEMA: quantidade de feridos graves de cada tipo de acidente em função do mês
#lista 'meses_20202' com os meses do ano 
#lista 'tipos' com os tipos de acidentes
#lista 'feridos'  com a quantidade de feridos graves por acidente

df=dict(MESES=meses_2020,TIPOS=tipos,FERIDOS=feridos, Total='Total') #dicionario que irá receber os dados das listas que estarão no grafico
fig_sunburst=px.sunburst(df,path=['Total','MESES','TIPOS'], values='FERIDOS', #plotando o gráfico.
                    branchvalues = 'total', #determina como os itens em valores são somados. 
                    color_discrete_sequence= px.colors.sequential.Plasma_r,  #mudar a textura de cor do gráfico 
                    maxdepth=2) #divisões do gráfico

fig_sunburst.update_traces(hovertemplate='<b>%{label}</b> <br> Feridos: %{value}<br>',
                    insidetextorientation='radial', 
                    textfont_color='#aaaaaa', 
                    selector=dict(type='sunburst'))

                    
fig_sunburst.update_layout(plot_bgcolor="#272b30",paper_bgcolor="#272b30",margin=dict(l=50, r=50, t=50, b=50)) #características do layout do gráfico                                
 

app = dash.Dash()
app.layout = html.Div( children=[
    html.H1(children='Feridos por tipo de acidentes', style={'textAlign': 'center',}),  #característicacs de layout na página html,título,sub-título,centralização e estilo da fonte
    html.Div(children=
        'Quantidade de feridos de cada tipo de acidentes por mês de 2020.'
    ,style={'textAlign': 'center',}),
    dcc.Graph(id='sunburst-graph',figure=fig_sunburst) #criando identidade pro gráfico 
])




#Barra - Causas

df = pd.read_csv('datatran.2020.csv', sep=";")

df_lista = df.values.tolist() 


def separar_coluna(df_lista, num_coluna):                                                      #Argumentos sao a tabela em formato de lista
                                                                                               # e o numero da coluna que voce quer retirar da tabela
    conteudo_coluna = []                                                                       # Inserindo coluna vazia para receber os valores da coluna desejada

    for i in df_lista:                                                                         # o i percorre a lista e quando ele chegar no indice desejado 
        conteudo_coluna.append(i[num_coluna])                                                  # ele adiciona na coluna vazia
    
    return conteudo_coluna     



def excluir_duplicado(coluna_valor_duplicado):                                                # Funcao para excluir valor duplicado
                                                                                              # Os argumentos sao: 
  lista_valor_unico = []                                                                      #a coluna que possui os valores duplicados

  for i in range (len(coluna_valor_duplicado)):                                               #laco possui o tamanho da coluna que vai ser unificada para verficar todos os valores
                                                                                              # A condicao estabelecida verfica se todos os valores da coluna duplicada
      if coluna_valor_duplicado[i] not in lista_valor_unico:                                  # estao na coluna criada, caso nao esteja, ele adiciona nessa coluna onde nao possui                                                                                              # ele adiciona esse valor
         lista_valor_unico.append(coluna_valor_duplicado[i])                                  #valores repetidos
  
  return lista_valor_unico  





dias_semana = separar_coluna(df_lista,2)

dias_semana_single = excluir_duplicado(dias_semana)

periodo = separar_coluna(df_lista,8)

periodo_single = excluir_duplicado(periodo)




def acidente_dia_periodo(lista, arg, periodo_acidente):
    periodo = []
    dia_sem = 0

    

    for linha in lista:

        if linha[2] == arg and linha[8] == periodo_acidente:
            dia_sem += 1
    
    periodo.append(arg)
    periodo.append(dia_sem)
    periodo.append(periodo_acidente)
    
    return periodo



def lista_dias (periodo_single,lista, arg):
    dia_list = []

    for i in periodo_single:
        dia_list.append(acidente_dia_periodo(lista,arg,i))
    
    return dia_list



segunda = lista_dias(periodo_single,df_lista, 'segunda')
terca = lista_dias(periodo_single,df_lista, 'terça')
quarta = lista_dias(periodo_single,df_lista, 'quarta')
quinta = lista_dias(periodo_single,df_lista, 'quinta')
sexta = lista_dias(periodo_single,df_lista, 'sexta')
sabado = lista_dias(periodo_single,df_lista, 'sábado')
domingo = lista_dias(periodo_single,df_lista, 'domingo')


dias = segunda + terca + quarta + quinta + sexta + sabado + domingo
colunas = ['dias_Semana', 'quantidade', 'causas']



with open('causas.csv', 'w', encoding='UTF8', newline='') as f:
     writer = csv.writer(f)
     writer.writerow(colunas)
     writer.writerows(dias)


df = pd.read_csv('causas.csv')


#Barra - Período



dias_semana = separar_coluna(df_lista,2)

dias_semana_single = excluir_duplicado(dias_semana)

periodo = separar_coluna(df_lista,11)

periodo_single = excluir_duplicado(periodo)




def acidente_dia_periodo(lista, arg, periodo_acidente):
    periodo = []                                                        #PERCORRE A LISTA E VERIFICA SE O ARGUMENTO INSERIDO E IGUAL AO
    dia_sem = 0                                                         #ELEMENTO ANALISADO EM UM DETERMINADA PERIODO TAMBEM INSERIDO,
                                                                        #CASO ESSA VERIFICACAO SEJA SATISFEITA, E ADICIONADO 1 NO CONTADOR
                                                                        #DO NUMERO DE ACIDENTES
                                                                        #RETORNA O NUMERO DE ACIDENTES PELOS DIAS DA SEMANA EM UM DETERMINADO
    for linha in lista:                                                 #PERIODO                                
                                                                        #EXEMPLO: ['segunda', 2667, 'Plena Noite']
        if linha[2] == arg and linha[11] == periodo_acidente:
            dia_sem += 1
    
    periodo.append(arg)
    periodo.append(dia_sem)
    periodo.append(periodo_acidente)
    
    return periodo



def lista_dias (periodo_single,lista, arg):                             #E FEITA A JUNCAO DOS DADOS FILTRADOS ACIMA PARA CADA DIA DA SEMANA
    dia_list = []                                                       # OBTENDO POR EXEMPLO: [SEGUNDA, 234, PLENA NOITE
                                                                        #                       SEGUNDA, 222, PLENO DIA
    for i in periodo_single:                                            #                       SEGUNDA, 222, AMANHECER
        dia_list.append(acidente_dia_periodo(lista,arg,i))              #                       SEGUNDA, 222, ANOITECER]
                                                                        #PERCORRE A LISTA DOS PERIODOS E UTILIZA O ELEMENTO ANALISADO NA FUNCAO ANTERIOR
    return dia_list



segunda = lista_dias(periodo_single,df_lista, 'segunda')
terca = lista_dias(periodo_single,df_lista, 'terça')
quarta = lista_dias(periodo_single,df_lista, 'quarta')
quinta = lista_dias(periodo_single,df_lista, 'quinta')
sexta = lista_dias(periodo_single,df_lista, 'sexta')
sabado = lista_dias(periodo_single,df_lista, 'sábado')
domingo = lista_dias(periodo_single,df_lista, 'domingo')


dias = segunda + terca + quarta + quinta + sexta + sabado + domingo
colunas = ['Dias da Semana', 'Quantidade', 'Periodo']



with open('nova_basedados.csv', 'w', encoding='UTF8', newline='') as f:
     writer = csv.writer(f)
     writer.writerow(colunas)
     writer.writerows(dias)

nova_df = pd.read_csv('nova_basedados.csv')
fig = px.bar(nova_df, x='Dias da Semana', 
                      y = 'Quantidade', 
                      color='Periodo' , 
                      barmode='group')

opcoes = list(nova_df['Periodo'].unique())                                  #LISTA DE ITENS PARA O DROPDOWN
opcoes.append('Todos os períodos')

#Mapa Coroplético

newdata = pd.read_csv('newdata.csv') 
brasil_states = json.load(open("brazil_geo.json", "r"))

def calculo_mortes(data_list, uf): 
    mortos_estado = [] 
    for linha in data_list:
        if linha[4] == uf:  
            mortos_estado.append(linha[18]) 


    return sum(mortos_estado) 


def calculo_feridos(data_list, uf): 
    feridos_estado = [] 
    for linha in data_list:
        if linha[4] == uf:    
            feridos_estado.append(linha[23])


    return sum(feridos_estado) 

def estado(data_list, num_coluna):
    lista2 = []
    lista_estados =[]
    for i in data_list:
        lista2.append(i[num_coluna])
    for i in lista2:
        if i not in lista_estados:
            lista_estados.append(i)
    lista_estados.sort()

    return lista_estados    

estados = (estado(data_list,4))            


soma_mortes = []
soma_feridos = []
geral = []
for i in estados:
    mortes = calculo_mortes(data_list, i) 
    feridos = calculo_feridos(data_list, i) 
    total = mortes + feridos 

    geral.append(total) 
    soma_mortes.append(mortes) 
    soma_feridos.append(feridos) 

 
dados = [] 
for i in range (len(geral)):
    dados.append([soma_mortes[i], soma_feridos[i], geral[i], estados[i]]) 


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

app.layout = html.Div(children=[

    #Barra - Causas por dia

    html.H1(children='Acidentes rodoviarios no brasil em 2020', style={'textAlign': 'center',}),

    html.H2(children ='Causas', style={'textAlign': 'center',}),
        html.P(children ='Selecione a causa a ser analisada:', style={'textAlign': 'center',}),
                dcc.Dropdown(id='selecione_causa', options=[{'label': x, 'value': x }
                    for x in sorted (df.causas.unique())],
                
                    value ='Animais na Pista'),

                dcc.Graph(id = 'my_graph', figure= {}),
                
    #Barra - Acidentes por período

    html.H2(children='Acidentes por periodo', style={'textAlign': 'center',}),
        html.P(children ='Selecione o período do dia:', style={'textAlign': 'center',}),
                dcc.Dropdown(opcoes, value='Todos os períodos', id='botao-dropdown'),
                dcc.Graph(
        id='grafico-periodo',                                            
        figure=fig),

    #Sunburst

    html.H2(children='Feridos por tipo de acidentes', style={'textAlign': 'center',}),  #característicacs de layout na página html,título,sub-título,centralização e estilo da fonte
        html.Div(children=
            'Quantidade de feridos de cada tipo de acidentes por mês de 2020.', style={'textAlign': 'center',}),
        dcc.Graph(id='sunburst-graph',figure=fig_sunburst), #criando identidade pro gráfico 

    #Coroplético

    html.H2('Acidentes rodoviários 2020', style={'textAlign': 'center',}), #Tag de Cabeçalho – onde h1 tem um tamanho maior, que vai diminuindo até chegar no h6.
        html.P("Selecione o parâmetro", style={'textAlign': 'center',}), # Tag de parágrafo
    
    dcc.RadioItems(  # o input do tipo "radioitems" se refere a um elemento que possui opções que podem ser marcadas ou desmarcadas, caracterizadas por um pequeno círculo ao lado do texto.
        id='cor',   #identificação
        options=[
       {'label': 'Mortos', 'value': 'Mortos'},
       {'label': 'Feridos', 'value': 'Feridos'},
       {'label': 'Total de acidentados', 'value': 'Total'},
   ], #opções a serem marcadas
        value="Total", #correspondência (depende da opção escolhida pelo usuário)
        inline=True, #(opções alinhadas lado a lado)
        style={'textAlign': 'center',}   
    ),


    dcc.Graph(id="mapa"), #Criação de um gráfico

])






@app.callback(
    Output(component_id='grafico-periodo',component_property='figure'),  
    Output(component_id='my_graph', component_property='figure'),
    Output(component_id="mapa",component_property="figure"),
    Input(component_id='botao-dropdown',component_property='value'),
    Input(component_id= 'selecione_causa', component_property='value'),
    Input(component_id="cor",component_property="value")                        
)



def update_output(value, causas, cor):
    
    dff = df[df.causas==causas]
    fig2 = px.bar(data_frame = dff, x = 'dias_Semana', y = 'quantidade')

    fig2.update_layout(plot_bgcolor="#272b30",paper_bgcolor="#272b30")
    fig2.update_xaxes(color='#aaaaaa')
    fig2.update_yaxes(color='#aaaaaa')
#==========================================================================================
    if value == 'Todos os períodos':

        fig = px.bar(nova_df, x='Dias da Semana', 
                            y = 'Quantidade', 
                            color='Periodo' , 
                            barmode='group',
                            )


        fig.update_layout(plot_bgcolor="#272b30",paper_bgcolor="#272b30",legend_title_font_color="#aaaaaa", font_color="#aaaaaa")
        fig.update_xaxes(color='#aaaaaa')
        fig.update_yaxes(color='#aaaaaa')
    else:

        tabela_filtrada = nova_df.loc[nova_df['Periodo'] == value, :]       #SE O VALOR SELECIONADO NAO FOR TODOS OS PERIODOS
        fig = px.bar(tabela_filtrada, x='Dias da Semana',                   #AS LINHAS QUE DEVERAO SER ANALISADAS SOMENTE SAO AS
                            y = 'Quantidade',                               #QUE SAO PERTENCENTES AOS VALORES INDICADO NO FILTRO
                            color='Periodo' , 
                            barmode='group',
                            )
                            
        fig.update_layout(plot_bgcolor="#272b30",paper_bgcolor="#272b30",legend_title_font_color="#aaaaaa", font_color="#aaaaaa")
        fig.update_xaxes(color='#aaaaaa')
        fig.update_yaxes(color='#aaaaaa')
#==========================================================================================

    df_mapa = newdata # cópia da base de dados para não alterar a original
    geojson = brasil_states # cópia do arquivo geojson para não alterar o original

    if cor == 'Mortos':  #se a opçao 'mortos' for selecionada, o mapa terá a seguinte aparência:
        fig_mapa = px.choropleth_mapbox(df_mapa, geojson=geojson, locations='UF', color = cor,
                            color_continuous_scale="Burg",                                                
                            center = {"lat": -13.6128, "lon": -48.5920}, 
                            range_color=(0, 530), 
                            zoom=3, 
                            opacity=0.4,   
                            hover_data={'Mortos': True, 'Feridos': False, 'Total': False, 'UF': True}   #define o que vai ser mostrado ao passar o mouse                 
    )   

    elif cor == 'Feridos': # Mas se a opçao 'feridos' for selecionada, o mapa terá a seguinte aparência:
        fig_mapa = px.choropleth_mapbox(df_mapa, geojson=geojson, locations='UF', color = cor,
                            color_continuous_scale="Burg",                                                
                            center = {"lat": -13.6128, "lon": -48.5920}, 
                            range_color=(0, 10000), 
                            zoom=3, 
                            opacity=0.4,   
                            hover_data={'Mortos': False, 'Feridos': True, 'Total': False, 'UF': True}   #define o que vai ser mostrado ao passar o mouse                 
    )   

    else:  # Por fim se a opçao 'total' for selecionada, o mapa terá a seguinte aparência:
        fig_mapa = px.choropleth_mapbox(df_mapa, geojson=geojson, locations='UF', color = cor,
                            color_continuous_scale="Burg",                                                
                            center = {"lat": -13.6128, "lon": -48.5920}, 
                            range_color=(0, 10000), 
                            zoom=3, 
                            opacity=0.4,   
                            hover_data={'Mortos': False, 'Feridos': False, 'Total': True, 'UF': True}    #define o que vai ser mostrado ao passar o mouse                
    )   




    fig_mapa.update_layout(
        mapbox_style="carto-darkmatter", #estilo
        autosize= True, #ajuste na tela
        margin=go.layout.Margin(l=300, r=300, t=0, b=0),
        plot_bgcolor="#272b30",
        paper_bgcolor="#272b30",
        legend_title_font_color="#aaaaaa",
         font_color="#aaaaaa"
    ) 

    return fig, fig2, fig_mapa


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)