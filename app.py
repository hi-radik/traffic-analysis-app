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
#Импор файла с запросами
import queries
#Подключение css
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
    {
        "href":"https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css",
        "rel":"stylesheet"
    }
]

#Создание  Dash приложения
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Аналитика траффика"
app._favicon = ("assets/favicon.ico")

#Layout - то, что мы видим на странице
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(

                #Лого линейной диаграммы
                children = html.Img(src='assets/bar1.png',className='img-top'), className = "animate__animated animate__pulse animate__slow animate__infinite infinite"),
                #Основной заголовок
                html.H1(
                    children="Аналитика трафика", className="header-title"
                ),
                #Параграф под заголовком
                html.P(
                    children="Анализ динамики летной активности в 2022 году",
                    className="header-description",
                ),
            ],
            className="header",
        ),

        #Меню с выпадающими списками
        html.Div(
            children=[
                html.Div(
                    children=[

                        #Подпись для выпадающего списка
                        html.Div(children="Авиабаза", className="menu-title"),
                        dcc.Dropdown(
                            id="afb-filter",
                            options = [
                                #Значения для выпадающего списка авиабаз берем из уникальных значений авиабаз таблицы
                                {"label": afb, "value": afb}
                                for afb in np.sort(queries.diagram_data.afb.unique())
                            ],
                            value='LTAG',
                            clearable=False,
                            className="dropdown",
                ),
            ]
        ),



        html.Div(
            children=[
                html.Div(
                    children="Диапазон",
                    className="menu-title"
                    ),
                #Компонент с выбором диапазона дат
                dcc.DatePickerRange(
                    id="date-range",
                    min_date_allowed=queries.diagram_data.today.min().date(),
                    max_date_allowed=queries.diagram_data.today.max().date(),
                    start_date=queries.diagram_data.today.min().date(),
                    end_date=queries.diagram_data.today.max().date()
                ),
            ]
        ),
    ],
    className="menu",
),
        #Блок с линейной диаграммой
        html.Div(
            children=[
                html.Div(
                    children=

                    #Линейная диаграмма
                    dcc.Graph(
                        id="arrived-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": queries.diagram_data['today'],
                                    "y": queries.diagram_data['text'],
                                    "type": "lines"

                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "График активности",
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True},
                                "yaxis": {"fixedrange": True},
                                "colorway": ["#17B897"]


                            },
                        },
                    ),
                    className="card",
                )


            ],
            className="wrapper",
        ),

        #Блок со второй менюшкой, которая тоже содержит выпадающие списки
        html.Div(
            children = [
                html.Div(
                    children=[
                        html.Div(
                            children="Дата",
                            className="menu-title"
                            ),

                        #Компонент для выбора конкретной даты
                        dcc.DatePickerSingle(
                                id='my-date-picker-single',
                                min_date_allowed=queries.diagram_data.today.min().date(),
                                max_date_allowed=queries.diagram_data.today.max().date(),
                                date=queries.diagram_data.today.max().date()

                            )

                    ]
        ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(children="Авиабаза", className="menu-title"),

                                #Компонент выпадающий список для выбора авиабазы
                                dcc.Dropdown(
                                    id="afb_geo_filter",
                                     options = [
                                #Значения для выпадающего списка авиабаз берем из уникальных значений авиабаз таблицы
                                {"label": afb, "value": afb}
                                for afb in np.sort(queries.diagram_data.afb.unique())
                            ],
                            value='LTAG',
                                    clearable=False,
                                    className="dropdown",
                        ),
            ]
        ),
            ]
        ),
            ],className = 'menu2' ),

        html.Div(
            children=[
                html.Div(

                    #Построение scatter_geo (карты с кругами, где каждый круг - строка в базе данных, описывающая авиабазу)
                    children=dcc.Graph(figure=queries.scatter_fig,id='sctr_geo_chart'), className="card",)],className="wrapper"),

        #Пай чарт и блоки
        html.Div(
            children = [
                html.Div(
                    children = [

                        #Надпись над пай чартом, которая меняется в зависимости от выбора авиабазы из списка
                        html.P(id='afb_text', children='BIKF', className = 'p_afb_text')
                    ],className = 'p_afb'),
                html.Div(

                    #Пай чарт, который показывает отношение военных судов к гражданским для выбранной авиабазы
                    children = dcc.Graph(figure=queries.pie_fig, id='pieFigId1', config = {"displayModeBar": False}), className = 'pie'),

                html.Div(
                    children = [
                        html.P(id='most_busy', children=[

                            html.B('Наиболее загруженная авиабаза на '),' ',html.B(html.P(id='p_date_busy', children = '')),': ', queries.most_busy.iloc[0]['out'], html.Br(),
                            html.B('Активность составляет:'),' ',queries.most_busy.iloc[0]['activity']

                        ], className = 'p_busy')
                    ],className = "busy_block")

            ], className = 'wrapper1'),

        #Футер
        html.Footer(children = [

         html.Div(
            children = [
                html.Div(
                    children = [
                        html.P(
                            children='Anatolij Lysenko', className='footer_p'
                        ),
                        html.P(
                            children='Radomir Spartesnyj', className='footer_p1'
                        ),
                        html.P(
                            children='© 2022', className='footer_p2'
                        )], className = 'pshki' ),

                        html.Div( children = [
                        html.Img(src='assets/dash.png',className = 'dash_img')
                        ],className = 'footer_image_container')

                ], className ='wrapper3'),








        ],className='footer')



#Не трогать
    ]
)

########################################################## Коллбеки ###################################################################

#Изменяем дату в соответсвующем компоненте - меняется дата во фразе "Наиболее загруженная авиабаза на...."
@app.callback(

    Output("most_busy", "children"),
    Input("my-date-picker-single", "date")
)
def update_must_busy_date (date):
    if date is not None:
        mask = (queries.scatter_data.today == date)
        filtered_df = queries.scatter_data.loc[mask,:]
        return [

                            html.B('Наиболее загруженная авиабаза на'),' ', html.B(html.P(id='p_date_busy')),': ',filtered_df[filtered_df['activity'] == filtered_df.activity.max()].iloc[0]['out'], html.Br(),
                            html.B('Активность составляет: '),' ', filtered_df[filtered_df['activity'] == filtered_df.activity.max()].iloc[0]['activity']

                        ]

#Изменяем дату в соответсвующем компоненте - меняется дата во фразе "Наиболее загруженная авиабаза на...."
@app.callback(

    Output("p_date_busy", "children"),
    Input("my-date-picker-single", "date")
)
def update_date_busy (date):
    #mask = (df1.afb == afb)
    #filtered_df = df1.loc[mask,:]
    return date

#Изменяем афб в соответсвующем компоненте - меняется авиабаза над пай чартом
@app.callback(

    Output("afb_text", "children"),
    Input("afb_geo_filter", "value")
)
def update_must_busy (afb):
    #mask = (df1.afb == afb)
    #filtered_df = df1.loc[mask,:]
    return [
                        afb
                    ]

#Изменяем дату в соответсвующем компоненте - меняются значения в выпадающем списке авиабаз для этой даты
@app.callback(

    Output("afb_geo_filter", "options"),
    Input("my-date-picker-single", "date")
)
def update_afb_geo_filter (date):
    if date is not None:
        mask = (queries.pie_data.today == date)
        filtered_df = queries.pie_data.loc[mask,:]

        return [
                                #Значения для выпадающего списка авиабаз берем из уникальных значений авиабаз таблицы
                                {"label": afb, "value": afb}
                                for afb in np.sort(filtered_df.afb.unique())
                            ]


##Изменяем дату в соответсвующем компоненте - меняется скаттер гео чарт
@app.callback(

    Output("sctr_geo_chart", "figure"),
    Input("my-date-picker-single", "date")

)
def update_scatter_chart (date):
    if date is not None:
        mask = (queries.scatter_data.today == date)
        filtered_df = queries.scatter_data.loc[mask,:]

        sctr_geo_chart = px.scatter_geo(filtered_df,
            lon = filtered_df['longitude'],
            lat = filtered_df['latitude'],
            text = filtered_df['activity'],
            color = filtered_df['country'],
            size = filtered_df['activity'],
            hover_name = filtered_df['out'],
            hover_data = {'country':False,
                        'latitude':False,
                        'longitude':False,
                        'out':False}
            )
        return sctr_geo_chart


#Изменяем дату в соответсвующем компоненте - меняется пай чарт
@app.callback(

    Output("pieFigId1", "figure"),
    [
        Input("afb_geo_filter","value"),
        Input("my-date-picker-single", "date")

    ]
)
def update_pie(afb, date):
    if date is not None:
        mask = (
            (queries.pie_data.afb == afb)
            & (queries.pie_data.today == date)
        )

        filtered_data = queries.pie_data.loc[mask,:]
        civils = filtered_data.query("type == 'Civil'")['type'].count()
        military = filtered_data.query("type == 'Military Transport'")['type'].count()
        labels = ['Military Transport Aircarft','Civil Aircraft']
        values = [military, civils]
        pieFig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        return pieFig



#Коллбек для линейной диаграммы
@app.callback(
    Output("arrived-chart", "figure"),
    [
        Input("afb-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date")
    ],
)
def update_charts(afb, start_date, end_date):
    mask = (
        (queries.diagram_data.afb == afb)
        & (queries.diagram_data.today >= start_date)
        & (queries.diagram_data.today <= end_date)

    )
    filtered_data = queries.diagram_data.loc[mask, :]
    arrived_chart_figure = {
        "data": [
            {
                "x": filtered_data["today"],
                "y": filtered_data["text"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {
                "text": "График активности воздушных судов для указанной авиабазы в выбранном диапазоне дат",
                "x": 0.1,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    return arrived_chart_figure

if __name__ == "__main__":
    app.run_server(debug=False)