import dash
import os
import pandas as pd
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import data
import plots
from dash import html, callback, Input, Output
dash.register_page(__name__, path='/')

# Load data ---------------------------------------------------------------
CA06a_vertices = pd.read_csv("data/CA06a_vertices.csv")
CA06a_faces = pd.read_csv("data/CA06a_faces.csv")
CA06b_vertices = pd.read_csv("data/CA06b_new_vertices.csv")
CA06b_faces = pd.read_csv("data/CA06b_new_faces.csv")
CA10_vertices = pd.read_csv("data/CA10_vertices.csv")
CA10_faces = pd.read_csv("data/CA10_faces.csv")
CA20_vertices = pd.read_csv("data/CA20_vertices.csv")
CA20_faces = pd.read_csv("data/CA20_faces.csv")
CA30_vertices = pd.read_csv("data/CA30_vertices.csv")
CA30_faces = pd.read_csv("data/CA30_faces.csv")
CA43_vertices = pd.read_csv("data/CA43_vertices.csv")
CA43_faces = pd.read_csv("data/CA43_faces.csv")
CA49_vertices = pd.read_csv("data/CA49_vertices.csv")
CA49_faces = pd.read_csv("data/CA49_faces.csv")
CA49_stick_vertices = pd.read_csv("data/CA49_stick_vertices.csv")
CA49_stick_faces = pd.read_csv("data/CA49_stick_faces.csv")
CA49_1_vertices = pd.read_csv("data/CA49_1_vertices.csv")
CA49_1_faces = pd.read_csv("data/CA49_1_faces.csv")
cube_vertices = pd.read_csv("data/cube_vertices.csv")
cube_faces = pd.read_csv("data/cube_faces.csv")
cone_vertices = pd.read_csv("data/full_cone_vertices.csv")
cone_faces = pd.read_csv("data/full_cone_faces.csv")
calcite_2_vertices = pd.read_csv("data/calcite_2_vertices.csv")
calcite_2_faces = pd.read_csv("data/calcite_2_faces.csv")
aragonite_2_vertices = pd.read_csv("data/aragonite_2_vertices.csv")
aragonite_2_faces = pd.read_csv("data/aragonite_2_faces.csv")
aragonite_3_vertices = pd.read_csv("data/aragonite_3_vertices.csv")
aragonite_3_faces = pd.read_csv("data/aragonite_3_faces.csv")
coral_vertices = pd.read_csv("data/coral_vertices.csv")
coral_faces = pd.read_csv("data/coral_faces.csv")
limestone_2_vertices = pd.read_csv("data/limestone_2_vertices.csv")
limestone_2_faces = pd.read_csv("data/limestone_2_faces.csv")
weathered_limestone_1_vertices = pd.read_csv("data/weathered_limestone_1_vertices.csv")
weathered_limestone_1_faces = pd.read_csv("data/weathered_limestone_1_faces.csv")
weathered_limestone_4_vertices = pd.read_csv("data/weathered_limestone_4_vertices.csv")
weathered_limestone_4_faces = pd.read_csv("data/weathered_limestone_4_faces.csv")
storrs_1_vertices = pd.read_csv("data/storr_1_vertices.csv")
storrs_1_faces = pd.read_csv("data/storr_1_faces.csv")

master_minkowski_df = data.get_master_dataframe()
master_plfa_df = data.get_master_plfa_data()
master_alkane_df = data.get_master_alkane_data()


layout = html.Div([
    # Main content ----------------------------------------------------------
    html.Div([
        html.Div([
            dcc.Dropdown(
                    id="sample-dropdown",
                    options=["CA06a", "CA06b", "CA10", "CA20", "CA30", "CA43", "CA49", "CA49_stick", "CA49_1",
                             "crystalline aragonite", "oolithic aragonite", "crystalline calcite",
                              "limestone", "weathered limestone (1)", "weathered limestone (4)",
                               "Storr's lake (1)", "coral", "cube", "cone"],
                    value="CA06a",
                    style = {'width': '25vw', "order": "1", "margin-left": "1.5vw"}
                ),
            dbc.RadioItems(id = "data-selection",
                            options=[
                                        {"label": "PLFAs", "value": 1},
                                        {"label": "Alkanes", "value": 2},
                                        {"label": "Fractal dimensions", "value": 3},
                                    ],
                            value = 1, inline = True,
                            style = {"order": "2", "margin-right": "5vw"})
            ], style = {"display": "flex", "flex-direction": "row", "width": "80vw",
                        "justify-content": "space-between",  "margin": "auto"}),

        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(
                            id = "graph-type",
                            options = ["3D scatter", "4D scatter", "4D meshgrid"],
                            value = "4D meshgrid",
                            style = {"width": "15vw", "z-index": "10", "margin-left": "0.2vw", "margin-bottom": "-3vh", "order": "1"}
                        ),

                    html.Div(id = "main-graph",
                            style = {"order": "2", "width": "50vw", "z-index": "1"})
                    ], style = {"display": "flex", "flex-direction": "column", "order": "2",
                                "height": "70vh", "width": "40vw",
                                "margin-bottom": "0px"}),
                    
                ], style = {"display": "flex", "flex-direction": "column", "order": "1",
                            "margin-top": "3vh", "margin-left": "10vw",
                            "width": "40vw", "height": "80vh", "margin-bottom": "0px"}),
            
            html.Div([
                html.Div(
                    id = "upper-container",
                    style= {"height" : "40vh", "width" : "40vw", "order": "1", "margin-bottom": "0vh"}),
                
                html.Div(
                    id = "lower-container",
                    style = {"order": "2", "height": "40vh", "width": "40vw",
                             "margin-top": "0vh", "z-index": "10"}),
                    
                ], style = {"display": "flex", "flex-direction": "column", "order": "2",
                            "margin-top": "2vh", "margin-right": "5vw",
                            "width": "40vw", "height": "80vh", "margin-bottom": "0px"})

        ], style = {"display": "flex", "flex-direction": "row", "justify-content": "space-between"}),
            
    ]),

], style = {"height": "100vh" ,"margin-bottom": "0px", "margin-left": "10px", "margin-top": "8vh"})

@callback(Output('main-graph', 'children'),
          Input('sample-dropdown', 'value'),
          Input('graph-type', 'value'))
def render_tab_content(sample, graph):
    if sample == "CA43":
        vertices = CA43_vertices
        faces = CA43_faces
        epsilon = 0.01
    elif sample == "CA06b":
        vertices = CA06b_vertices
        faces = CA06b_faces
        epsilon = 0.01
    elif sample == "CA30":
        vertices = CA30_vertices
        faces = CA30_faces
        epsilon = 0.01
    elif sample == "CA49":
        vertices = CA49_vertices
        faces = CA49_faces
        epsilon = 0.01
    elif sample == "CA49_1":
        vertices = CA49_1_vertices
        faces = CA49_1_faces
        epsilon = 0.01
    elif sample == "CA49_stick":
        vertices = CA49_stick_vertices
        faces = CA49_stick_faces
        epsilon = 0.01
    elif sample == "cube":
        vertices = cube_vertices
        faces = cube_faces
        epsilon = 5
    elif sample == "cone":
        vertices = cone_vertices
        faces = cone_faces
        epsilon = 20
    elif sample == "crystalline aragonite":
        vertices = aragonite_2_vertices
        faces = aragonite_2_faces
        epsilon = 0.01
    elif sample == "oolithic aragonite":
        vertices = aragonite_3_vertices
        faces = aragonite_3_faces
        epsilon = 0.01
    elif sample == "crystalline calcite":
        vertices = calcite_2_vertices
        faces = calcite_2_faces
        epsilon = 0.01
    elif sample == "coral":
        vertices = coral_vertices
        faces = coral_faces
        epsilon = 0.01
    elif sample == "limestone":
        vertices = limestone_2_vertices
        faces = limestone_2_faces
        epsilon = 0.01
    elif sample == "weathered limestone (1)":
        vertices = weathered_limestone_1_vertices
        faces = weathered_limestone_1_faces
        epsilon = 0.01
    elif sample == "weathered limestone (4)":
        vertices = weathered_limestone_4_vertices
        faces = weathered_limestone_4_faces
        epsilon = 0.01
    elif sample == "Storr's lake (1)":
        vertices = storrs_1_vertices
        faces = storrs_1_faces
        epsilon = 0.01
    elif sample == "CA20":
        vertices = CA20_vertices
        faces = CA20_faces
        epsilon = 0.01
    elif sample == "CA10":
        vertices = CA10_vertices
        faces = CA10_faces
        epsilon = 0.01
    else:
        vertices = CA06a_vertices
        faces = CA06a_faces
        epsilon = 0.01
    if graph == "3D scatter":
        return dcc.Graph(figure= plots.plot_3d_sample(vertices), style= {"height" : "80vh", "width": "35vw"}, responsive=True)
    elif graph == "4D scatter":
        return dcc.Graph(figure= plots.plot_4d_object(vertices, epsilon=epsilon), style= {"height" : "80vh", "width": "35vw"}, responsive=True)
    else:
        return dcc.Graph(figure= plots.plot_4d_mesh(vertices, faces, epsilon=epsilon), style= {"height" : "80vh", "width": "35vw"}, responsive=True)

""" @callback(Output('polycam-view', 'src'),
          Input('sample-dropdown', 'value'))
def render_tab_content(sample):
    if sample == "CA43":
        src = "https://poly.cam/capture/5AE71421-6B38-4350-8152-5E09665618D7"
    elif sample == "CA06b":
        src = "https://poly.cam/capture/ABCFFF49-AF8D-4637-88C7-C8620E786706"
    elif sample == "CA30":
        src = "https://poly.cam/capture/14C96ABF-440B-4609-B6C8-87AFE6372BCC"
    elif sample == "CA49":
        src = "https://poly.cam/capture/E3104C28-36D1-4BB2-8705-8E1A75BA66AB"
    elif sample == "CA49_stick":
        src = "https://poly.cam/capture/174D0F6B-8063-457F-AD01-10635522655D"
    elif sample == "CA49_1":
        src = "https://poly.cam/capture/C3B96C87-38AB-428D-91BA-D38F594D75AF"
    elif sample == "CA06a":
        src = "https://poly.cam/capture/4B716154-9A38-4E5F-8E6F-FA3115282A42"
    elif sample == "crystalline aragonite":
        src = "https://poly.cam/capture/36701A7F-2906-4380-8F04-8F6ABB2D3502"
    elif sample == "oolithic aragonite":
        src = "https://poly.cam/capture/E1A14947-EA50-4E96-8864-9CFF4D0672BB"
    elif sample == "crystalline calcite":
        src = "https://poly.cam/capture/147EEB73-35DE-43E2-9B82-F97D6F1EA6EC"
    elif sample == "coral":
        src = "https://poly.cam/capture/43B90330-28FD-4D59-9CEA-9231CEE1C0D3"
    elif sample == "limestone":
        src = "https://poly.cam/capture/7E979C0F-0026-417F-8A59-51857B0E663A"
    elif sample == "weathered limestone (1)":
        src = "https://poly.cam/capture/11BEF734-05C1-45BE-9688-C87A960F1674"
    elif sample == "weathered limestone (4)":
        src = "https://poly.cam/capture/EAF62289-EF55-4C95-9827-9AB34F8231D7"
    elif sample == "Storr's lake (1)":
        src = "https://poly.cam/capture/9673A75D-0AA1-4E98-B791-B5FE2A7CFF5E"
    elif sample == "CA20":
        src = "https://poly.cam/capture/EFD3C54F-FA25-4E1C-AA60-4686A05E885C"
    elif sample == "CA10":
        src = "https://poly.cam/capture/66A60616-D572-4AB7-83FC-88204726F4DC"
    else:
        src = "data:text/html;charset=utf-8,%3Chtml%3E%3Cdiv style='background-color:rgb(247, 245, 242);height:105vh;width:105vw;padding-top:40vh;'%3E%3Ch3 style='color:grey; font-family:Arial,Helvetica,sans-serif;text-align:center;'%3ENo Polycam preview for this object%3C/h3%3E%3C/div%3E%3C/html%3E"
    return src """

@callback(Output('upper-container', 'children'),
          Input('data-selection', 'value'),
          Input('sample-dropdown', 'value'))
def render_tab_content(data_selection, sample):
    """  dcc.Graph(figure= plots.compute_minkowski(master_minkowski_df[master_minkowski_df["sample"] == sample]),
                         style= {"height" : "20vw"}, responsive=True) """
    if data_selection == 2:
        return dcc.Graph(figure=plots.plot_chromatogram(master_alkane_df, sample),
                         style= {"height" : "20vw"}, responsive=True)
    if data_selection == 3:
        return dcc.Graph(figure= plots.compute_minkowski(master_minkowski_df[master_minkowski_df["sample"] == sample]),
                         style= {"height" : "20vw"}, responsive=True)
    else:
        return dcc.Graph(figure=plots.plot_chromatogram(master_plfa_df, sample),
                         style= {"height" : "20vw"}, responsive=True)

@callback(Output('lower-container', 'children'),
          Input('data-selection', 'value'),
          Input('sample-dropdown', 'value'))
def render_tab_content(data_selection, sample):
    if data_selection == 2:
        geochem_df = pd.read_csv("data/geochem_data_ALK.csv")
        geochem_df.columns = ["Alkane ID", "Concentration (ng/g of sample)", "Sample"]
        return dcc.Graph(figure=plots.plot_alk_content(geochem_df, sample), style= {"height" : "40vh"}, responsive=True)
    if data_selection == 3:
        if sample == "CA43":
            df = CA43_vertices
        elif sample == "CA06b":
            df = CA06b_vertices
        elif sample == "CA30":
            df = CA30_vertices
        elif sample == "CA49":
            df = CA49_vertices
        elif sample == "CA49_stick":
            df = CA49_stick_vertices
        elif sample == "CA49_1":
            df = CA49_1_vertices
        elif sample == "crystalline aragonite":
            df = aragonite_2_vertices
        elif sample == "oolithic aragonite":
            df = aragonite_3_vertices
        elif sample == "oolithic aragonite":
            df = calcite_2_vertices
        elif sample == "coral":
            df = coral_vertices
        elif sample == "limestone":
            df = limestone_2_vertices
        elif sample == "weathered limestone (1)":
            df = weathered_limestone_1_vertices
        elif sample == "weathered limestone (4)":
            df = weathered_limestone_4_vertices
        elif sample == "cube":
            df = cube_vertices
        elif sample == "cone":
            df = cone_vertices
        elif sample == "Storr's lake (1)":
            df = storrs_1_vertices
        elif sample == "CA20":
            df = CA20_vertices
        elif sample == "CA10":
            df = CA10_vertices
        else:
            df = CA06a_vertices
        return dcc.Graph(figure= plots.hist_n_points(df, epsilon=0.01, sample_name=sample), style= {"height" : "40vh"}, responsive=True)
    else:
        geochem_df = pd.read_csv("data/geochem_data.csv")
        geochem_df.columns = ["PLFA ID", "Concentration (ng/g of sample)", "Sample"]
        return dcc.Graph(figure=plots.plot_plfa_content(geochem_df, sample), style= {"height" : "40vh"}, responsive=True)