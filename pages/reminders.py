from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from app.app import app
from dash.dependencies import Input, Output, State
from dash import dcc
from update_current_values import update_current_values
from mongodb.save_tresholds_2_db import save_tresholds_2_db
from mongodb.get_tresholds_db import get_tresholds_db
from mongodb.get_current_values_db import get_current_values_db

# bool_site_change, cannula_age = update_current_values("site_change", 36)
site_change, battery_level, insuline_level = get_current_values_db()
current_values = [{'Cannula age':site_change, 'Battery level':battery_level, 'Insuline level':insuline_level}]
th_site_change, th_battery_level, th_insuline_level = get_tresholds_db()
treshold_values = [{'Cannula age':th_site_change, 'Battery level':th_battery_level, 'Insuline level':th_insuline_level}]
df = pd.DataFrame()


list_emails = [{"Name":"PersonA","E-mail":"persona@email"}, {"Name":"PersonB","E-mail":"personb@email"}]
df_emails = pd.DataFrame(list_emails)
params = [
    'Cannula age', 'Battery level', 'Insuline level',
]



layout = html.Div(id='reminders-layout',children=[
    # html.Br(),
    # html.H3("Reminders", id='page-reminders', style={'textAlign': 'center'}),
    # html.Hr(),
    html.Br(),
    dbc.Row([
        html.Div(children=[
            dbc.Card(html.H5(children="Current values",
                             className="text-center text-light bg-primary"), body=True, color="primary"),
                ],
                    style={"width": "50%", 'justify-content': 'center'}
                ),],
                justify = 'center'),
    # html.Br(),
    dbc.Row([
        html.Div(children=[
            dash_table.DataTable(
                id='table-current-values',
                columns=(
                    [{'id': p, 'name': p, "selectable": False} for p in params]
                ),
                data=current_values,
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
                    # 'padding': '2px 22px',
                    'whiteSpace': 'inherit',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
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
                    "backgroundColor": "white",
                    'color': 'black'
                },
                # style filter
                # style data
                style_data_conditional=[
                    {
                        "if": {"state": "active"},
                        'backgroundColor': 'rgba(0, 116, 217, 0.3)',
                        'border': '1px solid rgb(0, 116, 217)'
                    }
                ],
            ),
        ],
            style={"width": "50%", 'justify-content': 'center'}
        ), ],
        justify='center'),
    html.Br(),
    dbc.Row([
        html.Div(children=[
            dbc.Card(html.H5(children="Treshold values",
                             className="text-center text-light bg-primary"), body=True, color="primary"),
        ],
            style={"width": "50%", 'justify-content': 'center'}
        ),
        ],
        justify='center'),
    dbc.Row([
    html.Div(children=[
        dash_table.DataTable(
            id='table-editing-reminders',
            columns=(
                    [{'id': p, 'name': p} for p in params]
            ),
            data=treshold_values,
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
                # 'padding': '2px 22px',
                'whiteSpace': 'inherit',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
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
                "backgroundColor": "white",
                'color': 'black'
            },
            # style filter
            # style data
            style_data_conditional=[
                {
                    # stripped rows
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                },
                {
                    # highlight one row
                    'if': {'row_index': 4},
                    "backgroundColor": "white",
                    'color': 'white'
                }
            ],
            editable=True,
        ),
    ],
        style={"width": "50%", 'justify-content': 'center'}
    ),
    ],
        justify='center'),
    dbc.Row([
        html.Div(children=[html.H6("*click on cells to adjust values")],
                 style={"width": "50%", 'justify-content': 'center'}),
    ],
        justify='center'),
    html.Br(),
    dbc.Row([
        html.Div([
        dbc.Alert(
            id="alert-auto-reminders",
            is_open=False,
            duration=4000,
            color="success",
            style={'textAlign': 'center',}
    ),
        ],
    style = {"width": "50%", 'justify-content': 'center'}
    ),],
        justify='center'),
    dbc.Row([
        html.Div(children=[
            dbc.Card(html.H5(children="Reminder list",
                             className="text-center text-light bg-primary"), body=True, color="primary"),
        ],
            style={"width": "50%", 'justify-content': 'center'}
        ), ],
        justify='center'),
    dbc.Row([
        html.Div(children=[
            dash_table.DataTable(
                id='emails-list',
                columns=[{"name": i, "id": i} for i in df_emails.columns],
                data=df_emails.to_dict('records'),
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
                    # 'padding': '2px 22px',
                    'whiteSpace': 'inherit',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
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
                    "backgroundColor": 'white',
                    'color': 'black'
                },
                # style filter
                # style data
                style_data_conditional=[
                    {
                        # stripped rows
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'white'
                    },
                    {
                        # highlight one row
                        'if': {'row_index': 4},
                        "backgroundColor": "#3D9970",
                        'color': 'white'
                    }
                ],
                editable=True,
                row_deletable=True
            ),
        ],
            style={"width": "50%", 'justify-content': 'center'}
        ), ],
        justify='center'),
    dbc.Row([
        html.Div(children=[html.H6("*click on cells to adjust list")],
                 style={"width": "50%", 'justify-content': 'center'}),
    ],
        justify='center'),
    html.Br(),
    dbc.Row([
        html.Div(children=[
            dbc.Card(html.H5(children="Add people",
                             className="text-center text-light bg-primary"), body=True, color="primary"),
        ],
            style={"width": "50%", 'justify-content': 'center'}
        ), ],
        justify='center'),
    html.Br(),
    dbc.Row([
        dcc.Input(
            id="input-name", type="text", placeholder="Name",
        ),
    ], style={'text-align': 'center', 'margin': 'auto', 'width': '15%'}, className='justify-content-center'),
    html.Br(),
    dbc.Row([
        dcc.Input(
            id="input-email", type="email", placeholder="E-mail address",
        ),
    ], style={'text-align': 'center', 'margin': 'auto', 'width': '15%'}, className='justify-content-center'),
    html.Br(),
    dbc.Row([
        dbc.Button('Add e-mail address', id='e-mail-address', n_clicks=0),
    ], style={'text-align': 'center', 'margin': 'auto', 'width': '15%'}, className='justify-content-center'),
    html.Br(),
    html.Div(id="empty-div-reminders"),
    dcc.Interval(
        id='interval-component',
        interval=60 * 1000,  # in milliseconds
        n_intervals=0
    ),
    ])


@app.callback(
    Output("emails-list", "data"),
    [Input('e-mail-address', 'n_clicks'),],
    State("input-name", "value"),
    State("input-email", "value"),
)
def add_list(click, name, e_mail):
    global list_emails
    print(e_mail)
    if click and name and e_mail:
        d = {"Name":name,"E-mail":e_mail}
        list_emails.append(d)
    df_emails = pd.DataFrame(list_emails)
    return df_emails.to_dict('records')


@app.callback(Output('table-current-values', 'data'),
              Input('interval-component', 'n_intervals'),)
def update_metrics(n):
    # import database variables treshold + current values
    site_change, battery_level, insuline_level = get_current_values_db()
    current_values = [{'Cannula age':site_change, 'Battery level':battery_level, 'Insuline level':insuline_level}]
    return current_values

if __name__ == '__main__':
    app.layout = layout
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=True)