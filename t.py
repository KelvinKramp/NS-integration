from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
from app.app import app
from dash.dependencies import Input, Output, State



layout = html.Div(children=[
    html.Div(id="step-1",children="testa",hidden=False),
   html.Div(id="step-2", children="testb", hidden=False),
   html.Div(id="step-3", children="testc", hidden=False),
    dbc.Button(id="button")
],
    style={"width": "50%", 'justify-content': 'center'}
)


@app.callback(
    Output('step-1', 'hidden'),
    Output('step-2', 'hidden'),
    Output('step-3', 'hidden'),
    [Input('button', 'n_clicks')],
)
def load_profile(click):
    if click==1:
        return True,False,True
    elif click==2:
        return True, True,False
    else:
        return False, True, True


if __name__ == '__main__':
    app.layout = layout
    app.run_server(host='0.0.0.0', port=8000, debug=True, use_reloader=True)