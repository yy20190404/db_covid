

#!/usr/bin/env python
#-*- coding:utf-8 -*-

import datetime
import gc
import os
import sys

import numpy as np
import pandas as pd

import requests
from requests_html import HTMLSession





def get_converted_multi_columns(df, just_second=False, to_snake_case=True):
  if just_second:
    return [col[1] for col in df.columns.values]
  else:
    if to_snake_case:
        return [col[0] + '_' + col[1] for col in df.columns.values]
    else:
        return [col[0] + col[1].capitalize() for col in df.columns.values]

def down_load():
  HEADERS_DIC = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
  URLWW1 = "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv"
  URLWW2 = "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_deaths_global.csv&filename=time_series_covid19_deaths_global.csv"
  URLWW3 = "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_recovered_global.csv&filename=time_series_covid19_recovered_global.csv"
  URLJP  = "https://dl.dropboxusercontent.com/s/6mztoeb6xf78g5w/COVID-19.csv"
  SAVE_NAMES = ["covid19_ww_confirmed_global.csv", "covid19_ww_deaths_global.csv","covid19_ww_recovered_global.csv", "covid19_jp.csv"]
  DIRCSV = "./static/csv/"
  urls = [URLWW1, URLWW2, URLWW3, URLJP]
  del_cols = ["Province/State", "Lat", "Long"]
  
  ##############################################################################
  ## Reshape of worldwide COVID19 daily numbers csv
  ##############################################################################
  today = datetime.date.today()
  save_names = SAVE_NAMES.copy()
  del save_names[-1]
  i = 0
  for f_name in save_names:
    # Download a target file if it is not exist
    if os.path.isfile(DIRCSV + f_name) == False:
      r = requests.get(urls[i], headers=HEADERS_DIC)
      with open(DIRCSV + f_name, mode='w', encoding='utf_8') as f:
        f.write(r.text)

      ## Reshape csv file
      df = pd.read_csv(DIRCSV + f_name)
      ### Drop unnessesary columns
      df = df.drop(del_cols, axis=1) 
      ### Reshape date style          
      cols = df.columns
      dates = []
      for col in cols:
        if col == 'Country/Region':
          dates.append(col)
        else:
          day = datetime.datetime.strptime(col, '%m/%d/%y')  
          dates.append(day.strftime('%Y-%m-%d'))
      df.columns = dates
      ### Group and sum each country
      df = df.groupby("Country/Region").sum()
      ### Save as csv file
      df.to_csv(DIRCSV + f_name, encoding='utf_8_sig')
      ### Delete dataframe instance
      del df
    else:
      ### Get file datetime
      dt = os.path.getmtime(DIRCSV + f_name)
      dt = datetime.datetime.fromtimestamp(dt)
      dt = dt.strftime('%Y-%m-%d')
      ## Download and reshape csv file when the exist file not made on today
      if str(dt) != str(today):
        r = requests.get(urls[i], headers=HEADERS_DIC)
        with open(DIRCSV + f_name, mode='w', encoding='utf_8') as f:
          f.write(r.text)
        df = pd.read_csv(DIRCSV + f_name)
        df = df.drop(del_cols, axis=1) 
        cols = df.columns
        dates = []
        for col in cols:
          if col == 'Country/Region':
            dates.append(col)
          else:
            day = datetime.datetime.strptime(col, '%m/%d/%y')  
            dates.append(day.strftime('%Y-%m-%d'))
        df.columns = dates
        ### Group and sum each countory
        df = df.groupby("Country/Region").sum()
        df = df.set_index('Country/Region')
        ### Save as csv file
        df.to_csv(DIRCSV + f_name, encoding='utf_8_sig')
        ### Delete dataframe instance
        del df
    i += 1

  ##############################################################################
  ## Reshape of Japanese COVID19 daily numbers csv
  ##############################################################################
  f_name = SAVE_NAMES[3]
  today = datetime.date.today()
  # Download a target file if it is not exist
  if os.path.isfile(DIRCSV + f_name) == False:
    r = requests.get(urls[3], headers=HEADERS_DIC)
    with open(DIRCSV + f_name, mode='w', encoding='utf_8') as f:
      f.write(r.text)
  else:
    dt = os.path.getmtime(DIRCSV + f_name)
    dt = datetime.datetime.fromtimestamp(dt)
    dt = dt.strftime('%Y-%m-%d')
    if today != dt:
      r = requests.get(urls[3], headers=HEADERS_DIC)
      with open(DIRCSV + f_name, mode='w', encoding='utf_8') as f:
        f.write(r.text)
  ## Reshape csv file
  df = pd.read_csv(DIRCSV + f_name)
  
  ################################################################################
  ## Download of Japanese COVID19 data
  ## Reshape the data
  ################################################################################
  cols = df.columns
  df = df.loc[:, ["通し", "受診都道府県", "確定日", "更新日時", "年代", "性別", "ステータス", "人数"]]
  df.columns = ["No.", "Prefecture", "Date", "Saved_Date", "Genelation", "Sex", "Status", "Number"]
  df['Status'] = df['Status'].replace(np.nan, "confirmed")
  df['Status'] = df['Status'].replace('退院', "recovered")
  df['Status'] = df['Status'].replace('死(.*)', "death", regex=True)
  df['Prefecture'] = df['Prefecture'].replace('中部国際空港', '愛知県')
  df['Prefecture'] = df['Prefecture'].replace('成田空港', '千葉県')
  df['Prefecture'] = df['Prefecture'].replace('羽田空港', '東京都')
  df['Prefecture'] = df['Prefecture'].replace('関西国際空港', '大阪府')
  sr = df['Saved_Date']
  modified_date = str(sr[0])
  modified_date = datetime.datetime.strptime(modified_date, '%m/%d/%Y %H:%M')
  modified_date = modified_date.strftime('%Y-%m-%d %H:%M')
  df.at[0, 'Saved_Date'] = modified_date
  df = df.dropna(subset=["Date"])
  dates = []
  for date in df['Date']:
    day = datetime.datetime.strptime(str(date), '%m/%d/%Y')
    dates.append(day.strftime('%Y-%m-%d'))
  df['Date'] = dates
  df.to_csv(DIRCSV + "covid19_jp_all.csv", encoding='utf_8_sig')

  ## 日本の都道府県別・日付別発症者数リスト
  dfc = df.drop(["No.", "Saved_Date", "Genelation", "Sex", "Status"], axis=1)
  dfc = dfc.groupby(["Prefecture", "Date"]).sum().unstack()
  dfc = dfc.replace(np.nan, 0.0)
  dfc.columns = get_converted_multi_columns(dfc, just_second=True)
  dfc.to_csv(DIRCSV + "covid19_jp_prf_cfm.csv", encoding='utf_8_sig')

  ## 日本の都道府県別・日付別死者数リスト
  dfc = df.drop(["No.", "Saved_Date", "Genelation", "Sex", "Number"], axis=1)
  dfc = dfc[dfc["Status"] != "confirmed"]
  dfc = dfc[dfc["Status"] != "recovered"]
  dfc["Status"] = 1
  dfc = dfc.groupby(["Prefecture", "Date"]).sum().unstack()
  dfc = dfc.replace(np.nan, 0.0)
  dfc.columns = get_converted_multi_columns(dfc, just_second=True)
  dfc.to_csv(DIRCSV + "covid19_jp_prf_dth.csv", encoding='utf_8_sig')
  
  ## 日本の都道府県別・日付別退院者数リスト
  dfc = df.drop(["No.", "Saved_Date", "Genelation", "Sex", "Number"], axis=1)
  dfc = dfc[dfc["Status"] != "confirmed"]
  dfc = dfc[dfc["Status"] != "death"]
  dfc["Status"] = 1
  dfc = dfc.groupby(["Prefecture", "Date"]).sum().unstack()
  dfc = dfc.replace(np.nan, 0.0)
  dfc.columns = get_converted_multi_columns(dfc, just_second=True)
  dfc.to_csv(DIRCSV + "covid19_jp_prf_rcv.csv", encoding='utf_8_sig')

  ## 日本の都道府県別・ 男性数リスト
  dfc = df.drop(["No.", "Saved_Date", "Genelation", "Status", "Number"], axis=1)
  dfc = dfc[dfc["Sex"] != "女性"]
  dfc["Sex"] = 1
  dfc = dfc.groupby(["Prefecture", "Date"]).sum().unstack()
  dfc = dfc.replace(np.nan, 0.0)
  dfc.columns = get_converted_multi_columns(dfc, just_second=True)
  dfc.to_csv(DIRCSV + "covid19_jp_prf_male.csv", encoding='utf_8_sig')

  ## 日本の都道府県別・ 女性数リスト
  dfc = df.drop(["No.", "Saved_Date", "Genelation", "Status", "Number"], axis=1)
  dfc = dfc[dfc["Sex"] != "男性"]
  dfc["Sex"] = 1
  dfc = dfc.groupby(["Prefecture", "Date"]).sum().unstack()
  dfc = dfc.replace(np.nan, 0.0)
  dfc.columns = get_converted_multi_columns(dfc, just_second=True)
  dfc.to_csv(DIRCSV + "covid19_jp_prf_female.csv", encoding='utf_8_sig')

  ## 日本の都道府県別・ 年代別リスト
  dfc = df.drop(["No.", "Date", "Saved_Date", "Sex", "Status"], axis=1)
  dfc = dfc.replace(np.nan, 99.0)
  dfc = dfc.replace("0-10", 1.0)
  dfc = dfc.replace("10", 10.0)
  dfc = dfc.replace("20", 20.0)
  dfc = dfc.replace("30", 30.0)
  dfc = dfc.replace("40", 40.0)
  dfc = dfc.replace("50", 50.0)
  dfc = dfc.replace("60", 60.0)
  dfc = dfc.replace("70", 70.0)
  dfc = dfc.replace("80", 80.0)
  dfc = dfc.replace("90", 90.0)
  dfc = dfc.replace(10, 10.0)
  dfc = dfc.replace(20, 20.0)
  dfc = dfc.replace(30, 30.0)
  dfc = dfc.replace(40, 40.0)
  dfc = dfc.replace(50, 50.0)
  dfc = dfc.replace(60, 60.0)
  dfc = dfc.replace(70, 70.0)
  dfc = dfc.replace(80, 80.0)
  dfc = dfc.replace(90, 90.0)
  dfc["Genelation"] = dfc["Genelation"].replace("不明", 99.0)
  dfc["Genelation"] = dfc["Genelation"].astype(int)
  dfc = dfc.groupby(["Prefecture", "Genelation"]).sum().unstack()
  dfc.columns = get_converted_multi_columns(dfc, just_second=True)
  dfc = dfc.replace(np.nan, 0.0)
  dfc = dfc.astype(int)
  dfc.to_csv(DIRCSV + "covid19_jp_prf_gen.csv", encoding='utf_8_sig')

if __name__ == "__main__":
  down_load()
