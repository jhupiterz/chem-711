import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import os
from dash import html, callback, Input, Output

dash.register_page(__name__, path='/compressibility')

layout = html.Div([
    # Main content ----------------------------------------------------------
    html.Div([
        html.Div([
            dcc.Dropdown(
                    id="sample-dropdown-ci",
                    options=["CA06a", "CA43"],
                    value="CA06a",
                    style = {'width': '25vw', "order": "1", "margin-bottom": "0.5vh"}
                )
            ], style = {"display": "flex", "flex-direction": "row", "width": "80vw",
                        "justify-content": "center",  "margin": "auto"}),

        html.Div([
                    html.Img(
                    id = "sem-scans",
                    alt="SEM scan",
                    style = {"order": "1", "height": "55vh", "width": "auto"}
                    ),
                    html.Img(
                    id = "ci-map",
                    style = {"order": "2", "height": "55vh", "width": "auto", "margin-left": "5.5vh"})

        ], style = {"width": "100vw", "height": "80vh", "display": "flex", "flex-direction": "row", "align-items": "center", "justify-content": "center"}),
            
    ]),
], style = {"height": "100vh", "margin-left": "10px", "margin-top": "8vh"})

@callback(Output('sem-scans', 'src'),
          Input('sample-dropdown-ci', 'value'))
def render_tab_content(sample):
    if sample == "CA43":
        return "assets/CA43_1.png"
    else:
        return "assets/CA06_1.png"
    
@callback(Output('ci-map', 'src'),
          Input('sample-dropdown-ci', 'value'))
def render_tab_content(sample):
    if sample == "CA43":
        return "assets/CA43_1_CI.png"
    else:
        return "assets/CA06_1_CI.png"