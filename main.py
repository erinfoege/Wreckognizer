import pandas as pd

file_path = "data/US_Accidents_March23.csv";

# Read first 100,000 rows
df = pd.read_csv(file_path, usecols=['ID', 'Severity', 'Start_Lat', 'Start_Lng','Zipcode','State', 'City'],
    nrows= 100000)

print(df.head())

df.to_csv("data/US_Accidents_Sample_smaller.csv", index=False)
