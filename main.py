
# IMPORT MODULES
from dash import html
from dash import dcc
import dash
from dash.dependencies import Input, Output, State
from app.app import app
import dash_bootstrap_components as dbc
from pages import blank, autotune, reminders, activity, switch_on
from dateutil import parser
from mongodb.save_tresholds_2_db import save_tresholds_2_db
from mongodb.get_tresholds_db import get_tresholds_db

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

def convert_to_datetime(date):
    return parser.parse(date)


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Autotune", href='/autotune')),
        dbc.NavItem(dbc.NavLink("Reminders", href='/reminders')),
        dbc.NavItem(dbc.NavLink("Activity", href="/activity")),
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
    elif "switch_on" in url:
        return switch_on.layout
    else:
        return blank.layout



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

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8081, debug=False)
