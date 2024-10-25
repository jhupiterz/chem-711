import dash
import os
import pandas as pd
from dash import dcc, html, callback, Output, Input
import plots

dash.register_page(__name__, path='/morph-complex')

means_all = [7.943*10**-7, 4.607*10**-7, 9.566*10**-7, 5.000*10**-7, 1.521*10**-6, 1.122*10**-6, 8.180*10**-7, 2.740*10**-6, 2.582*10**-6, 1.931*10**-7, 4.608*10**-7, 9.373*10**-7, 1.802*10**-7, 6.488*10**-7, 4.147*10**-7, 6.352*10**-8]
stds_all = [1.840*10**-7, 1.436*10**-7, 2.888*10**-7, 1.492*10**-7, 4.987*10**-7, 5.103*10**-7, 1.949*10**-7, 8.679*10**-7, 5.451*10**-7, 7.651*10**-8, 1.436*10**-7, 2.505*10**-7, 9.818*10**-8, 1.170*10**-7, 1.216*10**-7, 2.442*10**-8]
samples = ["microbialite", "microbialite", "microbialite", "microbialite", "microbialite", "microbialite", "microbialite", "microbialite", "oolite", "abiotic", "abiotic", "abiotic", "abiotic", "abiotic", "coral", "microbialite"]

means = [4.607*10**-7, 9.566*10**-7, 6.188*10**-7, 7.943*10**-7, 5.000*10**-7, 1.521*10**-6, 1.122*10**-6, 8.180*10**-7, 2.740*10**-6]
stds = [1.436*10**-7, 2.888*10**-7, 2.361*10**-7, 1.840*10**-7,  1.492*10**-7, 4.987*10**-7, 5.103*10**-7, 1.949*10**-7, 8.679*10**-7]
depths = [6, 6, 10, 20, 30, 43, 49, 49, 49]
sample_names = ["CA06a", "CA06b", "CA10", "CA20", "CA30", "CA43", "CA49_1", "CA49_stick", "CA49"]

layout = html.Div([
    # Main content ----------------------------------------------------------
    html.Div([
        html.Div([
            dcc.Graph(id = "left-panel", figure = plots.make_complexity_all_samples_plot(means, depths, stds, sample_names))
        ], style = {"height" : "80vh", "width" : "40vw", "order": "1", "margin-left": "10vw"}),
        html.Div([
            html.Div(
                id = "upper-container-morph",
                style= {"height" : "42vh", "width" : "40vw", "order": "1", "margin-right": "2vw",
                         "margin-bottom": "2vh"}),
            
            html.Div(
                id = "lower-container-morph",
                children=[dcc.Graph(figure=plots.make_mean_vs_std_plot(means, depths, stds))],
                style = {"height": "42vh", "width": "40vw", "order": "2", "z-index": "10"}),
                
            ], style = {"order": "2", "display": "flex", "flex-direction": "column", 
                        "width": "40vw", "height": "85vh", "margin-right": "2vw"})
            
    ], style = {"display": "flex", "flex-direction": "row", "margin": "auto", "margin-left": "10px", "margin-top": "7vh"}),

], style = {"height": "100vh", "align-items":"center"})

@callback(Output('upper-container-morph', 'children'),
          Input('left-panel', 'hoverData'))
def render_sample_scan(hoverData):
    if hoverData:
        sample_name = hoverData['points'][0]['customdata'][1]
        vertices = pd.read_csv(f"data/{sample_name}_vertices.csv")
        faces = pd.read_csv(f"data/{sample_name}_faces.csv")
        epsilon = 0.01
        fig = plots.plot_4d_mesh_morph_page(vertices, faces, epsilon)
        fig.update_layout(title = f"Sample: {sample_name}", title_x = 0.02, title_y = 0.95)
        return dcc.Graph(figure=fig, style= {"height" : "40vh", "width": "42.5vw"}, responsive=True)
    else:
        return html.P('Hover on a data point in left panel', style = {'font-family': 'Arial, sans-serif', 'text-align': 'center', 'margin-top': "15vh"})