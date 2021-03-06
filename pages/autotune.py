from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from app.app import app
from dash.dependencies import Input, Output, State
import json
from dash import dcc
from datetime import date
from datetime import datetime as dt
from dateutil import parser
from datetime import timedelta
from urllib.parse import urlparse
import requests
# import pandas as pd
# import json
from API_url import BASE, api_url_part

# VARIABLEs
df = pd.DataFrame()
params = [
    'Weight', 'Torque', 'Width', 'Height',
    'Efficiency', 'Power', 'Displacement'
]


# Functions
# https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False


# TEST 1
# GET PROFILE
def get_profile(NS_HOST):
    response = requests.get(BASE + api_url_part + "get-profile", {"--nightscout":NS_HOST})
    d = response.json()
    full_profile = d
    print(d)
    carb_ratio = d["carb_ratios"]["schedule"][0]["ratio"]
    sensitivity = d["isfProfile"]["sensitivities"][0]["sensitivity"]
    df_basals = pd.DataFrame.from_dict(d["basalprofile"])
    df_basals = df_basals.drop(["i","minutes"],axis=1)
    df_basals["start"] = df_basals["start"].str.slice(stop=-3)
    df_basals = df_basals.rename(columns={"start": "Start", "rate": "Rate"})
    df_non_basals = pd.DataFrame(data={'Sensitvity': [sensitivity], 'Carbratio': [carb_ratio]})
    return df_basals, df_non_basals, full_profile



def create_adjusted_profile(autotune_recomm, old_profile):
    l = autotune_recomm
    d = old_profile
    for i in l:
        if "ISF" in str(i["Parameter"]):
            sensitivity = i["Autotune"]
        if "CarbRatio" in str(i["Parameter"]):
            carb_ratio = i["Autotune"]

    # source https://stackoverflow.com/questions/10663720/how-to-convert-a-time-string-to-seconds

    ftr = [3600,60,1]
    m = []
    for i,j in enumerate(l):
        if any(c.isalpha() for c in j["Parameter"]):
            continue
        timestr = j["Parameter"]
        sec = sum([a * b for a, b in zip(ftr, map(int, timestr.split(':')))])
        for k in range(0,24):
            if (k*3600) == sec:
                l ={'i': k, 'minutes': 60.0*k, 'start': '{:02d}:00:00'.format(k), 'rate': "{:.2f}".format(float(j["Autotune"]))}
                m.append(l)

    d["carb_ratios"]["schedule"][0]["ratio"] = round(float(carb_ratio),1)
    d["carb_ratio"] = round(float(carb_ratio),1)
    d["isfProfile"]["sensitivities"][0]["sensitivity"] = round((float(sensitivity)/18),1)
    d["basalprofile"] = m
    return d


layout = html.Div([
    html.Br(),
    html.H3("Autotune", id='page-autotune', style={'textAlign': 'center'}),
    html.Hr(),
    html.Br(),
    dbc.Row([
    html.Div(children=[
        # STEP 1
        html.Div(id="step-1", hidden=False, children=[
        dbc.Row([
            html.H5("Your nightscout URL:"),
        ], style={'text-align': 'center', 'margin': 'auto', 'width': '50%'}, className='justify-content-center'),
        dbc.Row([
            dcc.Input(
                id="input-url", type="url", placeholder="https://nighscoutname.herokuappp.com",style={'text-align': 'center'},
            ),
        ], style={'text-align': 'center', 'margin': 'auto', 'width': '40%'}, className='justify-content-center'),
        html.Br(),
        dbc.Row([
            dbc.Button('Load profile', id='load-profile', n_clicks=0),
        ], style={'text-align': 'center', 'margin': 'auto', 'width': '30%'}, className='justify-content-center'),
        html.Br(),
        ]),

        # STEP 2
        html.Div(id="step-2", hidden=False, children=[
            dash_table.DataTable(
                id='table-current-non-basals',
                columns=[],
                data=[],
                style_table={
                    'maxHeight': '40ex',
                    'overflowY': 'scroll',
                    'width': '100%',
                    'minWidth': '100%',
                },
                # style cell
                style_cell={
                    'fontFamily': 'Open Sans',
                    'textAlign': 'center',
                    'height': '50px',
                    'padding': '2px 22px',
                    'whiteSpace': 'inherit',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'specifier': '.2f'
                },
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'State'},
                        'textAlign': 'left'
                    },
                ],
                # style header
                style_header={
                    'fontWeight': 'bold',
                    "backgroundColor": "#3D9970",
                    'color': 'white'
                },
                # style filter
                # style data
                style_data_conditional=[
                    {
                        # stripped rows
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    },
                    # {
                    #     # highlight one row
                    #     'if': {'row_index': 4},
                    #     "backgroundColor": "#3D9970",
                    #     'color': 'white'
                    # }
                ],
                editable=False,
            ),
            dash_table.DataTable(
                id='title-table-current-basals',
                columns=[{"name": i, "id": i} for i in ["Start", "Rate"]],
                data=[],
                style_table={
                    'maxHeight': '40ex',
                    'overflowY': 'scroll',
                    'width': '100%',
                    'minWidth': '100%',
                },
                # style cell
                style_cell={
                    'fontFamily': 'Open Sans',
                    'textAlign': 'center',
                    'height': '50px',
                    'padding': '2px 22px',
                    'whiteSpace': 'inherit',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'specifier': '.2f'
                },
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'State'},
                        'textAlign': 'left'
                    },
                ],
                # style header
                style_header={
                    'fontWeight': 'bold',
                    "backgroundColor": "#3D9970",
                    'color': 'white'
                },
                # style filter
                # style data
                style_data_conditional=[
                    {
                        # stripped rows
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    },
                    # {
                    #     # highlight one row
                    #     'if': {'row_index': 4},
                    #     "backgroundColor": "#3D9970",
                    #     'color': 'white'
                    # }
                ],
                editable=False,
            ),
            dash_table.DataTable(
                id='table-current-basals',
                columns=[],
                data=[],
                style_table={
                    'maxHeight': '40ex',
                    'overflowY': 'scroll',
                    'width': '100%',
                    'minWidth': '100%',
                },
                # style cell
                style_cell={
                    'fontFamily': 'Open Sans',
                    'textAlign': 'center',
                    'height': '50px',
                    'padding': '2px 22px',
                    'whiteSpace': 'inherit',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'specifier': '.2f'
                },
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'State'},
                        'textAlign': 'left'
                    },
                ],
                # style header
                style_header={'display': 'none'},
                # style filter
                # style data
                style_data_conditional=[
                    {
                        # stripped rows
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    },
                    # {
                    #     # highlight one row
                    #     'if': {'row_index': 4},
                    #     "backgroundColor": "#3D9970",
                    #     'color': 'white'
                    # }
                ],
                editable=False,
            ),
        html.Br(),
        dbc.Row([
            html.H5("Start and end date for autotune:"),
        ], style={'text-align': 'center', 'margin': 'auto', 'width': '50%'}, className='justify-content-center'),
        dbc.Row([
            html.Div([
                dcc.DatePickerRange(
                    id='date-picker-range',
                    min_date_allowed=date(2000, 8, 5),
                    max_date_allowed=dt.now().date(),
                    initial_visible_month=dt.now().date(),
                    display_format='D-M-Y',
                    start_date=(dt.now() - timedelta(7)).date(),
                    end_date=dt.now().date(),
                    # end_date=dt.now().date()
                ),
            ], style={'text-align': 'center', 'margin': 'auto', 'width': '70%'}, className='justify-content-center'),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Button('Run autotune', id='run-autotune', n_clicks=0),
        ], style={'text-align': 'center', 'margin': 'auto', 'width': '30%'}, className='justify-content-center'),
        ]),


        # STEP 3
        html.Div(id="step-3", hidden=False, children=[
        dbc.Row([
            html.H5("Evaluate:"),
        ], style={'text-align': 'center', 'margin': 'auto', 'width': '50%'}, className='justify-content-center'),
        html.Br(),
            dash_table.DataTable(
                id='title-table-recommendations',
                columns=[{"name": i, "id": i} for i in ["Time", "Pump", "Autotune", "Days Missing"]],
                data=[],
                style_table={
                    'maxHeight': '40ex',
                    'overflowY': 'scroll',
                    'width': '100%',
                    'minWidth': '100%',
                },
                # style cell
                style_cell={
                    'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                    'fontFamily': 'Open Sans',
                    'textAlign': 'center',
                    'height': '50px',
                    'padding': '2px 22px',
                    'whiteSpace': 'inherit',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'specifier': '.2f'
                },
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'State'},
                        'textAlign': 'left'
                    },
                ],
                # style header
                style_header={
                    'fontWeight': 'bold',
                    "backgroundColor": "#3D9970",
                    'color': 'white'
                },
                # style filter
                # style data
                style_data_conditional=[
                    {
                        # stripped rows
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    },
                    # {
                    #     # highlight one row
                    #     'if': {'row_index': 4},
                    #     "backgroundColor": "#3D9970",
                    #     'color': 'white'
                    # }
                ],
                editable=True,
            ),

            dash_table.DataTable(
            id='table-recommendations',
            columns=[],
            data=[],
            style_table={
                'maxHeight': '40ex',
                'overflowY': 'scroll',
                'width': '100%',
                'minWidth': '100%',
            },
            # style cell
            style_cell={
                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'fontFamily': 'Open Sans',
                'textAlign': 'center',
                'height': '50px',
                'padding': '2px 22px',
                'whiteSpace': 'inherit',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'specifier': '.2f'
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': 'State'},
                    'textAlign': 'left'
                },
            ],
            # style header
            style_header={'display': 'none'},
            # style filter
            # style data
            style_data_conditional=[
                {
                    # stripped rows
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                },
                # {
                #     # highlight one row
                #     'if': {'row_index': 4},
                #     "backgroundColor": "#3D9970",
                #     'color': 'white'
                # }
            ],
            editable=True,
        ),
        dbc.Row([
            html.Div([
                dbc.Alert(
                    id="alert-auto-autotune",
                    is_open=False,
                    duration=2000,
                    color="success",
                    style={'textAlign': 'center', }
                ),
            ],
                style={"width": "50%", 'justify-content': 'center'}
            ), ],
            justify='center'),
        html.Br(),
        dbc.Row([
            html.H5("Nightscout API secret:"),
        ], style={'text-align': 'center', 'margin': 'auto', 'width': '50%'}, className='justify-content-center'),
        dbc.Row([
            dcc.Input(
                id="input-API-secret", type="password", placeholder="",style={'text-align': 'center'},
            ),
        ], style={'text-align': 'center', 'margin': 'auto', 'width': '40%'}, className='justify-content-center'),
        html.Br(),
        dbc.Row([
            dbc.Button('Activate on nightscout', id='activate-profile', n_clicks=0),
        ], style={'text-align': 'center', 'margin': 'auto', 'width': '30%'}, className='justify-content-center'),
        ]), #end step3

    ],
        style={"width": "50%", 'justify-content': 'center'}
    ),],
        justify='center'),
    html.Br(),
    html.Div(id="empty-div-autotune")
    ])


    # if click:

    # else:
    #     return [],[],[],[]

#

# @app.callback(
#     Output("alert-auto-autotune", 'children'),
#     Output("alert-auto-autotune", 'is_open'),
#     Input('table-editing-autotune', 'data'),
#     State('table-editing-autotune', 'active_cell'),
# )
# def process_data_autotune(rows, columns):
#     print(rows)
#     print(columns)
#     if columns:
#         return [str(columns['column_id']) + " succesfully changed"], True
#     else:
#         return "", False




if __name__ == '__main__':
    app.layout = layout
    app.run_server(host='0.0.0.0', port=8000, debug=True, use_reloader=True)