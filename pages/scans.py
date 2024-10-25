import dash
import os
import pandas as pd
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import data
import plots
from dash import html, callback, Input, Output

dash.register_page(__name__, path='/scans')

# Load data ---------------------------------------------------------------
CA06a_vertices = pd.read_csv("data/CA06a_vertices.csv")
CA06a_faces = pd.read_csv("data/CA06a_faces.csv")
CA06b_vertices = pd.read_csv("data/CA06b_new_vertices.csv")
CA06b_faces = pd.read_csv("data/CA06b_new_faces.csv")
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

layout = html.Div([
    # Main content ----------------------------------------------------------
    html.Div([
        html.Div([
            dcc.Dropdown(
                    id="sample-dropdown-scans",
                    options=["CA06a", "CA06b", "CA30", "CA43", "CA49", "CA49_stick", "CA49_1", "cube", "cone"],
                    value="CA06a",
                    style = {'width': '25vw', "order": "1", "margin-bottom": "0.5vh"}
                )
            ], style = {"display": "flex", "flex-direction": "row", "width": "80vw",
                        "justify-content": "center",  "margin": "auto"}),

        html.Div([
            html.Div([
                html.Div([
                    html.Div(id = "left-scan",
                            style = {"order": "2", "width": "40vw", "z-index": "1"})
                ], style= {"height" : "80vh", "width" : "40vw", "order": "1", "margin-bottom": "2vh"}),
                
                html.Div([
                    html.Div(id = "right-scan",
                            style = {"order": "2", "width": "40vw", "z-index": "1"})
                    ], style = {"display": "flex", "flex-direction": "row", "order": "2",
                                "height": "40vh", "width": "40vw",
                                "margin-bottom": "0px"}),
                    
                ], style = {"display": "flex", "flex-direction": "row", "order": "1",
                            "margin-top": "2vh", "margin": "auto",
                            "width": "80vw", "height": "80vh", "margin-bottom": "0px"})

        ], style = {"display": "flex", "flex-direction": "row", "justify-content": "space-between"}),
            
    ]),
], style = {"margin-left": "10px", "margin-top": "8vh"})

@callback(Output('right-scan', 'children'),
          Input('sample-dropdown-scans', 'value'))
def render_tab_content(sample):
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
    else:
        vertices = CA06a_vertices
        faces = CA06a_faces
        epsilon = 0.01
    #if graph == "3D scatter":
    #    return dcc.Graph(figure= plots.plot_3d_sample(vertices), style= {"height" : "38vh", "width": "80vw"}, responsive=True)
    #elif graph == "4D scatter":
    #    return dcc.Graph(figure= plots.plot_4d_object(vertices, epsilon=epsilon), style= {"height" : "38vh", "width": "80vw"}, responsive=True)
    #else:
    return dcc.Graph(figure= plots.plot_4d_mesh(vertices, faces, epsilon=epsilon), style= {"height" : "80vh", "width": "40vw"}, responsive=True)

@callback(Output('left-scan', 'children'),
          Input('sample-dropdown-scans', 'value'))
def render_tab_content(sample):
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
    else:
        vertices = CA06a_vertices
        faces = CA06a_faces
        epsilon = 0.01
    #if graph == "3D scatter":
    #    return dcc.Graph(figure= plots.plot_3d_sample(vertices), style= {"height" : "38vh", "width": "80vw"}, responsive=True)
    #elif graph == "4D scatter":
    return dcc.Graph(figure= plots.plot_4d_object(vertices, epsilon=epsilon), style= {"height" : "80vh", "width": "40vw"}, responsive=True)

""" @callback(Output('polycam-view-scans', 'src'),
          Input('sample-dropdown-scans', 'value'))
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
    else:
        src = "data:text/html;charset=utf-8,%3Chtml%3E%3Cdiv style='background-color:rgb(247, 245, 242);height:105vh;width:105vw;padding-top:40vh;'%3E%3Ch3 style='color:grey; font-family:Arial,Helvetica,sans-serif;text-align:center;'%3ENo Polycam preview for this object%3C/h3%3E%3C/div%3E%3C/html%3E"
    return src """