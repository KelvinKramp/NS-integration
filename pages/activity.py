from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from app.app import app
from dash.dependencies import Input, Output, State

df = pd.DataFrame()

params = [
    'Weight', 'Torque', 'Width', 'Height',
    'Efficiency', 'Power', 'Displacement'
]

layout = html.Div([
    html.Br(),
    html.H3("Activity", id='page-activity', style={'textAlign': 'center'}),
    html.Hr(),
    html.Br(),
    dbc.Row([
    html.Div(children=[
        dash_table.DataTable(
            id='table-editing-activity',
            columns=(
                    [{'id': 'Model', 'name': 'Model', 'selectable':False, 'editable':False}] +
                    [{'id': p, 'name': p} for p in params]
            ),
            data=[
                dict(Model=i, **{param: 0 for param in params})
                for i in range(1, 2)
            ],
            style_table={
                'maxHeight': '40ex',
                'overflowY': 'scroll',
                'width': '100%',
                'minWidth': '100%',
            },
            # style cell
            style_cell={
                'fontFamily': 'Open Sans',
                'textAlign': 'right',
                'height': '50px',
                'padding': '2px 22px',
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
                {
                    # highlight one row
                    'if': {'row_index': 4},
                    "backgroundColor": "#3D9970",
                    'color': 'white'
                }
            ],
            editable=True,
        ),
    ],
        style={"width": "90%", 'justify-content': 'center'}
    ),],
        justify='center'),
    html.Br(),
    dbc.Row([
        html.Div([
        dbc.Alert(
            id="alert-auto-activity",
            is_open=False,
            duration=2000,
            color="success",
            style={'textAlign': 'center',}
    ),
        ],
    style = {"width": "50%", 'justify-content': 'center'}
    ),],
        justify='center'),
    html.Br(),
    dbc.Row([
        dbc.Button('Run analysis', id='run-analysis', n_clicks=0),
    ], style={'text-align': 'center', 'margin': 'auto', 'width': '15%'}, className='justify-content-center'),
    html.Br(),
    html.Div(id="empty-div-activity")
    ])

@app.callback(
    Output('empty-div-activity', 'children'),
    [Input('run-analysis', 'n_clicks')]
)
def set_activity(run_click):
    if run_click:
        return "clicked on analysis"
    else:
        return ""

@app.callback(
    Output("alert-auto-activity", 'children'),
    Output("alert-auto-activity", 'is_open'),
    Input('table-editing-activity', 'data'),
    State('table-editing-activity', 'active_cell'),
)
def process_data_activity(rows, columns):
    print(rows)
    print(columns)
    if columns:
        return [str(columns['column_id']) + " succesfully changed"], True
    else:
        return "", False




if __name__ == '__main__':
    app.layout = layout
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=True)