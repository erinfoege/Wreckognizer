import pandas as pd
from kdTree import insert_rec, initialize_searches
from quadTree import insert_quad, quad_search

# file_path = "US_Accidents_March23.csv"
# df2 = pd.read_csv(file_path, usecols=['ID', 'Severity', 'Start_Time', 'Start_Lat', 'Start_Lng', 'City', 'State', 'Zipcode'])
#
# # convert 'Start_Time' to datetime format
# df2['Start_Time'] = pd.to_datetime(df2['Start_Time'], errors='coerce')
#
# # filter the data for records starting from 2022
# df_filtered = df2[df2['Start_Time'].dt.year >= 2022]
#
# # save the filtered data to a new CSV file
# output_file = "data/US_Accidents_2022_and_up.csv"
# df_filtered.to_csv(output_file, index=False)
#
#

file_path = "data/US_Accidents_2022_and_up_FL.zip"

# df of ID  Severity, Start_Lat, Start_Long, City, State, Zipcode
df = pd.read_csv(file_path)

root = None
quad_root = None
count = 0
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
    if count == 200000:
        break
    count = count + 1

#print_tree(root)
search_center = (29.6520, -82.3250) #gainesville coords
#search_center = (26.1004, -80.3998) #weston coords

radius = 100  # radius in miles
initialize_searches(root, search_center, radius)
quad_search(quad_root, search_center, radius)

# root = None
# for item in test_data:
#     point = (item['Start_Lat'], item['Start_Long'])
#     data = {
#         'ID': item['ID'],
#         'Severity': item['Severity'],
#         'City': item['City'],
#         'State': item['State'],
#         'Zipcode': item['Zipcode']
#     }
#     root = insert_rec(root, point, data)
#
# print_tree(root)