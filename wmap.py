
def wMap():
  import plotly.graph_objects as go
  import pandas as pd
  import numpy as np

  df0 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')
  df1 = pd.read_csv('./static/csv/covid19_ww_confirmed_global.csv')
  df1 = df1.replace('US', 'United States')
  df1 = df1.replace('Congo (Brazzaville)', 'Congo, Democratic Republic of the')
  df1 = df1.replace('Congo (Kinshasa)', 'Congo, Republic of the')
  df1 = df1.replace('Czechia', 'Czech Republic')

  df0 = df0.set_index('COUNTRY')
  df1 = df1.set_index('Country/Region')

  df = df0.join(df1)

  inds = df.index
  cols = df.columns
  col = cols[-1]
  title = 'COVID-19 Confirmed: ' + col
  df = df[['CODE', col]]
  df = df.replace(np.nan, 0)


  fig = go.Figure(data=go.Choropleth(
      locations = df['CODE'],
      z = df[col],
      text = inds,
      colorscale = 'Blues',
      autocolorscale=True,
      reversescale=False,
      marker_line_color='darkgray',
      marker_line_width=0.5,
      colorbar_tickprefix = '',
      colorbar_title = 'COVID-19<br>Confirmed',
  ))

  fig.update_layout(
      title_text=title,
      geo=dict(
          showframe=True,
          showcoastlines=True,
          projection_type='equirectangular'
      ),
  #    annotations = [dict(
  #        x=0.55,
  #        y=0.1,
  #        xref='paper',
  #        yref='paper',
  #        text='Source: <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">  #            CIA World Factbook</a>',
  #        showarrow = False
  #    )]

  )
  return fig
