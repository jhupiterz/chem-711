import pandas as pd
import numpy as np
import os
from ast import literal_eval

##------- Functions for building the 3D and 4D visualizations -------##
def load_data_from_csv(file_name):
    """To use if correlation dimension already computed and saved into CSV file.
       Takes the sample name as a string, reads the corresponding CSV file
       and returns a dataframe of vertices and faces."""
    sample_df = pd.read_csv(f"data/{file_name}.csv")
    sample_df['Faces'] = sample_df.Faces.apply(lambda x: literal_eval(str(x)))
    return sample_df

def create_coordinates(sample_df):
    """Creates a coordinates column with the [x,y,z] coordinates of each vertex"""
    coordinates = []
    for index in range(len(sample_df)):
        coordinates.append(np.array((sample_df.iloc[index]["X"], sample_df.iloc[index]["Y"], sample_df.iloc[index]["Z"])))
    sample_df["coordinates"] = coordinates
    return sample_df

def get_i_j_k(sample_df):
    i = []
    j = []
    k = []
    for _, row in sample_df.iterrows():
        i.append(row["Faces"][0])
        j.append(row["Faces"][1])
        k.append(row["Faces"][2])

    sample_df["I"] = i
    sample_df["J"] = j
    sample_df["K"] = k
    return sample_df

def get_prepared_dataframe(file_name):
    sample_df = load_data_from_csv(file_name)
    sample_df = create_coordinates(sample_df)
    sample_df = get_i_j_k(sample_df)
    return sample_df

##------- Functions for plotting the Minkowski-Bouligand fractal dims -------##
def get_data_dict():
    files = ["CA43.txt", "polyCA06a.txt", "CA06b.txt", "CA30.txt", "CA49.txt", "CA49_stick.txt", "CA49_1.txt", "cube.txt", "full_cone.txt"]
    data = {}
    for file in files:
        df = pd.read_csv(f"data/{file}", sep=" ", header=None)
        df.columns = ["line_ID", "dilation_radiua", "log(dilation_radius)", "log(influence_volume)"]
        data[file.strip(".txt")] = df
    return data

def get_master_dataframe():
    data_dict = get_data_dict()
    master_dataframe = pd.DataFrame()
    for sample in data_dict:
        df = data_dict[sample]
        df["sample"] = sample
        df["sample"] = df["sample"].map({"CA43": "CA43", "CA06b": "CA06b", "polyCA06a": "CA06a",
                                         "CA30": "CA30", "CA49": "CA49a", "CA49_stick": "CA49_stick",
                                         "aragonite_2": "crystalline aragonite",
                                         "aragonite_2": "oolithic aragonite",
                                         "CA49_1": "CA49b", "cube": "cube", "full_cone": "cone"})
        master_dataframe = pd.concat([master_dataframe, df])
    return master_dataframe

##------- Functions to get the chromatogram data -------##
def get_plfa_data(sample):
    df = pd.read_csv(f"data/chromatograms/plfa/{sample}_geochem.CSV")
    df.drop(labels= [0, 1], axis = 0, inplace = True)
    df.drop(labels= ["Date Acquired", "Sample", "Misc"], axis = 1, inplace = True)
    df.columns = ["Retention time", "Count"]
    df["Sample"] = sample
    df["Retention time"] = pd.to_numeric(df["Retention time"], errors='coerce')
    df["Count"] = pd.to_numeric(df["Count"], errors='coerce')
    return df

def get_master_plfa_data():
    df = pd.DataFrame()
    for file in os.listdir("data/chromatograms/plfa"):
        sample = file.rstrip("_geochem.CSV")
        df = pd.concat([df, get_plfa_data(sample)])
    return df

##------- Functions to get the chromatogram data -------##
def get_alkane_data(sample):
    df = pd.read_csv(f"data/chromatograms/alkane/{sample}_geochem_ALK.CSV")
    df.drop(labels= [0, 1], axis = 0, inplace = True)
    df.drop(labels= ["Date Acquired", "Sample", "Misc"], axis = 1, inplace = True)
    df.columns = ["Retention time", "Count"]
    df["Sample"] = sample
    df["Retention time"] = pd.to_numeric(df["Retention time"], errors='coerce')
    df["Count"] = pd.to_numeric(df["Count"], errors='coerce')
    return df

def get_master_alkane_data():
    df = pd.DataFrame()
    for file in os.listdir("data/chromatograms/alkane"):
        sample = file.rstrip("_geochem_ALK.CSV")
        df = pd.concat([df, get_alkane_data(sample)])
    return df