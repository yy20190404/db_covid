

import os
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import dldata
import time

dldata.down_load()
time.sleep(10)

DIRCSV = 'static/csv/'
CSV_FILES = ('covid19_ww_confirmed_global.csv',
            'covid19_ww_deaths_global.csv',
            'covid19_ww_recovered_global.csv',
            'covid19_jp_prf_cfm.csv',
            'covid19_jp_prf_dth.csv',
            'covid19_jp_prf_rcv.csv',
            'covid19_jp_prf_male.csv',
            'covid19_jp_prf_female.csv',
            'covid19_jp_prf_gen.csv')

df0 = pd.read_csv(DIRCSV + CSV_FILES[0])
df1 = pd.read_csv(DIRCSV + CSV_FILES[1])
df2 = pd.read_csv(DIRCSV + CSV_FILES[2])
df3 = pd.read_csv(DIRCSV + CSV_FILES[3])
df4 = pd.read_csv(DIRCSV + CSV_FILES[4])
df5 = pd.read_csv(DIRCSV + CSV_FILES[5])
df6 = pd.read_csv(DIRCSV + CSV_FILES[6])
df7 = pd.read_csv(DIRCSV + CSV_FILES[7])
df8 = pd.read_csv(DIRCSV + CSV_FILES[8])

df0 = df0.set_index('Country/Region')
df0.loc['Worldwide'] = df0.sum()
df0_x = df0.columns.tolist()
df0_y = df0.loc['Worldwide', ].tolist()
df0_z = df0.index.tolist()
dict0 = []
for x in df0_z:
  dict0.append({'label': x, 'value': x})

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# 背景色と文字色の設定
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
      children='COVID19ダッシュボード',
      style={'textAlign': 'center',
            'color': colors['text']
      }
    ),

    html.Div(
      children='COVID19ワールドワイド及び日本国内感染者数情報', 
      style={'textAlign': 'center',
        'color': colors['text']
      }
    ),

    dcc.Dropdown(
      id='my_ticker_symbol',
      options=dict0,
      value='Worldwide',
    ),

    dcc.Graph(
        id='example-graph',
        figure={
            'data':[
              {'x': df0_x, 'y': df0_y}
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])

@app.callback(
  Output('example-graph', 'figure'),
  [Input('my_ticker_symbol', 'value')])

def update_graph(stock_ticker):
  df0_y = df0.loc[stock_ticker, ].tolist()
  fig = {
    'data':[
      {'x': df0_x, 'y': df0_y}
    ],
    'layout': {
      'title': stock_ticker,
      'plot_bgcolor': colors['background'],
      'paper_bgcolor': colors['background'],
      'font': {'color': colors['text']}
    }
  }
  return fig


if __name__ == '__main__':
    import dldata
    import time

    dldata.down_load()
    time.sleep(10)
    app.run_server(debug=True)
