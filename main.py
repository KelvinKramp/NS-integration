
# IMPORT MODULES
from dash import html
from dash import dcc
import dash
from dash.dependencies import Input, Output, State
from app.app import app
import dash_bootstrap_components as dbc
from pages import blank, autotune, reminders, activity, emotion, switch_on
from dateutil import parser
from mongodb.save_tresholds_2_db import save_tresholds_2_db
from mongodb.get_tresholds_db import get_tresholds_db
import pandas as pd
import requests
from API_url import BASE, api_url_part



app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

def convert_to_datetime(date):
    return parser.parse(date)


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Autotune", href='/autotune')),
        dbc.NavItem(dbc.NavLink("Reminders", href='/reminders')),
        dbc.NavItem(dbc.NavLink("Activity", href="/activity")),
        dbc.NavItem(dbc.NavLink("Emotion", href="/emotion")),
    ],
    brand="Nigthscout extensions",
    brand_href="/",
    color="primary",
    dark=True,
    sticky='top',
)

app.title = 'Nigthscout extensions'
app.layout = html.Div(children=[
                            navbar,
                            dcc.Location(id='url', refresh=False),
                            html.Div(id="page-content", children=[
                            ]),
                            html.Br(),
                            html.Div(id='empyt-div',children=[]),
                            html.Div(id="hidden_div_for_redirect_callback", children=[]),
        ])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'href')])
def display_page(url):
    # https://github.com/plotly/dash/issues/468
    if "autotune" in url:
        return autotune.layout
    elif "reminders" in url:
        return reminders.layout
    elif "activity" in url:
        return activity.layout
    elif "emotion" in url:
        return emotion.layout
    elif "switch_on" in url:
        return switch_on.layout
    else:
        return blank.layout

# REMINDER CALLBACKS

@app.callback(
    Output("alert-auto-reminders", 'children'),
    Output("alert-auto-reminders", 'is_open'),
    Output('table-editing-reminders', "selected_cells"),
    Output('table-editing-reminders', "active_cell"),
    Output('table-editing-reminders', "data"),
    Input('table-editing-reminders', 'data'),
    State('table-editing-reminders', 'active_cell'),
)
def process_data_reminders(rows, active_cell):
    if not (rows[0]["Cannula age"] or rows[0]["Battery level"] or rows[0]["Insuline level"]):
        return "", False, [], None, None
    print(active_cell)
    site_change, battery_level, insuline_level = rows[0]["Cannula age"],rows[0]["Battery level"],rows[0]["Insuline level"]
    save_tresholds_2_db(site_change,battery_level,insuline_level)
    site_change, battery_level, insuline_level = get_tresholds_db()
    treshold_values = [{'Cannula age': site_change, 'Battery level': battery_level, 'Insuline level': insuline_level}]
    if active_cell:
        return [str(active_cell['column_id']) + " treshold succesfully saved"], True, [], None, treshold_values
    else:
        return "", False, [], None, treshold_values

# AUTOTUNE CALLBACKS

@app.callback(
    Output('table-current-non-basals', 'columns'),
    Output('table-current-non-basals', 'data'),
    Output('table-current-basals', 'columns'),
    Output('table-current-basals', 'data'),
    Output('step-1', 'hidden'),
    Output('step-2', 'hidden'),
    Output('step-3', 'hidden'),
    Output('table-recommendations', 'columns'),
    Output('table-recommendations', 'data'),
    [Input('load-profile', 'n_clicks'),
    Input('run-autotune', 'n_clicks'),],
    State('input-url', 'value'),
    State('date-picker-range', 'start_date'),
    State('date-picker-range', 'end_date'),
)
def load_profile(run_click, run_autotune, NS_HOST, start_date, end_date):
    print(run_autotune)
    print(NS_HOST)
    print(start_date)
    print(end_date)
    if run_autotune:
        if start_date is not None:
            if (end_date is not None) and (NS_HOST is not None):
                b = autotune.uri_validator(NS_HOST)
                if b is not None:
                    response = requests.get(BASE + api_url_part + "run-autotune", {"--nightscout":NS_HOST, "--start-date":start_date, "--end-date":end_date})
                    payload = response.json()
                    df = pd.read_json(payload)
                    print(df)
                    # GET RECOMMENDATIONS
                    # response = requests.get(BASE + api_url_part + "get-recomm", {"--nightscout":NS_HOST, "--start-date":start_date, "--end-date":end_date})
                    # payload = response.json()
                    # df = pd.read_json(payload)
                    # print(df)
                    return [], [], [], [], True, True, False, [{"name": i, "id": i} for i in df.columns], df.to_dict('records'),
                else:
                    df = pd.DataFrame()
            else:
                df = pd.DataFrame()
        else:
            df = pd.DataFrame()
    else:
        df = pd.DataFrame()
    if run_click==1:
        df_basals, df_non_basals, _ = autotune.get_profile(NS_HOST)
        print(_)
        return  [{"name": i, "id": i} for i in df_non_basals.columns], df_non_basals.to_dict('records'), \
                [{"name": i, "id": i} for i in df_basals.columns], df_basals.to_dict('records'),\
                True,False,True,[{"name": i, "id": i} for i in df.columns], df.to_dict('records'),
    elif run_click==2:
        df_basals, df_non_basals, _ = autotune.get_profile(NS_HOST)
        print(_)
        return  [{"name": i, "id": i} for i in df_non_basals.columns], df_non_basals.to_dict('records'), \
                [{"name": i, "id": i} for i in df_basals.columns], df_basals.to_dict('records'),\
                True,True,False,[{"name": i, "id": i} for i in df.columns], df.to_dict('records'),
    else:
        return [],[],[],[], False, True, True,[{"name": i, "id": i} for i in df.columns], df.to_dict('records'),


@app.callback(
    Output('empty-div-autotune','children'),
    [Input('activate-profile', 'n_clicks')],
    State('input-url', 'value'),
    State('input-API-secret', 'value'),
    State('table-recommendations', 'data'),
)
def activate_profile(click, NS_HOST, API_SECRET, json_data):
    if click and NS_HOST and API_SECRET and json_data:
        _, _, profile = autotune.get_profile(NS_HOST)
        new_profile = autotune.create_adjusted_profile(json_data, profile)
        from pprint import pprint
        print("NEW PROFILE")
        pprint(new_profile)
        response = requests.get(BASE + api_url_part + "upload", {"--nightscout":NS_HOST, "--token":API_SECRET, "--json_profile":str(new_profile)})
        print("response")
        print(response)
        print(response.text)
        return "PROFILE SUCCESFULLY UPLOADED"
    else:
        return ""

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8081, debug=False)
