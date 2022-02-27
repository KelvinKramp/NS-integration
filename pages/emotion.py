# IMPORT MODULES
import dash
from dash import html
from dash.dependencies import Input, Output, State
from dash import dcc
import dash_bootstrap_components as dbc
from datetime import datetime as dt
from app.app import app


options=[
                                                {'label': 'Very slightly', 'value': '1'},
                                                {'label': 'A little', 'value': '2'},
                                                {'label': 'Moderately', 'value': '3'},
                                                {'label': 'Quite a bit', 'value': '4'},
                                                {'label': 'Extremely', 'value': '5'}
                                            ]


layout = html.Div(children=[
                            # dbc.Row([
                            #     dbc.Col(html.H1("OPS score calculator", style={'textAlign': 'center'}),
                            #             width=12)
                            # ]),
                            dbc.Row([
                                html.H3("",style={ "display": "inline-block", 'textAlign': 'center', "width": "100%",}),
                                ]),
                            dbc.Row(children=[
                                        html.H5("Inspired",
                                                 style={ "display": "inline-block", 'textAlign': 'center', "width": "50%",}),
                                        dcc.RadioItems(
                                            options=options,
                                            id='1',
                                            value='',
                                            # labelStyle={'display': 'inline-block', 'text-align': 'center','width': '100%'},
                                            style={'display': 'inline-block', 'text-align': 'center','display': 'flex', 'justify-content': 'space-evenly', 'width': '40%'},
                                        ),
                            ],),
                            dbc.Row(children=[
                                        html.H5("Upset",
                                                 style={ "display": "inline-block", 'textAlign': 'center', "width": "50%",}),
                                dcc.RadioItems(
                                    options=options,
                                    id='2',
                                    value='',
                                    # labelStyle={'display': 'inline-block', 'text-align': 'center','width': '100%'},
                                    style={'display': 'inline-block', 'text-align': 'center', 'display': 'flex',
                                           'justify-content': 'space-evenly', 'width': '40%'},
                                ),
                            ], ),
                            dbc.Row(children=[
                                html.H5("Excited",
                                        style={"display": "inline-block", 'textAlign': 'center', "width": "50%", }),
                                dcc.RadioItems(
                                    options=options,
                                    id='3',
                                    value='',
                                    # labelStyle={'display': 'inline-block', 'text-align': 'center','width': '100%'},
                                    style={'display': 'inline-block', 'text-align': 'center', 'display': 'flex',
                                           'justify-content': 'space-evenly', 'width': '40%'},
                                ),
                            ], ),
                            dbc.Row(children=[
                                html.H5("Scared",
                                        style={"display": "inline-block", 'textAlign': 'center', "width": "50%", }),
                                dcc.RadioItems(
                                    options=options,
                                    id='4',
                                    value='',
                                    # labelStyle={'display': 'inline-block', 'text-align': 'center','width': '100%'},
                                    style={'display': 'inline-block', 'text-align': 'center', 'display': 'flex',
                                           'justify-content': 'space-evenly', 'width': '40%'},
                                ),
                            ], ),
                            dbc.Row(children=[
                                html.H5("Determined",
                                        style={"display": "inline-block", 'textAlign': 'center', "width": "50%", }),
                                dcc.RadioItems(
                                    options=options,
                                    id='5',
                                    value='',
                                    # labelStyle={'display': 'inline-block', 'text-align': 'center','width': '100%'},
                                    style={'display': 'inline-block', 'text-align': 'center', 'display': 'flex',
                                           'justify-content': 'space-evenly', 'width': '40%'},
                                ),
                            ], ),
                            dbc.Row(children=[
                                html.H5("Afraid",
                                        style={"display": "inline-block", 'textAlign': 'center', "width": "50%", }),
                                dcc.RadioItems(
                                    options=options,
                                    id='6',
                                    value='',
                                    # labelStyle={'display': 'inline-block', 'text-align': 'center','width': '100%'},
                                    style={'display': 'inline-block', 'text-align': 'center', 'display': 'flex',
                                           'justify-content': 'space-evenly', 'width': '40%'},
                                ),
                            ], ),
                            dbc.Row(children=[
                                html.H5("Alert",
                                        style={"display": "inline-block", 'textAlign': 'center', "width": "50%", }),
                                dcc.RadioItems(
                                    options=options,
                                    id='7',
                                    value='',
                                    # labelStyle={'display': 'inline-block', 'text-align': 'center','width': '100%'},
                                    style={'display': 'inline-block', 'text-align': 'center', 'display': 'flex',
                                           'justify-content': 'space-evenly', 'width': '40%'},
                                ),
                            ], ),
                            dbc.Row(children=[
                                html.H5("Nervous",
                                        style={"display": "inline-block", 'textAlign': 'center', "width": "50%", }),
                                dcc.RadioItems(
                                    options=options,
                                    id='8',
                                    value='',
                                    # labelStyle={'display': 'inline-block', 'text-align': 'center','width': '100%'},
                                    style={'display': 'inline-block', 'text-align': 'center', 'display': 'flex',
                                           'justify-content': 'space-evenly', 'width': '40%'},
                                ),
                            ], ),
                            dbc.Row(children=[
                                html.H5("Enthusiastic",
                                        style={"display": "inline-block", 'textAlign': 'center', "width": "50%", }),
                                dcc.RadioItems(
                                    options=options,
                                    id='9',
                                    value='',
                                    # labelStyle={'display': 'inline-block', 'text-align': 'center','width': '100%'},
                                    style={'display': 'inline-block', 'text-align': 'center', 'display': 'flex',
                                           'justify-content': 'space-evenly', 'width': '40%'},
                                ),
                            ], ),
                            dbc.Row(children=[
                                html.H5("Distressed",
                                        style={"display": "inline-block", 'textAlign': 'center', "width": "50%", }),
                                dcc.RadioItems(
                                    options=options,
                                    id='10',
                                    value='',
                                    # labelStyle={'display': 'inline-block', 'text-align': 'center','width': '100%'},
                                    style={'display': 'inline-block', 'text-align': 'center', 'display': 'flex',
                                           'justify-content': 'space-evenly', 'width': '40%'},
                                ),
                            ], ),
                            dbc.Row([
                                dbc.Button('Submit', id='submit', n_clicks=0),
                            ], style={'text-align': 'center', 'margin': 'auto', 'width': '15%'}, className='justify-content-center'),
                            dbc.Row(children=[
                                # html.H3("Totale Score", style={"display": "inline-block", 'textAlign': 'center', "width": "50%", }),
                                html.H3("outcome", id='output-OPS-total',
                                    style={"display": "inline-block", 'textAlign': 'center', "width": "30%", },)
                                ]),
                        ])


### CALLBACKS ## the numbers are LETTER O followed by a number
@app.callback(
    Output('output-OPS-total', 'children'),
    Input("submit", "n_clicks"),
    [State('1', 'value'),
     State('2', 'value'),
     State('3', 'value'),
     State('4', 'value'),
     State('5', 'value'),
     State('6', 'value'),
     State('7', 'value'),
     State('8', 'value'),
     State('9', 'value'),
     State('10', 'value'),
     ])
def calc(click, Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9, Q10):
    l = [Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10]
    l_total, l_o, l_p, l_s   = [], [], [], []
    for i in l:
        if i:
            l_total.append(int(i))
    for i in l[0:3]:
        if i:
            l_o.append(int(i))
    for i in l[3:6]:
        if i:
            l_p.append(int(i))
    for i in l[6:9]:
        if i:
            l_s.append(int(i))
    return "graph"

if __name__ == '__main__':
    app.layout = layout
    server = app.server
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=True)
