from dash import html
from dash import dcc
from dash import dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from app.app import app
from dash.dependencies import Input, Output, State

try:
    df = Parameters.get_parameters_from_DB()
    df = df.drop("id", axis=1)
except Exception as e:
    print(e)
    df = pd.DataFrame()

l=list(df.values)
d = {}
l2 = []
for i in l:
    d = {'label':i[0],'value':i[0]}
    l2.append(d)

submit_update_old, submit_new_old = 0,0

ALLOWED_TYPES = (
    "text", "number", "password", "email", "search",
    "tel", "url", "range", "hidden",
)

layout = html.Div([
    html.Br(),
    html.H4("", id='page-parameters', style={'textAlign': 'center'}),
    html.Br(),
    dbc.Row([
        html.Div(children=[
            dash_table.DataTable(
                id='table-parameters',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
            )
        ],
            style={"width": "50%", 'justify-content': 'center'}
        ), ],
        justify='center'),
    html.Br(),
    html.Hr(),
    html.Br(),
    html.H4("Change parameters", id='change-parameters', style={'textAlign': 'center'}),
    html.Br(),
    dbc.Row([
        dcc.Dropdown(id='my_dropdown-Q2#',
                     options=l2,
                     optionHeight=35,  # height/space between dropdown options
                     value='',  # dropdown value selected automatically when page loads
                     disabled=False,  # disable dropdown value selection
                     multi=False,  # allow multiple dropdown values to be selected
                     searchable=True,  # allow user-searching of dropdown values
                     search_value='',  # remembers the value searched in dropdown
                     placeholder='Please select...',  # gray, default text shown when no option is selected
                     clearable=True,  # allow user to removes the selected value
                     ),
        ], style={'text-align':'center', 'margin':'auto','width':'30%'}, className='justify-content-center'),
    html.Br(),
    dbc.Row([
        dcc.Input(
                          id="input",
                          type="text",
                          placeholder="",
                      ),
        ], style={'text-align':'center', 'margin':'auto','width':'15%'}, className='justify-content-center'),
    html.Br(),
    dbc.Row([
    dbc.Button('Submit', id='submit', n_clicks=0),
    ], style={'text-align': 'center', 'margin': 'auto', 'width': '15%'}, className='justify-content-center'),
    html.Br(),
    html.Hr(),
    html.Br(),
    html.H4("Create new parameters", id='create-new-parameters', style={'textAlign': 'center'}),
    html.Br(),
    dbc.Row([
        dcc.Input(
            id="input-2",
            value="",
            placeholder="Parameter name",
        ),
    ], style={'text-align': 'center', 'margin': 'auto', 'width': '15%'}, className='justify-content-center'),
    html.Br(),
    dbc.Row([
        dcc.Input(
            id="input-3",
            value="",
            placeholder="Parameter value",
        ),
    ], style={'text-align': 'center', 'margin': 'auto', 'width': '15%'}, className='justify-content-center'),
    html.Br(),
    dbc.Row([
        dbc.Button('Submit', id='submit-2', n_clicks=0),
    ], style={'text-align': 'center', 'margin': 'auto', 'width': '15%'}, className='justify-content-center'),
    html.Br(),
    ])



@app.callback(
    Output('table-parameters','data'),
    [Input('submit','n_clicks'),
     Input("submit-2", "n_clicks"),],
    [State('my_dropdown-Q2#','value'),
     State('input','value'),
     State("input-2", "value"),
     State("input-3", "value"),
     ]
)
def submit(submit_update, submit_new, parameter_name_update, content_update, parameter_name_new, content_new):
    global submit_update_old, submit_new_old
    if submit_update > submit_update_old:
        Parameters.update_parameter_in_DB(parameter_name_update, content_update)
    elif submit_new > submit_new_old:
        Parameters.store_parameter_in_DB(parameter_name_new, content_new)
    df = Parameters.get_parameters_from_DB()
    df = df.drop("id", axis=1)
    l = list(df.values)
    l2 = []
    for i in l:
        d = {'label': i[0], 'value': i[0]}
        l2.append(d)
    return df.to_dict('records'), l2


if __name__ == '__main__':
    app.layout = layout
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=True)