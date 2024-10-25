import dash
import os
import pandas as pd
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import data
import plots
from dash import html, callback, Input, Output

dash.register_page(__name__, path='/geochem')

master_plfa_df = data.get_master_plfa_data()
master_alkane_df = data.get_master_alkane_data()


layout = html.Div([
    # Main content ----------------------------------------------------------
    html.Div([
        html.Div([
            dcc.Dropdown(
                    id="sample-dropdown-geochem",
                    options=["CA06a", "CA06b", "CA30", "CA43", "CA49", "CA49_stick", "CA49_1", "cube", "cone"],
                    value="CA06a",
                    style = {'width': '25vw', "order": "1", "margin-left": "1.5vw"}
                ),
            dbc.RadioItems(id = "data-selection-geochem",
                            options=[
                                        {"label": "PLFAs", "value": 1},
                                        {"label": "Alkanes", "value": 2}
                                    ],
                            value = 1, inline = True,
                            style = {"order": "2", "margin-right": "5vw"})
            ], style = {"display": "flex", "flex-direction": "row", "width": "75vw",
                        "justify-content": "space-between",  "margin": "auto", "margin-bottom": "1vh"}),

        html.Div([
            html.Div([
                html.Div(
                    id = "upper-container-geochem",
                    style= {"height" : "40vh", "width" : "75vw", "order": "1"}),
                
                html.Div(
                    id = "lower-container-geochem",
                    style = {"height": "40vh", "width": "75vw",
                             "margin-top": "0vh", "z-index": "10"}),
                    
                ], style = {"margin-top": "5vh", "width": "75vw", "height": "85vh", "margin": "auto"})

        ]),
            
    ]),

], style = {"height": "100vh", "align-items":"center", "margin-bottom": "0px", "margin-left": "10px", "margin-top": "12vh"})

@callback(Output('upper-container-geochem', 'children'),
          Input('data-selection-geochem', 'value'),
          Input('sample-dropdown-geochem', 'value'))
def render_tab_content(data_selection, sample):
    if data_selection == 2:
        return dcc.Graph(figure=plots.plot_chromatogram(master_alkane_df, sample),
                         style= {"height" : "35vh"}, responsive=True)
    else:
        return dcc.Graph(figure=plots.plot_chromatogram(master_plfa_df, sample),
                         style= {"height" : "35vh"}, responsive=True)

@callback(Output('lower-container-geochem', 'children'),
          Input('data-selection-geochem', 'value'),
          Input('sample-dropdown-geochem', 'value'))
def render_tab_content(data_selection, sample):
    if data_selection == 2:
        geochem_df = pd.read_csv("data/geochem_data_ALK.csv")
        geochem_df.columns = ["Alkane ID", "Concentration (ng/g of sample)", "Sample"]
        return dcc.Graph(figure=plots.plot_alk_content(geochem_df, sample), style= {"height" : "35vh"}, responsive=True)
    else:
        geochem_df = pd.read_csv("data/geochem_data.csv")
        geochem_df.columns = ["PLFA ID", "Concentration (ng/g of sample)", "Sample"]
        return dcc.Graph(figure=plots.plot_plfa_content(geochem_df, sample), style= {"height" : "35vh"}, responsive=True)