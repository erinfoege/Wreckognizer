import pandas as pd
from kdTree import insert_rec, bfs_search, dfs_search
from quadTree import insert_quad, quad_search

file_path = "data/US_Accidents_2022_and_up.zip"

# df of ID  Severity, Start_Lat, Start_Long, City, State, Zipcode
df = pd.read_csv(file_path)

root = None
quad_root = None

for index, row in df.iterrows():
    point = (row['Start_Lat'], row['Start_Lng'])
    data = {
        'ID': row['ID'],
        'Severity': row['Severity'],
        'City': row['City'],
        'State': row['State'],
        'Zipcode': row['Zipcode']
    }
    root = insert_rec(root, point, data)
    quad_root = insert_quad(quad_root, point, data)

#print_tree(root)
search_center = (29.6520, -82.3250) #gainesville coords
#search_center = (26.1004, -80.3998) #weston coords

radius = 100  # radius in miles
#bfs_search(root, search_center, radius)
dfs_search(root, search_center, radius)
quad_search(quad_root, search_center, radius)
