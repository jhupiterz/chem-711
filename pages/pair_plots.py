import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plots

dash.register_page(__name__, path='/plots')

layout = html.Div([
    # Main content ----------------------------------------------------------
    html.Div([
        html.Div([
            #dcc.Graph(id='plfa-vs-fractal', figure = plots.plot_plfa_vs_fractal()),
            #html.Br(),
            #dcc.Graph(id='plfa-vs-depth', figure = plots.plot_plfa_vs_depth(), style = {"margin-right": "2vw"}),
            #html.Br(),
            #dcc.Graph(id='fractal-vs-depth', figure = plots.plot_fractal_vs_depth(), style = {"margin-right": "2vw"}),
            dcc.Graph(id='subplot', figure = plots.make_paired_subplots_px_mobile(), responsive=True, style = {"width": "97vw", "height": "85vh"})
        ], style = {'margin': 'auto'})
    ]),

], style = {"height": "100vh" ,"margin-bottom": "0px", "margin-left": "10px", "margin-top": "8vh"})
