# Dashboard profissional com Dash (Plotly)
# Execute com: python dashboard_dash.py
# Requer: dash, dash-bootstrap-components, plotly, pillow, nltk

import dash
from dash import html, dcc
from dash import dash_table, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import nltk
import re
from collections import Counter
import base64
from wordcloud import WordCloud
from nltk.corpus import stopwords

# Adiciona CSS customizado para visual moderno e responsivo
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, "https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap", "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css"])
app.title = 'Dashboard Debate IFES'

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body, .app-container, .dash-table-container, .dash-table, .dash-table-container .dash-spreadsheet-container {
                font-family: 'Poppins', sans-serif;
                background-color: #18191A;
                color: #F5F6FA;
            }
            .main-header {
                font-size: 2.5rem;
                font-weight: 600;
                margin-bottom: 0.5rem;
                text-align: center;
                color: #A259F7;
            }
            .main-subtitle {
                font-size: 1.2rem;
                margin-bottom: 1.5rem;
                text-align: center;
                color: #B0BEC5;
            }
            .carousel-title {
                font-size: 1.5rem;
                font-weight: 500;
                margin-bottom: 1rem;
                text-align: center;
                color: #F5F6FA;
            }
            .nuvem-img {
                width: 100%;
                height: auto;
                border-radius: 16px;
                box-shadow: 0 0 10px #a259f7aa;
                margin-bottom: 1em;
            }
            .busca-box {
                display: flex;
                align-items: center;
                background: #23272F;
                border-radius: 8px;
                padding: 0.5em 1em;
                margin-bottom: 1em;
            }
            .busca-input {
                flex: 1;
                background: transparent;
                border: none;
                color: #F5F6FA;
                font-size: 1.1em;
                outline: none;
            }
            .busca-icon {
                color: #A259F7;
                font-size: 1.3em;
                margin-left: 0.5em;
            }
            .transcricao-box {
                max-height: 300px;
                overflow-y: auto;
                padding-right: 10px;
            }
            .custom-card {
                background: #181828;
                border-radius: 16px;
                box-shadow: 0 0 10px #a259f7aa;
                padding: 1.5em;
                margin-bottom: 2em;
            }
            .download-btn {
                color: #A259F7;
                text-decoration: none;
                font-weight: 600;
                margin-top: 1em;
                display: inline-block;
            }
            .download-btn:hover {
                color: #F76E11;
            }
            .grafico-card {
                background: #181828;
                border-radius: 16px;
                box-shadow: 0 0 10px #a259f7aa;
                padding: 1.5em;
            }
            .ranking-table {
                margin-top: 1em;
            }
            .tutorial-list {
                padding-left: 1.5rem;
                margin-top: 0.5rem;
            }
            .tutorial-list li {
                margin-bottom: 0.8rem;
                font-size: 1.1rem;
            }
            .tutorial-section {
                background-color: rgba(162, 89, 247, 0.12);
                backdrop-filter: blur(2px);
                border-radius: 16px;
                padding: 1.5rem;
                margin-top: 1rem;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

def carregar_transcricao():
    with open('data/transcricao.txt', 'r', encoding='utf-8') as f:
        return f.read()

def get_nuvem_base64():
    with open('imgs/nuvem_geral.png', 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode()

def grafico_palavras(transcricao):
    nltk.download('stopwords', quiet=True)
    stopwords_pt = set(stopwords.words('portuguese'))
    texto_limpo = re.sub(r'\[\d{2}:\d{2}\]', '', transcricao)
    palavras = re.findall(r'\b\w+\b', texto_limpo.lower())
    palavras_filtradas = [p for p in palavras if p not in stopwords_pt and len(p) > 2]
    contagem = Counter(palavras_filtradas)
    mais_comuns = contagem.most_common(20)
    if mais_comuns:
        palavras_, freq_ = zip(*mais_comuns)
        fig = go.Figure(go.Bar(
            x=freq_,
            y=palavras_,
            orientation='h',
            marker=dict(color='#4F8DFD'),
            hoverinfo='x+y',
        ))
        fig.update_layout(
            height=400,
            plot_bgcolor='#23272F',
            paper_bgcolor='#18191A',
            font=dict(color='#F5F6FA', size=16),
            margin=dict(l=80, r=20, t=40, b=40),
            xaxis=dict(title='Frequência', color='#F5F6FA', showgrid=False),
            yaxis=dict(title='', color='#F5F6FA', showgrid=False, autorange='reversed'),
            showlegend=False
        )
        return fig
    else:
        return go.Figure()

def dividir_blocos(linhas):
    n = len(linhas)
    bloco1 = linhas[:n//3]
    bloco2 = linhas[n//3:2*n//3]
    bloco3 = linhas[2*n//3:]
    return bloco1, bloco2, bloco3

def grafico_evolucao(linhas):
    minutos = []
    for l in linhas:
        ts = re.findall(r'\[(\d{2}):(\d{2})\]', l)
        if ts:
            m, s = map(int, ts[0])
            minutos.append(m)
    if not minutos:
        return go.Figure()
    contagem = pd.Series(minutos).value_counts().sort_index()
    fig = go.Figure(go.Scatter(
        x=contagem.index,
        y=contagem.values,
        mode='lines+markers',
        line=dict(color='#A259F7', width=3),
        marker=dict(size=8, color='#F76E11')
    ))
    fig.update_layout(
        title='Evolução Temporal: Falas por Minuto',
        xaxis_title='Minuto',
        yaxis_title='Nº de Falas',
        plot_bgcolor='#23272F',
        paper_bgcolor='#18191A',
        font=dict(color='#F5F6FA'),
        margin=dict(l=40, r=20, t=40, b=40)
    )
    return fig

def duracao_media(linhas):
    tempos = []
    for l in linhas:
        ts = re.findall(r'\[(\d{2}):(\d{2})\]', l)
        if ts:
            m, s = map(int, ts[0])
            tempos.append(m*60+s)
    if len(tempos) < 2:
        return 0
    diffs = np.diff(tempos)
    return np.mean(diffs)

def nuvem_bloco(linhas_bloco, nome_arquivo):
    nltk.download('stopwords', quiet=True)
    stopwords_pt = set(stopwords.words('portuguese'))
    texto = ' '.join([re.sub(r'\[\d{2}:\d{2}\]', '', l) for l in linhas_bloco])
    wc = WordCloud(width=1200, height=600, background_color='#18191A', colormap='plasma', stopwords=stopwords_pt,
                  max_words=150, min_font_size=10, prefer_horizontal=0.95, relative_scaling=0.5).generate(texto)
    wc.to_file(nome_arquivo)
    with open(nome_arquivo, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode()

def tabela_palavras(transcricao):
    nltk.download('stopwords', quiet=True)
    stopwords_pt = set(stopwords.words('portuguese'))
    texto_limpo = re.sub(r'\[\d{2}:\d{2}\]', '', transcricao)
    palavras = re.findall(r'\b\w+\b', texto_limpo.lower())
    palavras_filtradas = [p for p in palavras if p not in stopwords_pt and len(p) > 2]
    contagem = Counter(palavras_filtradas)
    df = pd.DataFrame(contagem.items(), columns=['Palavra', 'Frequência']).sort_values('Frequência', ascending=False)
    return df

def busca_transcricao(linhas, termo):
    termo = termo.lower()
    return [l for l in linhas if termo in l.lower()]

def gerar_download(texto):
    return dict(content=texto, filename="transcricao_debate.txt")

transcricao = carregar_transcricao()
linhas = transcricao.strip().split('\n')
nuvem_base64 = get_nuvem_base64()
fig_palavras = grafico_palavras(transcricao)

# --- Preparação dos dados ---
bloco1, bloco2, bloco3 = dividir_blocos(linhas)
nuvem1 = nuvem_bloco(bloco1, 'imgs/nuvem_bloco1.png')
nuvem2 = nuvem_bloco(bloco2, 'imgs/nuvem_bloco2.png')
nuvem3 = nuvem_bloco(bloco3, 'imgs/nuvem_bloco3.png')
fig_evolucao = grafico_evolucao(linhas)
duracao = duracao_media(linhas)
df_palavras = tabela_palavras(transcricao)

# Carrossel de nuvens de palavras
carousel_items = [
    {"key": "1", "src": f"data:image/png;base64,{nuvem1}"},
    {"key": "2", "src": f"data:image/png;base64,{nuvem2}"},
    {"key": "3", "src": f"data:image/png;base64,{nuvem3}"},
]

app.layout = dbc.Container([
    html.Div([
        html.H1('Dashboard do Debate IFES', className='main-header'),
        html.Div('Análise de transcrição e frequência de palavras', className='main-subtitle'),
    ]),
    html.Div([
        dbc.Carousel(
            id='carousel-nuvens',
            items=carousel_items,
            controls=True,
            indicators=True,
            interval=4000,
            style={'maxWidth': '900px', 'margin': '0 auto', 'background': '#181828', 'borderRadius': '16px', 'boxShadow': '0 0 10px #a259f7aa', 'padding': '1em', 'overflow':'visible'}
        ),
    ], style={'marginBottom': '2em'}),
    html.Div([
        html.Div('Nuvem Geral', className='carousel-title'),
        html.Img(src=f'data:image/png;base64,{nuvem_base64}', className='nuvem-img', id='nuvem-geral-img', style={'display': 'block', 'margin': '0 auto', 'maxWidth': '900px'}),
    ], style={'marginBottom': '2em'}),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div('Transcrição', className='carousel-title', style={'textAlign': 'left'}),
                html.Div([
                    html.Div([
                        dcc.Input(id='busca-termo', type='text', placeholder='Buscar...', className='busca-input'),
                        html.I(className='bi bi-search busca-icon')
                    ], className='busca-box'),
                    html.Div(id='resultado-busca', style={'marginBottom': '1em'}),
                    html.Div([
                        html.Div([
                            html.Span(l.split(']')[0] + ']', style={'color': '#a259f7', 'fontWeight': 'bold', 'marginRight': '0.5em'}),
                            html.Span(l.split(']')[1].strip(), style={'color': '#F5F6FA'})
                        ], style={'marginBottom': '0.7em', 'padding': '0.5em 0.7em', 'background': '#222', 'borderRadius': '8px', 'display': 'flex', 'alignItems': 'baseline'})
                        for l in linhas if ']' in l
                    ], className='transcricao-box'),
                    html.A([
                        html.I(className='bi bi-download'),
                        ' Baixar Transcrição'
                    ], id='download-link', download='transcricao_debate.txt', href='data:text/plain;charset=utf-8,' + transcricao, target='_blank', className='download-btn')
                ])
            ], className='custom-card', style={'maxWidth': '700px', 'margin': '0 auto'})
        ], md=6),
        dbc.Col([
            html.Div([
                html.Div('Evolução Temporal das Palavras', className='carousel-title'),
                html.Div([
                    dcc.Graph(figure=fig_evolucao, config={'displayModeBar': False})
                ], className='grafico-card', style={'maxWidth':'900px'})
            ], style={'maxWidth': '900px', 'margin': '0 auto'})
        ], md=6)
    ], style={'marginBottom': '2em'}),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div('Palavras com Maior Frequência', className='carousel-title'),
                html.Div([
                    dcc.Graph(figure=fig_palavras, config={'displayModeBar': False})
                ], className='grafico-card', style={'maxWidth':'900px'})
            ], style={'maxWidth': '900px', 'margin': '0 auto'})
        ], md=6),
        dbc.Col([
            html.Div([
                html.Div('Ranking de Palavras (Todas Etapas)', className='carousel-title'),
                html.Div([
                    dash_table.DataTable(
                        id='tabela-palavras',
                        columns=[{"name": i, "id": i} for i in df_palavras.columns],
                        data=df_palavras.to_dict('records'),
                        filter_action='native',
                        sort_action='native',
                        page_size=10,
                        style_table={'backgroundColor':'#181828', 'borderRadius':'12px', 'overflow':'hidden'},
                        style_header={'backgroundColor':'#2d1847', 'color':'#fff', 'fontWeight':'bold'},
                        style_cell={'backgroundColor':'#181828', 'color':'#f0f0f0', 'fontSize':16, 'textAlign':'center'},
                        style_data_conditional=[
                            {'if': {'row_index': 'even'}, 'backgroundColor': '#23272F'},
                        ],
                    )
                ], className='ranking-table')
            ], style={'maxWidth': '900px', 'margin': '0 auto'})
        ], md=6)
    ], style={'marginBottom': '2em'}),
    html.Div([
        dbc.Accordion([
            dbc.AccordionItem([
                html.Ul([
                    html.Li([
                        html.I(className='bi bi-check-circle'),
                        html.Span('Explore as Nuvens de Palavras por Etapas — Acesse a análise por trechos (início, meio e fim) no carrossel interativo. Use as setas ou aguarde a rotação automática. Assim, você visualiza como a linguagem evolui ao longo do debate.')
                    ]),
                    html.Li([
                        html.I(className='bi bi-arrow-repeat'),
                        html.Span('Veja a Nuvem Geral — A nuvem central resume os termos mais usados em toda a transcrição. É uma visão ampla do vocabulário predominante.')
                    ]),
                    html.Li([
                        html.I(className='bi bi-search'),
                        html.Span('Pesquise na Transcrição — Use o campo de busca para localizar palavras específicas no texto completo. Isso ajuda a encontrar momentos-chave do debate.')
                    ]),
                    html.Li([
                        html.I(className='bi bi-graph-up'),
                        html.Span('Analise a Linha do Tempo — O gráfico temporal mostra quando os participantes mais falaram. Ideal para identificar picos de discussão.')
                    ]),
                    html.Li([
                        html.I(className='bi bi-bar-chart'),
                        html.Span('Confira a Frequência das Palavras — Visualize as palavras mais mencionadas por meio do gráfico de barras. Cada barra representa a intensidade de uso.')
                    ]),
                    html.Li([
                        html.I(className='bi bi-trophy'),
                        html.Span('Consulte o Ranking de Palavras — A tabela classifica os termos por frequência total. Útil para entender quais palavras dominaram a conversa.')
                    ]),
                    html.Li([
                        html.I(className='bi bi-phone'),
                        html.Span('Use o Dashboard em Qualquer Dispositivo — A página é responsiva: ela se adapta automaticamente ao seu celular, tablet ou computador.')
                    ]),
                ], className='tutorial-list')
            ], title='Como Usar Esta Dashboard', style={'background': 'rgba(162,89,247,0.12)', 'backdropFilter': 'blur(2px)', 'borderRadius': '16px'})
        ], start_collapsed=True, className='tutorial-section')
    ], style={'maxWidth': '900px', 'margin': '0 auto', 'marginBottom': '2em'})
], fluid=True, style={'paddingBottom':'40px', 'paddingTop':'20px', 'paddingLeft':'2vw', 'paddingRight':'2vw'})

@app.callback(
    Output('resultado-busca', 'children'),
    Input('busca-termo', 'value')
)
def atualizar_busca(termo):
    if termo:
        resultados = [l for l in linhas if termo.lower() in l.lower()]
        if resultados:
            return html.Pre('\n'.join(resultados), style={'backgroundColor':'#23272F', 'color':'#F5F6FA', 'padding':'10px', 'borderRadius':'8px', 'fontSize':'1em'})
        else:
            return html.P('Nenhum resultado encontrado.', style={'color':'#F76E11'})
    return ''

if __name__ == '__main__':
    app.run(debug=True)
