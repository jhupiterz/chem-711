import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from scipy.spatial.distance import pdist, squareform
from sklearn.decomposition import PCA
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import math

##------- Functions to create the 3D and 4D visualizations -------##
def plot_3d_sample(sample_df):
    """Scatter plots the sample in 3D"""
    fig = px.scatter_3d(sample_df, x='X', y='Y', z='Z')
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), width = 717, height = 390,
                      paper_bgcolor='#f7f5f2', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_traces(marker=dict(size=2))
    fig.update_scenes(xaxis_visible=False, yaxis_visible=False,zaxis_visible=False)
    return fig

def hist_n_points(sample_df, epsilon, sample_name):
    fig = px.histogram(sample_df, x=f"corr_dim_{str(epsilon)}")
    fig.update_xaxes(title="Correlation dimension")
    fig.update_yaxes(title="Count")
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), width = 717, height = 400,
                     paper_bgcolor='#f7f5f2', plot_bgcolor='rgba(0,0,0,0)')
    if (sample_name != "cube") & (sample_name != "cone"):
        fig.add_vline(x=sample_df[f"corr_dim_{str(epsilon)}"].mean(), line_width=2, line_dash= "dash", line_color = "black")
        fig.add_vline(x=sample_df[f"corr_dim_{str(epsilon)}"].mean() + 2*sample_df[f"corr_dim_{str(epsilon)}"].std(), line_width=2, line_dash= "dash", line_color = "grey")
        fig.add_vline(x=sample_df[f"corr_dim_{str(epsilon)}"].mean() - 2*sample_df[f"corr_dim_{str(epsilon)}"].std(), line_width=2, line_dash= "dash", line_color = "grey")
        fig.add_annotation(x=sample_df[f"corr_dim_{str(epsilon)}"].mean()- 2.1*sample_df[f"corr_dim_{str(epsilon)}"].std(), y=400, showarrow=False,
                           text="-2𝜎", font_size=14, textangle=-90)
        fig.add_annotation(x=sample_df[f"corr_dim_{str(epsilon)}"].mean()+ 2.1*sample_df[f"corr_dim_{str(epsilon)}"].std(), y=400, showarrow=False,
                text="+2𝜎", font_size=14, textangle=-90)
        fig.add_annotation(x=0.97*sample_df[f"corr_dim_{str(epsilon)}"].mean(), y=150, showarrow=False,
                text="mean", font_size=14, textangle=-90)
    print("MEAN", sample_df[f"corr_dim_{str(epsilon)}"].mean())
    print("STD DEV", sample_df[f"corr_dim_{str(epsilon)}"].std())
    return fig

def plot_4d_object(sample_df, epsilon):
    """4D scatter plot of the sample with corr_dim as the 4th dimension (color of vertices)"""
    fig = px.scatter_3d(sample_df, x='X', y='Y', z='Z', color = f"corr_dim_{str(epsilon)}")
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), width = 717, height = 390,
                      coloraxis_colorbar_x=1, paper_bgcolor='#f7f5f2', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_traces(marker=dict(size=2))
    fig.update_coloraxes(showscale=False)
    camera = dict(
    eye=dict(x=2, y=2, z=2)
    )
    fig.update_scenes(camera=camera, xaxis_visible=False, yaxis_visible=False,zaxis_visible=False)
    return fig

def plot_4d_mesh(vertices, faces, epsilon):
    """Generates 4D meshgrid of sample with corr_dim as 4th dimension (intensity)"""
    corr_dim = vertices[f"corr_dim_{str(epsilon)}"]

    fig = go.Figure(data=[go.Mesh3d(x=vertices.X, y=vertices.Y, z=vertices.Z, i=faces.I, j=faces.J, k=faces.K, intensitymode= "vertex",
                                    intensity = corr_dim, color='lightpink', opacity=1, colorscale = "plasma"
                                    )
                        ]
                )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), width = 717, height = 390,
                      paper_bgcolor='#f7f5f2', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_traces(colorbar_title_text="Corr. Dim.", colorbar_x = 1)
    camera = dict(
    eye=dict(x=2, y=2, z=2)
    )
    fig.update_scenes(camera = camera, xaxis_visible=False, yaxis_visible=False,zaxis_visible=False)
    return fig

def plot_4d_mesh_morph_page(vertices, faces, epsilon):
    """Generates 4D meshgrid of sample with corr_dim as 4th dimension (intensity)"""
    corr_dim = vertices[f"corr_dim_{str(epsilon)}"]

    fig = go.Figure(data=[go.Mesh3d(x=vertices.X, y=vertices.Y, z=vertices.Z, i=faces.I, j=faces.J, k=faces.K, intensitymode= "vertex",
                                    intensity = corr_dim, color='lightpink', opacity=1, colorscale = "plasma"
                                    )
                        ]
                )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), width = 650, height = 350,
                      paper_bgcolor='#f7f5f2', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_traces(colorbar_title_text="Corr. Dim.", colorbar_x = 1)
    fig.update_scenes(xaxis_visible=False, yaxis_visible=False,zaxis_visible=False)
    return fig

def plot_axes_distribution_of_shape(vertices):
    fig = px.histogram(x=vertices["X"], labels=dict(x="Axis"))
    fig.update_traces(name='Z', showlegend = True)
    fig.update_yaxes(title="Count")
    # Add 3d surface of volcano
    fig.add_trace(
            go.Histogram(x=vertices["Y"], name="Y")
        )
    fig.add_trace(
            go.Histogram(x=vertices["Z"], name="X")
        )
    #fig.update_layout(
        #margin=dict(r=0, t=30, b=25, l=0),
        #title = f"{object_name.capitalize()} - Distribution of vertices along each axis"
    #)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), width = 717, height = 400,
                      paper_bgcolor='#f7f5f2', plot_bgcolor='rgba(0,0,0,0)')
    return fig


##------- Function to plot the Minkowski-Bouligand dimensions -------##
def compute_minkowski(data):
    fig = px.scatter(data_frame= data, x = data["log(dilation_radius)"], y = data["log(influence_volume)"], trendline= "ols", color = "sample")
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), width = 717, height = 400,
                      showlegend = False, paper_bgcolor='#f7f5f2', plot_bgcolor='rgba(0,0,0,0)')
    r_squared = px.get_trendline_results(fig).px_fit_results.iloc[0].rsquared
    fit_result = px.get_trendline_results(fig).px_fit_results.iloc[0]
    intercept = fit_result.params[0]
    slope = fit_result.params[1]
    minkowski_dimension =round(3 - slope, 3)
    fig.add_annotation(x=0.8, y=15.5, showarrow=False,
            text=f"Minkowski-Bouligand dimension = {minkowski_dimension}")
    return fig

##------- Function to plot geochem data -------##
def plot_plfa_content(geochem_data, sample):
    if sample == "CA06b":
        fig = px.bar(geochem_data[geochem_data["Sample"].str.contains(sample)], x="PLFA ID",
                     y="Concentration (ng/g of sample)", color="Sample", barmode="group", text_auto = ".2")
    else:
        fig = px.bar(geochem_data[geochem_data["Sample"] == sample], x="PLFA ID",
                     y="Concentration (ng/g of sample)", color="Sample", text_auto = ".2")
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), width = 717, height = 400, yaxis_title="Concentration [ng/g]",
                      showlegend = False, paper_bgcolor='#f7f5f2', plot_bgcolor='rgba(0,0,0,0)')
    return fig

##------- Function to plot geochem data -------##
def plot_alk_content(geochem_data, sample):
    if sample == "CA06b":
        fig = px.bar(geochem_data[geochem_data["Sample"].str.contains(sample)], x="Alkane ID",
                     y="Concentration (ng/g of sample)", color="Sample", barmode="group", text_auto = ".2")
    else:
        fig = px.bar(geochem_data[geochem_data["Sample"] == sample], x="Alkane ID",
                     y="Concentration (ng/g of sample)", color="Sample", text_auto = ".2")
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), width = 717, height = 400, yaxis_title="Concentration [ng/g]",
                      showlegend = False, paper_bgcolor='#f7f5f2', plot_bgcolor='rgba(0,0,0,0)')
    return fig

##------- Function to plot chromatogram -------##
def plot_chromatogram(df, sample):
    fig = px.line(df[df["Sample"].str.contains(sample)], x= "Retention time", y= "Count", color = "Sample")
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), width = 717, height = 400, xaxis_title="Retention time [min]",
                      legend=dict(x=0.85, y=0.9), hovermode = "x unified",
                      showlegend = False, paper_bgcolor='#f7f5f2', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_traces(opacity=.6)
    fig.update_xaxes(range = [10,25])
    return fig

##------- Function to plot the depth profile -------##
def plot_depth_profile():
    x = [0,0,0,0,0,0,0]
    y = [-6, -7, -30, -43, -48.5, -49, -49.5]
    x_tba = [0,0,0,0,0,0]
    tba = [-10, -15, -20, -30, -70, -71]
    sample_names = ["CA06a", "CA06b", "CA30", "CA43", "CA49", "CA49_1", "CA49_stick"]

    sample_df = pd.DataFrame(x, columns = ["X"])
    sample_df["Depth"] = y
    sample_df["Sample"] = sample_names

    fig = px.scatter(data_frame= sample_df, x = "X", y = "Depth", color = "Sample", custom_data= ["Sample"], )

    fig.update_layout(width=500, height = 700, margin=dict(l=0, r=0, b=0, t=0), showlegend=False)
    fig.update_traces(hovertemplate='Sample: %{customdata}<br>Depth: %{y}')

    fig.update_xaxes(visible= False, showticklabels=False, range=[-0.5, 2.5], showgrid = False)
    fig.update_yaxes(title="Depth [m]", range=[-71,0], showgrid = False)

    fig.update_traces(
        marker=dict(size=14, symbol="x"),
        selector=dict(mode="markers"))

    fig.add_traces(go.Scatter(x=x_tba, y=tba, mode="markers", marker_color = "grey", marker_size= 10, marker_symbol = "x"))
    
    fig.add_vrect(x0="-0.5", x1="0",
              fillcolor="brown", opacity=0.25, line_width=0)
    
    fig.add_annotation(x=-0.25, y=-35, showarrow=False,
                text="cenote wall", textangle=-90, font_size=14)

    #fig.add_vline(x=0, line_width=5, line_color = "white", opacity = 0.25)
    fig.add_hline(y=-11, line_width=2, line_dash= "dash")
    fig.add_hline(y=-13, line_width=2, line_dash= "dash")

    fig.add_hline(y=-58, line_width=2, line_dash= "dash")
    fig.add_hline(y=-62, line_width=2, line_dash= "dash")

    #fig.add_trace(go.Scatter(x = sample_df["X"], y = sample_df["Depth"], mode='markers', marker = dict(size= 12, symbol='x')))
    
    fig.add_annotation(x=0.5, y=-12, showarrow=False,
                text="thermocline", font_size=14)
    fig.add_annotation(x=0.5, y=-60, showarrow=False,
                text="<sup>H<sub>2</sub>S</sup>", font_size=20)
    fig.add_annotation(x=1.5, y=-6, showarrow=False,
                text="∂<sup>13</sup>C = -5.143 ±0.2‰<br>Age = 7714 B.P. ±33", bgcolor = "white", font_size=14)
    fig.add_annotation(x=1.5, y=-50, showarrow=False,
                text="∂<sup>13</sup>C = -6.313 ±0.2‰<br>Age = 8065 B.P. ±33", bgcolor = "white", font_size=14)
    fig.add_annotation(x=1.5, y=-60, showarrow=False,
                text="∂<sup>13</sup>C = -6.002 ±0.2‰<br>Age = 8024 B.P. ±39", bgcolor = "white", font_size=14)
    fig.add_annotation(x=1.5, y=-69, showarrow=False,
                text="∂<sup>13</sup>C = -6.632 ±0.2‰<br>Age = 9193 B.P. ±40", bgcolor = "white", font_size=14)
    return fig

def plot_ph_do2_profile():
    y = np.array([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 61, 62, 64, 66, 68, 70])
    y = y*-1
    x_o2 =  [10, 9.8, 9.7, 9.5, 9.4, 9.3, 9.2, 9.1, 9, 8.8, 8.7, 8.5, 8.4, 8.2, 8, 7.7, 7.5, 7.3, 7.2, 7.1, 7, 6.9, 6.8, 6.7, 6.6, 6.5, 6.45, 6.4, 6.38, 6.3, 4, 3, 2.5 ,2.1,2,2,1.9]
    x_ph = [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6.5, 6.3, 6, 6, 6, 6, 6]

    fig = px.line(x =x_o2, y=y, markers=True)
    fig.update_traces(showlegend=True, name='dO2')
    fig.add_trace(go.Scatter(x=x_ph, y=y, name="pH", mode="markers+lines"))
    fig.update_layout(width=200, height=691, margin=dict(l=0, r=0, b=0, t=0))
    fig.update_xaxes(visible=False)
    fig.add_hline(y=-11, line_width=2, line_dash= "dash")
    fig.add_hline(y=-13, line_width=2, line_dash= "dash")

    fig.add_hline(y=-58, line_width=2, line_dash= "dash")
    fig.add_hline(y=-62, line_width=2, line_dash= "dash")
    fig.update_yaxes(visible=False, range=(-71,0))
    return fig

def plot_plfa_vs_fractal():
    sample_names = ["CA06a", "CA06b", "CA43", "CA49"]
    fractal_dims = [1.94, 1.95, 1.91, 2.00]
    plfa_content = [1.974, 2.072, 0.457, 0.268]

    plfa_vs_fractals = pd.DataFrame(sample_names, columns = ["sample"])
    plfa_vs_fractals["fractal_dim"] = fractal_dims
    plfa_vs_fractals["plfa_content"] = plfa_content
    fig = px.scatter(data_frame=plfa_vs_fractals, x="fractal_dim", y="plfa_content", color="sample")
    fig.update_xaxes(title="Minkowski-Bouligand dimension", range=[1.8, 2.2])
    fig.update_yaxes(title="PLFA content [ng/g of sample]", range=[0, 3])
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=10), width= 600, height=260, showlegend = False)
    fig.update_traces(
        marker=dict(size=14, symbol="x"),
        selector=dict(mode="markers"))
    return fig

def plot_plfa_vs_depth():
    sample_names = ["CA06a", "CA06b", "CA43", "CA49"]
    depth = [-6, -6, -43, -49]
    plfa_content = [1.974, 2.072, 0.457, 0.268]

    plfa_vs_fractals = pd.DataFrame(sample_names, columns = ["sample"])
    plfa_vs_fractals["depth"] = depth
    plfa_vs_fractals["plfa_content"] = plfa_content
    fig = px.scatter(data_frame=plfa_vs_fractals, x="plfa_content", y="depth", color="sample")
    fig.update_yaxes(title="Depth [m]", range=[0, -70])
    fig.update_xaxes(title="PLFA content [ng/g of sample]", range=[0, 3])
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), width= 605, height=200, showlegend=False)
    fig.update_traces(
        marker=dict(size=14, symbol="x"),
        selector=dict(mode="markers"))
    return fig

def plot_fractal_vs_depth():
    sample_names = ["CA06a", "CA06b", "CA43", "CA49", "CA30", "CA49_1", "CA49_stick"]
    depth = [-6, -6, -43, -48.5, -30, -49, -49.5]
    fractal_dims = [1.94, 1.95, 1.91, 2.00, 2.03, 1.95, 2.05]

    plfa_vs_fractals = pd.DataFrame(sample_names, columns = ["sample"])
    plfa_vs_fractals["depth"] = depth
    plfa_vs_fractals["fractal_dim"] = fractal_dims
    fig = px.scatter(data_frame=plfa_vs_fractals, x="fractal_dim", y="depth", color="sample")
    fig.update_yaxes(title="Depth [m]", range=[0, -70])
    fig.update_xaxes(title="Minkowski-Bouligand dimension", range=[1.8, 2.2])
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), width= 605, height=200, legend=dict(yanchor="top",
                                  title = "KEY",
                                  bgcolor="#f7f5f2",
                                  orientation= "h",
                                  y=1.2,
                                  xanchor="left",
                                  x=0.01))
    fig.update_traces(
        marker=dict(size=14, symbol="x"),
        selector=dict(mode="markers"))
    return fig

def plot_light_profile():
    depth = [-2.5, -5, -10, -15, -20, -30, -40, -50]
    par = [1050, 800, 600, 450, 375, 225, 150, 90]
    df = pd.DataFrame(par, columns = ["PAR"])
    df["depth"] = depth
    fig = px.scatter(df, x="PAR", y="depth")
    fig.update_traces(mode="lines+markers")
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), width= 605, height=200)
    fig.update_xaxes(title="PAR [µmol/m2/s]")
    fig.update_yaxes(title="Depth [m]")
    return fig

def plot_light_profile_linear():
    depth = [-2.5, -5, -10, -15, -20, -30, -40, -50]
    par = [1050, 800, 600, 450, 375, 225, 150, 90]
    df = pd.DataFrame(par, columns = ["PAR"])
    df["depth"] = depth
    df["PAR_trans"] = [1/np.log(x) for x in par]
    fig = px.scatter(df, x="PAR_trans", y="depth", trendline = "ols")
    #fig.update_traces(mode="lines+markers")
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), width= 605, height=200)
    fig.update_xaxes(title="PAR [µmol/m2/s]")
    fig.update_yaxes(title="Depth [m]")
    return fig

def make_paired_subplots_px():
    # Create figures in Express
    figure1 = plot_plfa_vs_fractal()
    figure2 = plot_plfa_vs_depth()
    figure3 = plot_fractal_vs_depth()


    # For as many traces that exist per Express figure, get the traces from each plot and store them in an array.
    # This is essentially breaking down the Express fig into it's traces
    figure1_traces = []
    figure2_traces = []
    figure3_traces = []
    for trace in range(len(figure1["data"])):
        figure1["data"][trace]['showlegend'] = False
        figure1_traces.append(figure1["data"][trace])
    for trace in range(len(figure2["data"])):
        figure2["data"][trace]['showlegend'] = False
        figure2_traces.append(figure2["data"][trace])
    for trace in range(len(figure3["data"])):
        figure3_traces.append(figure3["data"][trace])

    #Create a 1x2 subplot
    this_figure = make_subplots(rows=3, cols=1) 

    # Get the Express fig broken down as traces and add the traces to the proper plot within in the subplot
    for traces in figure1_traces:
        this_figure.append_trace(traces, row=1, col=1)
    for traces in figure2_traces:
        this_figure.append_trace(traces, row=2, col=1)
    for traces in figure3_traces:
        this_figure.append_trace(traces, row=3, col=1)
    
    this_figure['layout']['xaxis']['title']='Minkowski-Bouligand dimension'
    this_figure['layout']['xaxis2']['title']='PLFA content [ng/g of sample]'
    this_figure['layout']['xaxis3']['title']='Minkowski-Bouligand dimension'
    this_figure['layout']['yaxis']['title']='PLFA content'
    this_figure['layout']['yaxis2']['title']='Depth [m]'
    this_figure['layout']['yaxis3']['title']='Depth [m]'

    this_figure.update_layout(width=700, height=720, showlegend = True, margin=dict(l=0, r=0, b=0, t=0))

    return this_figure

def make_paired_subplots_px_mobile():
    # Create figures in Express
    figure1 = plot_plfa_vs_fractal()
    figure2 = plot_plfa_vs_depth()
    figure3 = plot_fractal_vs_depth()


    # For as many traces that exist per Express figure, get the traces from each plot and store them in an array.
    # This is essentially breaking down the Express fig into it's traces
    figure1_traces = []
    figure2_traces = []
    figure3_traces = []
    for trace in range(len(figure1["data"])):
        figure1["data"][trace]['showlegend'] = False
        figure1_traces.append(figure1["data"][trace])
    for trace in range(len(figure2["data"])):
        figure2["data"][trace]['showlegend'] = False
        figure2_traces.append(figure2["data"][trace])
    for trace in range(len(figure3["data"])):
        figure3["data"][trace]['showlegend'] = False
        figure3_traces.append(figure3["data"][trace])

    #Create a 1x2 subplot
    this_figure = make_subplots(rows=3, cols=1) 

    # Get the Express fig broken down as traces and add the traces to the proper plot within in the subplot
    for traces in figure1_traces:
        this_figure.append_trace(traces, row=1, col=1)
    for traces in figure2_traces:
        this_figure.append_trace(traces, row=2, col=1)
    for traces in figure3_traces:
        this_figure.append_trace(traces, row=3, col=1)
    
    this_figure['layout']['xaxis']['title']='Minkowski-Bouligand dimension'
    this_figure['layout']['xaxis2']['title']='PLFA content [ng/g of sample]'
    this_figure['layout']['xaxis3']['title']='Minkowski-Bouligand dimension'
    this_figure['layout']['yaxis']['title']='PLFA content'
    this_figure['layout']['yaxis2']['title']='Depth [m]'
    this_figure['layout']['yaxis3']['title']='Depth [m]'

    this_figure.update_layout(width=700, height=720, showlegend = True, margin=dict(l=0, r=0, b=0, t=0))

    return this_figure

##------- Function to plot the complexity vs depth -------##

def make_complexity_vs_depth_plot(means_all, stds_all, samples):
    fig = px.scatter(x=means_all, y=stds_all, color = samples,
                     labels={'x': 'Mean correlation dimension', 'y':'Standard deviation'},
                     title="Morphological complexity of all samples")
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=40), width = 600, height = 300, title_x = 0.5,
                      showlegend = True, paper_bgcolor='#f7f5f2', plot_bgcolor='rgba(0,0,0,0)')
    return fig

def make_complexity_all_samples_plot(means, depths, stds, sample_names):
    fig = px.scatter(x=means, y=depths, error_x = stds,
                     labels={'x': 'Mean correlation dimension', 'y':'Depth [m]'},
                     hover_data={'Stdev': stds, 'Sample name': sample_names})                            
    fig.update_traces(error_x_color="black", error_x_thickness = 1.5, marker=dict(size=12))
    fig.update_layout(margin=dict(l=80, r=0, b=70, t=15), width = 450, height = 650, title_x = 0.5,
                      showlegend = False, paper_bgcolor='#f7f5f2', plot_bgcolor='rgba(0,0,0,0)',
                      font=dict(size=14))
    fig.update_yaxes(autorange="reversed")
    return fig

def make_mean_vs_std_plot(means, depths, stds):
    means = [4.607*10**-7, 9.566*10**-7, 6.188*10**-7, 7.943*10**-7, 5.000*10**-7, 1.521*10**-6, 1.122*10**-6, 2.740*10**-6]
    stds = [1.436*10**-7, 2.888*10**-7, 2.361*10**-7, 1.840*10**-7,  1.492*10**-7, 4.987*10**-7, 5.103*10**-7, 8.679*10**-7]
    depths = [6, 7, 10, 20, 30, 43, 49, 49]
    est_par = [math.exp(1/(0.0016*x+0.1398)) for x in depths]
    fig = px.scatter(x=means,y=stds, color=depths, trendline="ols")
    fig.update_traces(error_x_color="black", marker=dict(size=12, symbol="cross"))
    fig.update_layout(margin=dict(l=100, r=0, b=70, t=0), width = 600, height = 320, title_x = 0.5,
                        showlegend = False, paper_bgcolor='#f7f5f2', plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=14), coloraxis_colorbar=dict(
                                                title="Depth [m]"))

    tr_line=[]
    for  k, trace  in enumerate(fig.data):
            if trace.mode is not None and trace.mode == 'lines':
                tr_line.append(k)

    for id in tr_line:
        fig.data[id].update(line_width=2, line_color="black", line_dash="dot")

    a = round(px.get_trendline_results(fig).px_fit_results.iloc[0].rsquared,2)
    fig.add_annotation(x=0.000002, y=0.0000008, showarrow=False,
                    text=f"R-squared = {a}", bgcolor = "white", font_size=14)
    fig.update_xaxes(title="Mean correlation dimension")
    fig.update_yaxes(title="STD correlation dimension")
    return fig

##------- Functions to plot stats page graphs -------##

def plot_original_distribution(df):
    fig = go.Figure()
    for plfa in df:
        fig.add_trace(go.Box(x=df[plfa], boxpoints='all', name = plfa))
    fig.update_layout(title = "Before transformation", title_x = 0.95,
                    showlegend=False, width=220, height=350, margin=dict(l=20, r=0, b=0, t=30))
    return fig

def plot_pca_components(df, target):
    pca = PCA(n_components=4)
    components = pca.fit_transform(df)

    fig = px.scatter_matrix(
        components,
        dimensions=range(4),
        color=target
    )
    fig.update_traces(diagonal_visible=False)
    fig.update_layout(width=600, height=300, margin=dict(l=40, r=0, b=0, t=10),
                      font=dict(size=1), legend=dict(font_size=12, 
                                                     yanchor="top",
                                                     orientation= "h",
                                                     y=1.02,
                                                     xanchor="left",
                                                     x=-0.03),
                                                     legend_title=None)

    fig.add_annotation(dict(x=0.12, y=0.87,   ax=0, ay=0,
                    xref = "paper", yref = "paper", 
                    font_size=12,
                    text= f'<b>PC1 ({round(pca.explained_variance_ratio_[0]*100,1)}%)</b>'
                  ))
    fig.add_annotation(dict(x=0.38, y=0.63,   ax=0, ay=0,
                    xref = "paper", yref = "paper", 
                    font_size=12,
                    text= f'<b>PC2 ({round(pca.explained_variance_ratio_[1]*100,1)}%)</b>'
                  ))
    fig.add_annotation(dict(x=0.63, y=0.36,   ax=0, ay=0,
                    xref = "paper", yref = "paper", 
                    font_size=12,
                    text= f'<b>PC3 ({round(pca.explained_variance_ratio_[2]*100,1)}%)</b>',
                  ))
    fig.add_annotation(dict(x=0.88, y=0.11,   ax=0, ay=0,
                    xref = "paper", yref = "paper", 
                    font_size=12,
                    text= f'<b>PC4 ({round(pca.explained_variance_ratio_[3]*100,1)}%)</b>'
                  ))
    return fig, pca, components

def plot_2d_scores(components, target):
    sample_names = ["CA06a", "CA06b", "CA06c", "CA10", "CA20", "CA30", "CA43", "CA49"]
    fig = px.scatter(x=components[:,0], y=components[:,1], color=target, text= sample_names)
    fig.update_traces(textposition= "top center",
                      marker=dict(size=12, line=dict(width=2,
                                                     color='DarkSlateGrey')
                                ))
    fig.update_xaxes(title="PC1")
    fig.update_yaxes(title="PC2", range=[-2,4])
    fig.update_layout(width=600, height=310, margin=dict(l=0, r=0, b=0, t=10),
                      legend=dict(font_size=12, 
                                  yanchor="top",
                                  orientation= "h",
                                  y=0.99,
                                  xanchor="right",
                                  x=0.99),
                                  legend_title=None)
    return fig

def plot_biplot(dataset, pca, components):
    loadings = pca.components_
    # Number of features before PCA
    n_features = pca.n_features_in_
    
    # Feature names before PCA
    feature_names = dataset.columns
    
    # PC names
    pc_list = [f'PC{i}' for i in list(range(1, n_features + 1))]
    
    # Match PC names to loadings
    pc_loadings = dict(zip(pc_list, loadings))
    
    # Matrix of corr coefs between feature names and PCs
    loadings_df = pd.DataFrame.from_dict(pc_loadings)
    loadings_df['feature_names'] = feature_names
    loadings_df = loadings_df.set_index('feature_names')
    
    #print(loadings_df.index)
    #text = [plfa.split(" ")[2] for plfa in loadings_df.index]

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=loadings_df["PC1"], y=loadings_df["PC2"], mode="markers+text", marker_size=1,
                            text=loadings_df.index, textposition="top left"), secondary_y=False)
    for i in range(len(loadings_df["PC1"])):
        fig.add_annotation(ax = 0, axref = 'x', ay = 0, ayref = 'y', x = loadings_df["PC1"][i],
                        arrowcolor='blue', xref = 'x', y =loadings_df["PC2"][i],
                        yref='y', arrowwidth=1,arrowside='end',arrowsize=1,arrowhead = 4)
    fig.update_annotations(opacity=0.3)

        
    fig.update_layout(xaxis2= {'anchor': 'y', 'overlaying': 'x', 'side': 'top'},
                    yaxis_domain=[0, 0.94], width=660, height=320, showlegend=False,
                    margin=dict(t=0, b=0, l=0, r=0))

    fig.add_trace(go.Scatter(x=components[:,0], y=components[:,1], mode="markers+text",
                            text=["CA06a", "CA06b", "CA06c", "CA10", "CA20", "CA30", "CA43", "CA49"],
                            textposition="top right",
                            textfont=dict(
                                    size=12,
                                    color="red"
                                ),
                            marker_symbol= "circle",
                            marker_line_color="hotpink", marker_color="lightpink",
                            marker_line_width=2, marker_size=10,), secondary_y=True)
    fig.data[1].update(xaxis='x2')
    fig.update_xaxes(title="PC1",)
    fig.update_yaxes(title="PC2")
    return fig

def plot_kmeans_dendrogram(data_scaled):
    # get data
    data_array = data_scaled
    labels = ["CA06a", "CA06b", "CA06c", "CA10", "CA20", "CA30", "CA43", "CA49"]

    # Initialize figure by creating upper dendrogram
    fig = ff.create_dendrogram(data_array, orientation='bottom', labels=labels)
    for i in range(len(fig['data'])):
        fig['data'][i]['yaxis'] = 'y2'

    # Create Side Dendrogram
    dendro_side = ff.create_dendrogram(data_array, orientation='right')
    for i in range(len(dendro_side['data'])):
        dendro_side['data'][i]['xaxis'] = 'x2'

    # Add Side Dendrogram Data to Figure
    for data in dendro_side['data']:
        fig.add_trace(data)

    # Create Heatmap
    dendro_leaves = dendro_side['layout']['yaxis']['ticktext']
    dendro_leaves = list(map(int, dendro_leaves))
    data_dist = pdist(data_array)
    heat_data = squareform(data_dist)
    heat_data = heat_data[dendro_leaves,:]
    heat_data = heat_data[:,dendro_leaves]

    heatmap = [
        go.Heatmap(
            x = dendro_leaves,
            y = dendro_leaves,
            z = heat_data,
            colorscale = 'Blues'
        )
    ]

    heatmap[0]['x'] = fig['layout']['xaxis']['tickvals']
    heatmap[0]['y'] = dendro_side['layout']['yaxis']['tickvals']

    # Add Heatmap Data to Figure
    for data in heatmap:
        fig.add_trace(data)

    # Edit Layout
    fig.update_layout({'width':680, 'height':680,
                            'showlegend':False, 'hovermode': 'closest',
                            })
    # Edit xaxis
    fig.update_layout(xaxis={'domain': [.15, 1],
                                    'mirror': False,
                                    'showgrid': False,
                                    'showline': False,
                                    'zeroline': False,
                                    'ticks':""})
    # Edit xaxis2
    fig.update_layout(xaxis2={'domain': [0, .15],
                                    'mirror': False,
                                    'showgrid': False,
                                    'showline': False,
                                    'zeroline': False,
                                    'showticklabels': False,
                                    'ticks':""})

    # Edit yaxis
    fig.update_layout(yaxis={'domain': [0, .85],
                                    'mirror': False,
                                    'showgrid': False,
                                    'showline': False,
                                    'zeroline': False,
                                    'showticklabels': False,
                                    'ticks': ""
                            })
    # Edit yaxis2
    fig.update_layout(yaxis2={'domain':[.825, .975],
                                    'mirror': False,
                                    'showgrid': False,
                                    'showline': False,
                                    'zeroline': False,
                                    'showticklabels': False,
                                    'ticks':""})
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig