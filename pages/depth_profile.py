import dash
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plots

dash.register_page(__name__, path='/profile')

layout = html.Div([
    # Main content ----------------------------------------------------------
    html.Div([
        html.Div([
            dcc.Graph(id = 'depth-profile', figure = plots.plot_depth_profile(), style = {'order': '1', "width": "35vw", "height": "85vh"}, responsive=True),
            dcc.Graph(id= 'ph-profile', figure = plots.plot_ph_do2_profile(), style = {'order': '2', "width": "10vw", "height": "84vh"}, responsive=True)    
        ], style = {'order': '1', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'flex-end'}),
        html.Div([
            html.Div([
                #dcc.Graph(id='plfa-vs-fractal', figure = plots.plot_plfa_vs_fractal()),
                #html.Br(),
                #dcc.Graph(id='plfa-vs-depth', figure = plots.plot_plfa_vs_depth(), style = {"margin-right": "2vw"}),
                #html.Br(),
                #dcc.Graph(id='fractal-vs-depth', figure = plots.plot_fractal_vs_depth(), style = {"margin-right": "2vw"}),
                dcc.Dropdown(
                        id="graph-dropdown",
                        options=["PLFA vs. Depth", "Minkowski vs. Depth", "Minkowski vs. PLFA"],
                        value="PLFA vs. Depth",
                        style = {'width': '15vw', "order": "1", "margin-left": "2vw", "margin-bottom": "-6.5vh", "zIndex": 10}
                    ),
                dcc.Graph(id='subplot', responsive=True, style = {"width": "40vw", "height": "40vh"})
            ], style = {'order': '1'}),
            html.Div([
                dcc.Dropdown(
                        id="light-dropdown",
                        options=["PAR vs Depth", "1/LN(PAR) vs. Depth"],
                        value="PAR vs Depth",
                        style = {'width': '15vw', "order": "1", "margin-left": "2vw", "margin-bottom": "-5.5vh", "zIndex": 10}
                    ),
                dcc.Graph(id="light-profile", figure = plots.plot_light_profile(), responsive=True, style = {"width": "40vw", "height": "40vh"})
            ], style = {'order': '2', "margin-top": "7vh"})
    ], style = {"margin-left": "-5vw", 'order':'2', 'display': 'flex',
                'flex-direction': 'column', 'align-items': 'center',
                'justify-content': 'space-between', "margin-top": "2vh"})
    ], style = {'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-around'}),

], style = {"height": "100vh" ,"margin-bottom": "0px", "margin-left": "6vw", "margin-top": "9vh"})

@callback(Output('subplot', 'figure'),
          Input('graph-dropdown', 'value'))
def render_tab_content(graph):
    if graph == "PLFA vs. Depth":
        return plots.plot_plfa_vs_depth()
    elif graph == "Minkowski vs. Depth":
        return plots.plot_fractal_vs_depth()
    else:
        return plots.plot_plfa_vs_fractal()
    
@callback(Output('light-profile', 'figure'),
          Input('light-dropdown', 'value'))
def render_tab_content(graph):
    if graph == "PAR vs Depth":
        return plots.plot_light_profile()
    else:
        return plots.plot_light_profile_linear()


