import pandas as pd
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output

# Acesso em http://127.0.0.1:8080/

# Iniciando a aplicação
app = dash.Dash(external_stylesheets=[dbc.themes.LITERA])

# Dataframe
df = pd.read_csv('dados.csv', index_col=0)
df.rename(columns={'País': 'Pais', 'Preço Médio': 'Preco Medio', 'Número': 'Numero'}, inplace=True)

# Mapa
bubble_map = px.scatter_geo(df, locations='Pais', locationmode='country names', hover_name='Pais', size='Numero',
                            size_max=80, projection='orthographic', color_discrete_sequence=px.colors.sequential.RdBu)

# Layout da página
app.layout = dbc.Container(
    [
        html.H1('Análise dos dados de vinhos', style={'textAlign': 'center'}),

        html.Hr(),

        dbc.Row(  # Linha dos filtros
            [
                dbc.Col(  # Coluna com a caixa de opções
                    dbc.Select(
                        id='select',
                        options=[
                            {'label': 'Todos', 'value': 'Todos'},
                            {'label': '40', 'value': '40'},
                            {'label': '30', 'value': '30'},
                            {'label': '20', 'value': '20'}
                        ],
                        value='Todos', style={'padding': '5px'}
                    ),
                ),
                dbc.Col(  # Coluna com checkbox
                    dbc.Checklist(
                        id='checkbox',
                        options=[
                            {'label': 'Mostrar 5 maiores?', 'value': True}
                        ]
                    ),
                )
            ]
        ),
        dbc.Row(  # Linha dos gráficos
            [
                dbc.Col(  # Coluna do gráfico de preço médio
                    html.Div(
                        id='grafico-1',
                        style={'padding': '5px'}
                    ), width=6
                ),
                dbc.Col(  # Coluna do gráfico de número de vinhos
                    html.Div(
                        id='grafico-2',
                        style={'padding': '5px'}
                    ), width=6
                )
            ]
        ),
        dbc.Row(  # Linha da checkbox para habilitar barras para grafico 1
            [
                dbc.Col(
                    dbc.Checklist(
                        id='check-2',
                        options=[
                            {'label': 'Apresentar gráfico de barras para preço médio?', 'value': True}
                        ]
                    )
                )
            ]
        ),

        html.Hr(),

        html.H3('Países produtores pelo mundo', style={'textAlign': 'center'}),

        dbc.Row(  # Gráfico do mundo
            [
                dbc.Col(
                    html.Div(
                        dcc.Graph(id='bubble_graph',
                                  figure=bubble_map)
                    ),
                )
            ]
        ),

        # html.Img(src=app.get_asset_url('download.jfif'))

    ], fluid=True
)


# CALLBACKS DE ATUALIZAÇÃO DE GRÁFICOS
@app.callback(  # Callback para o gráfico de preço médio
    Output(component_id='grafico-1', component_property='children'),
    [Input(component_id='select', component_property='value'),
     Input(component_id='check-2', component_property='value')]
)
def update_graph(input_value, check):
    if not check:  # Mostra pie chart se não estiver checado
        if input_value == 'Todos':
            df_preco_medio = df.sort_values('Preco Medio', ascending=False)[:5]
            fig = px.pie(df_preco_medio, values='Preco Medio', names='Pais', title='5 países com o maior preço médio',
                         template='presentation', color_discrete_sequence=px.colors.sequential.RdBu)
            fig.update_traces(textinfo='percent', marker={'line': {'color': 'black', 'width': 4}}, opacity=0.85)
            return dcc.Graph(figure=fig)
        else:
            df_preco_medio = df[df['Preco Medio'] <= int(input_value)].sort_values('Preco Medio', ascending=False)[:5]
            fig = px.pie(df_preco_medio, values='Preco Medio', names='Pais', template='presentation',
                         color_discrete_sequence=px.colors.sequential.RdBu,
                         title='5 países com o maior preço médio até US${}'.format(input_value))
            fig.update_traces(textinfo='percent', marker={'line': {'color': 'black', 'width': 4}}, opacity=0.85)
            return dcc.Graph(figure=fig)
    else:  # Apresenta gráfico de barras se checar
        if input_value == 'Todos':
            df_preco_medio = df.sort_values('Preco Medio', ascending=False)[:5]
            fig = px.bar(df_preco_medio, y='Preco Medio', x='Pais', title='5 países com o maior preço médio',
                         template='presentation', color='Pais', color_discrete_sequence=px.colors.sequential.RdBu)
            return dcc.Graph(figure=fig)
        else:
            df_preco_medio = df[df['Preco Medio'] <= int(input_value)].sort_values('Preco Medio', ascending=False)[:5]
            fig = px.bar(df_preco_medio, y='Preco Medio', x='Pais', template='presentation',
                         title='5 países com o maior preço médio até US${}'.format(input_value),
                         color='Pais', color_discrete_sequence=px.colors.sequential.RdBu)
            return dcc.Graph(figure=fig)


@app.callback(  # Callback para o gráfico de número de vinhos
    Output(component_id='grafico-2', component_property='children'),
    Input(component_id='checkbox', component_property='value')
)
def update_graph(check):
    if not check:
        df_numero = df.sort_values('Numero')[:5]
        fig = px.pie(df_numero, values='Numero', names='Pais', template='presentation',
                     title='5 países com menor número de vinhos', color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_traces(textinfo='percent', marker={'line': {'color': 'black', 'width': 4}}, opacity=0.85)
        return dcc.Graph(figure=fig)
    else:
        df_numero = df.sort_values('Numero', ascending=False)[:5]
        fig = px.pie(df_numero, values='Numero', names='Pais', template='presentation',
                     title='5 países com maior número de vinhos', color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_traces(textinfo='percent', marker={'line': {'color': 'black', 'width': 4}}, opacity=0.85)
        return dcc.Graph(figure=fig)


# Inicialização do servidor
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=8080)
