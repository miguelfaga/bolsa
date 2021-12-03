import dash
from datetime import date
from dash import dcc
from dash import html

from dash.dependencies import Input, Output

import plotly.express as px
import pandas as pd
    
import requests
import json

app = dash.Dash(__name__)  

app.layout = html.Div(children=[    #cria o layout da aplicação
    html.H1(children="Ações"),  #título
    html.Div("Insira o código da ação:"),
    dcc.Input(id='code-input', type='text'),
    html.Div(children=["Escolha um período para ver a cotação:" #uma Div
    ]),

    dcc.DatePickerRange(    #campo tipo calendário para escolha da data
            display_format='DD/MM/YYYY',
            start_date_placeholder_text= 'DD/MM/AAAA',
            end_date_placeholder_text = 'DD/MM/AAAA',
            id='my-date-picker-range'
),
    dcc.Graph(
        id='output-container-date-picker-range') #espaço para plotagem do gráfico
])

@app.callback(
    Output('output-container-date-picker-range', 'figure'), #a tag id relaciona a figura com o dcc (dash core component) Graph definido acima
    Input('code-input', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')) #cada elemento de Input e Output identificado pela tag id tem um valor armazenado nas variáveis indicadas no callback

def update_output(code, start_date, end_date): #a função que envolve o decorador de callback é acionada automaticamente caso o valor do input se altere
    '''Os parâmetros estão na mesma ordem da declaração de variáveis no decorador'''

    def grafico_acao(data_inicio, data_fim, acao="ETER3"):
    
        link = "https://www.okanebox.com.br/api/acoes/hist/" + acao + "/"+ data_inicio + "/"+ data_fim

        r = requests.get(link) #chamada da API
        page_json = json.loads(r.text) #load do json

        selected_data = {"DATE":[],
                         "PRICE":[]
                         }

        for data in page_json:
            selected_data["DATE"].append(data['DATPRG'][:10])
            selected_data["PRICE"].append(data['PREMED'])
    
        dataframe = pd.DataFrame.from_dict(selected_data) #criação do dataframe com data e valor médio
        print(dataframe)

        fig = px.line(dataframe, x="DATE", y="PRICE", title=acao) #criação expressa da curva

        fig.update_layout(transition_duration=500) 

        return fig

    if start_date == None or end_date== None:
        return "Nada a declarar." 
    start_date_object = date.fromisoformat(start_date)
    start_date_string = start_date_object.strftime('%Y%m%d') #transforma o objeto data em string
    end_date_object = date.fromisoformat(end_date)
    end_date_string = end_date_object.strftime('%Y%m%d')
    code = code.upper()
    fig = grafico_acao(start_date_string, end_date_string, acao=code) #chama função para chamar API e gerar o gráfico
    return fig #plotagem do gráfico

if __name__ == '__main__':
    app.run_server() #roda a aplicação





