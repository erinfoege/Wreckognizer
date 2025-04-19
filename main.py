import pandas as pd
from kdTree import insert_rec, print_tree, bfs_with_pruning

# file_path = "US_Accidents_March23.csv"
# df2 = pd.read_csv(file_path, usecols=['ID', 'Severity', 'Start_Time', 'Start_Lat', 'Start_Lng', 'City', 'State', 'Zipcode'])
#
# # Convert 'Start_Time' to datetime format
# df2['Start_Time'] = pd.to_datetime(df2['Start_Time'], errors='coerce')
#
# # Filter the data for records starting from 2022 and onward
# df_filtered = df2[df2['Start_Time'].dt.year >= 2022]
#
# # Save the filtered data to a new CSV file
# output_file = "data/US_Accidents_2022_and_up.csv"
# df_filtered.to_csv(output_file, index=False)
#
#

file_path = "data/US_Accidents_2022_and_up.zip"

# df of ID  Severity, Start_Lat, Start_Long, City, State, Zipcode
df = pd.read_csv(file_path)

root = None
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


print_tree(root)

search_center = (29.6520, -82.3250)
radius = 5  # Radius in miles

results = bfs_with_pruning(root, search_center, radius)

print(f"Accidents within {radius} miles of {search_center}:")
for result in results:
    print(result)
    print("hi")

test_data = [
    {'ID': 1, 'Start_Lat': 29.0002, 'Start_Long': -81.065, 'Severity': 3, 'City': 'Daytona Beach', 'State': 'FL', 'Zipcode': '32118'},
    {'ID': 2, 'Start_Lat': 29.0003, 'Start_Long': -81.066, 'Severity': 2, 'City': 'Orlando', 'State': 'FL', 'Zipcode': '32801'},
    {'ID': 3, 'Start_Lat': 29.0004, 'Start_Long': -81.067, 'Severity': 1, 'City': 'Jacksonville', 'State': 'FL', 'Zipcode': '32202'}
]

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