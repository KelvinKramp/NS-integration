
# IMPORT MODULES
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from app.app import app,server
import dash_bootstrap_components as dbc
from pages import blank, autotune, reminders, activity
from dateutil import parser


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
    else:
        return blank.layout



if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8081, debug=True)
