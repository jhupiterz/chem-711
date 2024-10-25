import dash
import pandas as pd
from dash import dcc, html, callback
import dash_bootstrap_components as dbc
from sklearn.decomposition import PCA
from dash.dependencies import Input, Output
import plots
import numpy as np
from dash import html, callback, Input, Output
import plotly.graph_objects as go
import plotly.express as px
from sklearn.preprocessing import Normalizer, StandardScaler, RobustScaler

dash.register_page(__name__, path='/stats')

# Load data ---------------------------------------------------------------
chem711_df = pd.read_csv("data/chem711.csv", index_col = 0)
chem711_df = chem711_df.iloc[0:18]
chem711_df = chem711_df[["CA06a", "CA06b", "CA06c", "CA10", "CA20", "CA30", "CA43", "CA49"]]
chem711_df = chem711_df.fillna(value=0)
chem711_df = chem711_df.T
chem711_df = chem711_df.drop(columns=["depth"])
target = ["shallow", "shallow", "shallow", "shallow", "shallow", "deep", "deep", "deep"]

plfa_dataset = chem711_df[chem711_df.columns[5:]]
new_columns = [column.split(" ")[2] for column in plfa_dataset.columns]
plfa_dataset.columns = new_columns

dropdown_1 = dcc.Dropdown(
                id = "dropdown-dataset",
                options = ["PLFA peak intensities", "Biomass content and morphologies"],
                value = "PLFA peak intensities",
                style = {"width": "25vw", "z-index": "10", "margin-left": "0.2vw", "margin-bottom": "-3vh", "order": "2"}
            )

dropdown_2 = dcc.Dropdown(
                id = "dropdown-bottom-plot",
                options = ["Scree plot", "Biplot"],
                value = "Scree plot",
                style = {"width": "15vw", "z-index": "10", "margin-left": "3vw", "margin-bottom": "1vh", "order": "2"}
            )

dropdown_3 = dcc.Dropdown(
                id = "dropdown-top-plot",
                options = ["Paired PCs", "2D scores plot"],
                value = "Paired PCs",
                style = {"width": "15vw", "z-index": "10", "margin-left": "3vw", "margin-bottom": "1vh", "order": "2"}
            )

radioitems_1 = html.Div(
    [
        dbc.Label("2. Then, pick a transformation/normalization"),
        dbc.RadioItems(
            id = "transformation",
            options=[
                {"label": "Normalization", "value": 1},
                {"label": "Standardization", "value": 2},
                {"label": "Robust scaling", "value": 3},
            ],
            value=2,
        ),
    ]
)

radioitems_2 = html.Div(
    [
        dbc.Label("3. Last, pick a statistical method"),
        dbc.RadioItems(
            id = "method",
            options=[
                {"label": "PCA", "value": 1},
                {"label": "Dendrogram", "value": 2}
            ],
            value=1,
        ),
    ]
)


layout = html.Div([
    # Main content ----------------------------------------------------------
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                html.P(["1. First, pick a dataset"], style={'font-family': 'Arial, sans-serif', "order": "1"}),
                dropdown_1
            ], style = {"order": "1", "display": "flex", "flex-direction": "column", 
                        "width": "35vw", "height": "20vh", "margin-left": "6vw"}),
            
            html.Div([
                radioitems_1
            ], style = {"order": "2", "display": "flex", "flex-direction": "column", 
                        "width": "35vw", "height": "20vh", "margin-left": "6vw", "margin-top": "-7.5vh"}),

            html.Div([
                radioitems_2
            ], style = {"order": "2", "display": "flex", "flex-direction": "column",
                        "width": "35vw", "height": "20vh", "margin-left": "6vw", "margin-top": "-2.5vh"}),
            ]),
        
            html.Hr(style={"margin-top": "-7vh"}),

            html.Div([
                dcc.Graph(figure= plots.plot_original_distribution(plfa_dataset), style = {"margin-left": "5vw", "order": "1", "margin-top": "1vh"}),
                dcc.Graph(id="transformation-plot", style = {"margin-left": "1vw", "order": "2", "margin-top": "1vh"})
            ], style = {"display": "flex", "flex-direction": "row"}),
        ], style = {"order": "1"}),

        html.Div(style = {"order": "2"}, id="right-panel")
    ], style = {"margin": "2vw", "display": "flex", "flex-direction": "row"})
    
], style = {"width": "100vw", "height":"100vh"})

@callback(Output('transformation-plot', 'figure'),
          Input('transformation', 'value'))
def render_sample_scan(transformation):
    df = plfa_dataset
    if transformation == 1:
        transformer = Normalizer().fit(df)
        data_scaled = transformer.transform(df)
        data_scaled = pd.DataFrame(data_scaled, columns = df.columns)
        title = "After normalization"
    elif transformation == 2:
        transformer = StandardScaler().fit(df)
        data_scaled = transformer.transform(df)
        data_scaled = pd.DataFrame(data_scaled, columns = df.columns)
        title = "After standardization"
    else:
        transformer = RobustScaler().fit(df)
        data_scaled = transformer.transform(df)
        data_scaled = pd.DataFrame(data_scaled, columns = df.columns)
        title = "After Robust scaling"

    fig = go.Figure()
    for plfa in data_scaled.columns:
        fig.add_trace(go.Box(x=data_scaled[plfa], boxpoints='all'))
    fig.update_layout(title = title, title_x = 0.5,
                    showlegend=False, width=200, height=350,
                    yaxis=dict(showline=False, showticklabels=False), margin=dict(l=0, r=0, b=0, t=30))
    return fig

@callback(Output('right-panel', 'children'),
          Input('method', 'value'),
          Input('transformation', 'value'))
def render_right_panel(method, transformation):
    if method == 1:
        return [
            dropdown_3,
            dcc.Graph(id="top-plot", style = {"margin-left": "3.5vw", "margin-bottom": "1vh"}),
            dropdown_2,
            dcc.Graph(id="bottom-plot", style = {"margin-left": "3vw"}),
        ]
    else:
        df = plfa_dataset
        if transformation == 1:
            transformer = Normalizer().fit(df)
            data_scaled = transformer.transform(df)
            data_scaled = pd.DataFrame(data_scaled, columns = df.columns)
        elif transformation == 2:
            transformer = StandardScaler().fit(df)
            data_scaled = transformer.transform(df)
            data_scaled = pd.DataFrame(data_scaled, columns = df.columns)
        else:
            transformer = RobustScaler().fit(df)
            data_scaled = transformer.transform(df)
            data_scaled = pd.DataFrame(data_scaled, columns = df.columns)
        return html.Div([dcc.Graph(figure=plots.plot_kmeans_dendrogram(data_scaled))], style = {"margin-left": "3vw"})

@callback(Output('top-plot', 'figure'),
          Input('transformation', 'value'),
          Input('method', 'value'),
          Input('dropdown-top-plot', 'value'))
def render_plots(transformation, method, plot_choice):
    df = plfa_dataset
    if transformation == 1:
        transformer = Normalizer().fit(df)
        data_scaled = transformer.transform(df)
        data_scaled = pd.DataFrame(data_scaled, columns = df.columns)
    elif transformation == 2:
        transformer = StandardScaler().fit(df)
        data_scaled = transformer.transform(df)
        data_scaled = pd.DataFrame(data_scaled, columns = df.columns)
    else:
        transformer = RobustScaler().fit(df)
        data_scaled = transformer.transform(df)
        data_scaled = pd.DataFrame(data_scaled, columns = df.columns)
    if method == 1:
        plot, pca_results, components = plots.plot_pca_components(data_scaled, target)
        if plot_choice == "Paired PCs":
            return plot
        else:
            return plots.plot_2d_scores(components, target)

@callback(Output('bottom-plot', 'figure'),
          Input('transformation', 'value'),
          Input('method', 'value'),
          Input('dropdown-bottom-plot', 'value'))
def render_scree_plot(transformation, method, plot):
    df = plfa_dataset
    if transformation == 1:
        transformer = Normalizer().fit(df)
        data_scaled = transformer.transform(df)
        data_scaled = pd.DataFrame(data_scaled, columns = df.columns)
    elif transformation == 2:
        transformer = StandardScaler().fit(df)
        data_scaled = transformer.transform(df)
        data_scaled = pd.DataFrame(data_scaled, columns = df.columns)
    else:
        transformer = RobustScaler().fit(df)
        data_scaled = transformer.transform(df)
        data_scaled = pd.DataFrame(data_scaled, columns = df.columns)
    _, pca_results, components = plots.plot_pca_components(data_scaled, target)
    if method == 1:
        pc_variance = pca_results.explained_variance_ratio_
        pc_accum_variance = np.cumsum(pc_variance)
        if plot == "Scree plot":
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=["PC1", "PC2", "PC3", "PC4"], y = pc_variance, text=np.round(pc_variance,2),
                                    mode="lines+markers+text", textposition='top center'))
            fig.update_traces(name='Non-accumulative', showlegend = True)
            fig.add_trace(go.Scatter(x=["PC1", "PC2", "PC3", "PC4"], y = pc_accum_variance, name="Accumulative",
                                    text=np.round(pc_accum_variance,2),
                                    mode="lines+markers+text", textposition='bottom center'))
            fig.update_layout(width = 610, height= 330, margin=dict(l=0, r=0, b=0, t=10),
                            legend=dict(
                                    yanchor="bottom",
                                    y=0.2,
                                    xanchor="right",
                                    x=0.99
                                ))
            fig.update_xaxes(title="")
            fig.update_yaxes(title="Explained variance")
        else:
            fig = plots.plot_biplot(df, pca_results, components)
        return fig