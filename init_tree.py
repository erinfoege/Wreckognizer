import os
import pickle
import pandas as pd
from kdTree import insert_rec
from quadTree import insert_quad
import zipfile

PICKLE_FILE = "data/trees.pkl.zip"
CSV_FILE = "data/US_Accidents_2022_and_up.zip"

# os.remove("data/trees.pkl.zip") # uncomment this to build the tree live before running it

def build_trees():
    # this builds the tree from a pickle of the tree, so that we don't have to remake it each time
    if os.path.exists(PICKLE_FILE):
        print("loading trees from zipped pickle file...")
        with zipfile.ZipFile(PICKLE_FILE, 'r') as z:
            with z.open(z.namelist()[0], 'r') as f: # gets the trees.pkl file
                return pickle.load(f)

    # if there's no pre-built tree, build from scratch
    print("no pickle found, building tree from scratch...")
    df = pd.read_csv(CSV_FILE, compression='zip')

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

    # pickle and zip it for next time
    unzipped_pickle = "data/trees.pkl"
    with open(unzipped_pickle, "wb") as f:
        pickle.dump((kd_root, quad_root), f)

    with zipfile.ZipFile(PICKLE_FILE, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(unzipped_pickle, arcname="trees.pkl")

    os.remove(unzipped_pickle) # delete the unzipped file after making the zipped

    return kd_root, quad_root