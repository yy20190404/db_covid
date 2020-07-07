
def jMap():
  ##
  # test code
  ##
  import matplotlib.pyplot as plt
  import plotly.graph_objects as go
  import dash_core_components as dcc
  import json
  import sys

  JSON_DIR = "./static/json/"
  prefecture_loop_steps = 47
  #prefecture_loop_steps = 2
  cmap = plt.get_cmap("tab10")
  width = 6.51
  height = 5.71

  class prfplot:
    def __init__(self, width, points):
      rate = width / 6.51
      self.width = width
      self.height = 5.71 * rate
      self.x = []
      self.y = []
      for i in range(0, len(points), 2):
        if i % 2 == 0:
          self.x.append(points[i] * 0.01 * rate)
          self.y.append((points[i + 1] * -0.01 + 5.71) * rate)

    def prfplot(self):
      return(self.x, self.y)

  with open(JSON_DIR + "difinitionOfAllJapan.json", encoding="utf_8_sig") as f:
    definition_of_allJapan = json.load(f) 
  prefectures_id = definition_of_allJapan["prefectures"]

  with open(JSON_DIR + "difinitionOfPrefectures.json", encoding="utf_8_sig") as f:
    definition_of_prefectures = json.load(f) 

  graphs = []
  fig = go.Figure()
  for i in range(0, prefecture_loop_steps):
    prefecture = definition_of_prefectures[i]
    prefecture_id = prefecture["code"]
    prefecture_name = prefecture["name"]
    prefecture_path = prefecture["path"]
    prefecture_map = prefecture_path[0]
    prefecture_draw = prefecture_map["coords"]

    if prefecture_id == 47:
      length = len(prefecture_draw)
      for i in range(0, length):
        pos = prefecture_draw[i]
        if pos > 500:
          npos = pos - 450
        else:
          npos = pos + 200
        prefecture_draw[i] = npos
    
    cascade_steps = len(prefecture_path)
    if cascade_steps == 1:
      pass
    else:
      for j in range(0, cascade_steps):
        pass

    pref = prfplot(width, prefecture_draw)
    x, y = pref.prfplot()

    fig.add_trace(go.Scatter(x=x, y=y,
                    mode='lines',
                    name=prefecture_name,
                    marker_line_color='darkgray'))
    graphs.append(fig)
    
    if prefecture_id == 47:
      separation_draw = [250, 200, 300, 200, 450, 100, 450, 50]
      pref = prfplot(width, separation_draw)
      x, y = pref.prfplot()
      fig.add_trace(go.Scatter(x=x, y=y,
                    mode='lines',
                    name='separation',
                    marker_line_color='darkgray'))
      graphs.append(fig)

  return fig
