

import os
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import dldata
import wmap
import jmap
#import matplotlib
from functools import partial
import re


def make_xyz(df, col):
  df.loc[col] = df.sum()
  df_x = df.columns.tolist()
  df_y = df.loc[col, ].tolist()
  df_z = df.index.tolist()
  today_df = df_x[-1]
  today_number_df = df_y[-1]
  dicts = []
  for x in df_z:
    dicts.append({'label': x, 'value': x})
  return(df_x, df_y, dicts, today_df, today_number_df)

DIRCSV = 'static/csv/'
CSV_FILES = (
    'covid19_ww_confirmed_global.csv',
    'covid19_ww_deaths_global.csv',
    'covid19_ww_recovered_global.csv',
    'covid19_jp_prf_cfm.csv',
    'covid19_jp_prf_dth.csv',
    'covid19_jp_prf_rcv.csv',
    'covid19_jp_prf_male.csv',
    'covid19_jp_prf_female.csv',
    'covid19_jp_prf_gen.csv',
    'daily_covid19_ww_confirmed_global.csv',
    'daily_covid19_ww_deaths_global.csv',
    'daily_covid19_ww_recovered_global.csv',
    'daily_covid19_jp_prf_cfm.csv',
    'daily_covid19_jp_prf_dth.csv',
    'daily_covid19_jp_prf_rcv.csv',
    'daily_covid19_jp_prf_male.csv',
    'daily_covid19_jp_prf_female.csv'
)

CATEGORY = ('Worldwide', '全日本')
category_item = (0, 1)
category_change = (3, 16)
ITEMS =(
  '全世界感染者総数： ',
  '全世界死者総数　： ',
  '全世界快復者総数： ', 
  '日本感染者総数　： ',
  '日本死者総数　　： ',
  '日本快復者総数　： ',
)
SUBJECTS = (
  'COVID19ダッシュボード',
  'COVID19ワールドワイド及び日本国内感染者数情報',
)
TITLES =(
  '感染者数',
  '死者数',
  '快復者数',
  '感染者数',
  '死者数',
  '快復者数',
  '男性感染者数',
  '女性感染者数',
  '年代別感染者数(99=年齢不明)'
)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dfs = []
dfx = []
dfy = []
data_xy = []
today = []
today_no = []
text = []
file_no = len(CSV_FILES)
graphs = []
graphs_no = len(TITLES)

for i in range(0, file_no):
  df = pd.read_csv(DIRCSV + CSV_FILES[i], header=0, index_col=0)
  dfs.append(df)
  if i < category_change[0]:
    xx, yy, xy, tdy, tdyno = make_xyz(df, CATEGORY[category_item[0]])
  else:
    xx, yy, xy, tdy, tdyno = make_xyz(df, CATEGORY[category_item[1]])
  dfx.append(xx)
  dfy.append(yy)
  data_xy.append(xy)
  today.append(tdy)
  today_no.append(int(tdyno))


for i in range(0, category_change[0]):
  text.append(str(today[i]) + ITEMS[i] + "{:,.0f}".format(today_no[i]) + '名')
  

##
# dash layout
##
# 背景色と文字色の設定
colors = {
    'background': '#111111',
    'text': '#7FDBFF',
    'text01': '#111111'
}


html_hs =[]
html_hs.append(
  html.H1(
    children=SUBJECTS[0],
    style={'textAlign': 'center',
          'color': colors['text']
    }
  ),
)

html_hs.append(
  html.H6(
    children=SUBJECTS[1], 
    style={'textAlign': 'center',
      'color': colors['text']
    }
  ),
)

j = 0
for i in ITEMS:
  html_hs.append(
    html.Div([
      html.H6(children = i + "{:,.0f}".format(today_no[j]) + "名", style={'color': colors['text'], 'align': 'center'}),
    ], style={'width': '33%', 'display': 'inline-block', 'align': 'center'}),
  )
  j += 1

html_hs.append(
  html.Div([
    html.H6("",
        style={'width': '2%', 'color': colors['text'], 'backgroundcolor': colors['background'], 'display': 'inline-block', 'align': 'center'}
    ),
    dcc.Graph(
        id='world_map',
        figure=wmap.wMap(),
        style={'width': '47%', 'color': colors['text'], 'backgroundcolor': colors['background'], 'display': 'inline-block', 'align': 'center'}
    ),
    html.H6("",
        style={'width': '2%', 'color': colors['text'], 'backgroundcolor': colors['background'], 'display': 'inline-block', 'align': 'center'}
    ),
    dcc.Graph(
      id = 'japan_map',
      figure=jmap.jMap(),
      style={'width': '47%', 'color': colors['text'], 'backgroundcolor': colors['background'], 'display': 'inline-block', 'align': 'center'}
    ),
    html.H6("",
        style={'width': '1%', 'color': colors['text'], 'backgroundcolor': colors['background'], 'display': 'inline-block', 'align': 'center'}
    ),
  ])
)

#html_hs.append(
#  html.Div([
#    dcc.Graph(
#      id = 'japan_map',
#      figure=jmap.jMap(),
#      style={'width': '49%'},
#    ),
#  ]), 
#)

for i in range(0, graphs_no):
  graphs.append(
    html.H6("",
      style={'width': '1%', 'color': colors['text'], 'backgroundcolor': colors['background'], 'display': 'inline-block', 'align': 'center'}
    ),
  )
  if i < category_change[0]:
    graphs.append(
      html.Div([
          dcc.Input(
            id = 'textarea' + str(i),
            value = TITLES[i], 
            style={'textAlign': 'center', 'color': colors['text01'], 'width': '100%'}), 
            dcc.Dropdown(
                id='dropdown' +str(i), 
                options=data_xy[i], 
                value=CATEGORY[0],
            ), 
            dcc.Graph(
                id='graph' + str(i), 
                figure={'data':[{'x': dfx[i], 'y': dfy[i]}], 
                        'layout': {'plot_bgcolor': colors['background'], 
                                  'paper_bgcolor': colors['background'], 
                                  'font': {'color': colors['text']}
                                  }
                        }
                      ),
      ], style={'width': '31%', 'display': 'inline-block'})
    )
  else:
    graphs.append(
      html.Div([
          dcc.Input(
            id = 'textarea' + str(i),
            value = TITLES[i], 
            style={'textAlign': 'center', 'color': colors['text01'], 'width': '100%'}), 
            dcc.Dropdown(
                id='dropdown' +str(i), 
                options=data_xy[i], 
                value=CATEGORY[1],
            ), 
            dcc.Graph(
                id='graph' + str(i), 
                figure={'data':[{'x': dfx[i], 'y': dfy[i]}], 
                        'layout': {'plot_bgcolor': colors['background'], 
                                  'paper_bgcolor': colors['background'], 
                                  'font': {'color': colors['text']}
                                  }
                        }
                      )
      ], style={'width': '31%', 'display': 'inline-block'})
    )
  graphs.append(
    html.H6("",
      style={'width': '1%', 'color': colors['text'], 'backgroundcolor': colors['background'], 'display': 'inline-block', 'align': 'center'}
    ),
  )
layouts = html_hs + graphs

      

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=layouts)


###############################################################################
##
# Callback WW confirmed
##

def update_text(value, i):
  df_list = dfs[i].loc[value, ].tolist()
  value = TITLES[i] + ':  ' + value + " " + str(today[i]) + "/" + "{:,.0f}".format(df_list[-1]) + "名"
  return value
  
def update_graph(value, i):
  dfy[i] = dfs[i].loc[value, ].tolist()
  fig = {
    'data':[
      {'x': dfx[i], 'y': dfy[i]}
    ],
    'layout': {
      'title': value,
      'plot_bgcolor': colors['background'],
      'paper_bgcolor': colors['background'],
      'font': {'color': colors['text']}
    }
  }
  return fig

for i in range(0, graphs_no):
  app.callback(
    Output('textarea{}'.format(i), 'value'),
    [Input('dropdown{}'.format(i), 'value')]
  )(partial(update_text, i = i))

  app.callback(
    Output('graph{}'.format(i), 'figure'),
    [Input('dropdown{}'.format(i), 'value')]
  )(partial(update_graph, i = i))


#if __name__ == '__main__':
  #app.run_server(debug=True)
