import os
import pickle
import pandas as pd
from kdTree import insert_rec
from quadTree import insert_quad

PICKLE_FILE = "data/trees.pkl"
CSV_FILE = "data/US_Accidents_2022_and_up.zip"

# os.remove("data/trees.pkl") # uncomment this to build the tree live before running it

def build_trees():
    # this builds the tree from a pickle of the tree, so that we don't have to remake it each time
    if os.path.exists(PICKLE_FILE):
        with open(PICKLE_FILE, "rb") as f:
            print("loading crash site trees from pickle...")
            return pickle.load(f)

    # if there's no pre-built tree, build from scratch
    print("no pickle found, building tree from scratch...")
    df = pd.read_csv(CSV_FILE)

    kd_root = None
    quad_root = None

    for _, row in df.iterrows():
        point = (row['Start_Lat'], row['Start_Lng'])
        data = {
            'ID': row['ID'],
            'Severity': row['Severity'],
            'City': row['City'],
            'State': row['State'],
            'Zipcode': row['Zipcode']
        }

        kd_root = insert_rec(kd_root, point, data)
        quad_root = insert_quad(quad_root, point, data)

    # pickle it for next time
    with open(PICKLE_FILE, "wb") as f:
        pickle.dump((kd_root, quad_root), f)

    return kd_root, quad_root