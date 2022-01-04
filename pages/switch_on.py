# IMPORT MODULES
from dash import html
import dash_bootstrap_components as dbc
from app.app import app
from dash import Input, Output
from mongodb.connect_mongodb import mongodb_client

layout = dbc.Row([
            html.Br(),
            html.Div(""),
            html.Div(id="layout", children=[
            html.H4("Turn reminder back on? Only confirm after cannula, battery or cartridge replacement, otherwise the reminder will alert again."),
            dbc.Button("Confirm", id='confirm', n_clicks=0)
            ],
            className="d-grid gap-2 col-6 mx-auto",
            style = {"width": "30%", 'justify-content': 'center'}),
            ],
            justify = 'center')

@app.callback(Output('layout', 'children'),
              Input('confirm', 'n_clicks'),)
def update_metrics(n_clicks):
    if n_clicks:
        switch_db = mongodb_client.NS_extension
        collection_name = "switch"
        switch_db = switch_db[collection_name]
        data = {}
        data["switch"] = True
        replacement_data = data
        id = switch_db.find().distinct('_id')
        query = {"_id": id[0]}
        result = switch_db.replace_one(query, replacement_data)
        return html.H4("Reminder turned on")
    else:
        return [
    html.H4("Turn reminder back on? Only confirm after cannula, battery or cartridge replacement, otherwise the reminder will alert again."),
    dbc.Button("Confirm", id='confirm', n_clicks=0)]


if __name__ == '__main__':
    app.layout = layout
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=True)