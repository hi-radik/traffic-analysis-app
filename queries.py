import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import glob
from numpy.lib.utils import source
import pandas as pd
import numpy as np
import plotly.express as px
import geopandas as gpd
import plotly.graph_objects as go

#Словарь транспортных судов
mtList = {'Lockheed C-5 Galaxy' : 'Military Transport',
          'Lockheed C-5A Galaxy' : 'Military Transport',
          'Lockheed Martin C-5A Galaxy' : 'Military Transport',
          'C-5A':'Military Transport',
          'C-5B':'Military Transport',
          'C-5C':'Military Transport',
          'C-5M':'Military Transport',
          'C-5':'Military Transport',
          'Boeing C-17A Globemaster III':'Military Transport',
          'Boeing C-17 Globemaster III':'Military Transport',
          'C-17': 'Military Transport',
          'C-17A':'Military Transport',
          'Lockheed C-130 Hercules':'Military Transport',
          'Lockheed Martin C-130 Hercules':'Military Transport',
          'C-130':'Military Transport',
          'C-130H':'Military Transport',
          'С-130J':'Military Transport',
          'Beechcraft C-12 Huron':'Military Transport',
          'С-12С':'Military Transport',
          'C-12D':'Military Transport',
          'C-12F':'Military Transport',
          'C-12J':'Military Transport',
          'UC-12F':'Military Transport',
          'UC-12M':'Military Transport',
          'UC-12W':'Military Transport',
          'C-20':'Military Transport',
          'C-21A':'Military Transport',
          'С 21А':'Military Transport',
          'C-26 Metroliner':'Military Transport',
          'C-26B':'Military Transport',
          'RC-26':'Military Transport',
          'Boeing C-32':'Military Transport',
          'C-32A':'Military Transport',
          'C-32B':'Military Transport',
          'C-37A':'Military Transport',
          'C-38A':'Military Transport',
          'C-40':'Military Transport',
          'C-40B':'Military Transport',
          'C-40C':'Military Transport',
          'C-144':'Military Transport',
          'C-146A Wolfhound':'Military Transport',
          'U-28A':'Military Transport'}

#Объединение всех файлов csv из указанной папки
combined = pd.read_csv('data/flights.csv')

#Таблица для первого блока
diagram_data = combined
diagram_data = diagram_data.groupby(['today','afb',]).agg({'text':'size'}).reset_index(level=['today','afb'])
diagram_data["today"] = pd.to_datetime(diagram_data["today"], format="%Y-%m-%d")

#Мердж
afb_details_data = pd.read_csv('data/afbDetails.csv')
afb_details_data = afb_details_data.rename(columns={'code':'afb'})
merged_data = diagram_data.merge(afb_details_data, on='afb')

#Функция определения типа самолета
pie_data = combined
def check_type(data):
    data['type'] = diagram_data['text'].map(mtList)
    data['type'].fillna('Civil', inplace=True)
    return data

#Таблица для пай-чарта
pie_data = check_type(pie_data)

#Подготовка данных для пай-чарта
civils = 0
military = 0
labels = ['Military Transport Aircarft','Civil Aircraft']
values = [military, civils]
#Построение пай чарта
pie_fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

#Таблица для скаттер-гео чарта
scatter_data = merged_data
scatter_data["today"] = pd.to_datetime(scatter_data["today"], format="%Y-%m-%d")
scatter_data['out'] = scatter_data['name'] + ', ' + scatter_data['city'] + ', ' + scatter_data['country'] ######Надо сравнить со списком
scatter_data = scatter_data.rename(columns={'text':'activity'})

#Построение скаттер-гео чарта
scatter_fig = px.scatter_geo(scatter_data,
        lon = scatter_data['longitude'],
        lat = scatter_data['latitude'],
        text = scatter_data['activity'],
        color = scatter_data['country'],
        size = scatter_data['activity'],
        hover_name = scatter_data['out'],
        hover_data = {'country':False,
                     'latitude':False,
                     'longitude':False,
                     'out':False}
        )

#Самая загруженная авиабаза
most_busy = scatter_data[scatter_data['activity'] == scatter_data.activity.max()]
