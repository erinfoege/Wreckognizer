import pandas as pd

file_path = "data/US_Accidents_Sample_smaller.zip";

# df of ID  Severity, Start_Lat, Start_Long, City, State, Zipcode
df = pd.read_csv(file_path)

print(df)


