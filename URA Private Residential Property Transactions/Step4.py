# Step 4: Missing coordinates and inconsistent "tenure" data entry.
# After data is flattened into a "processed" file, you can fill in missing coordinates using Excel, Google Map and Street Directory.


import json as js
import pandas as pd


# To access the first raw data file.
filename = input("Enter file name with missing coords: ")
fhandle = open(filename + ".json")
# To decode json file from utf-8 to unicode and load into "batch".
batch = js.load(fhandle)


# Put processed data into a dataframe.
df = pd.DataFrame(batch)

# To query df.
print(df.head(50))
print(df.shape)

# To find those unique street + project combinations with missing coords.
df_missing_coords = df[["street", "project"]][df['lat'].isna()]
#print(df_missing_coords.nunique())
uniq = df_missing_coords.drop_duplicates()
print(uniq)

# To write uniq dataframe into a csv file to see all the properties with missing coords. "index=False" to prevent auto-creation on an unnamed index column.
# Note: floor range may auto convert to date format. Eg. if "06-10", it will be converted to "6-Oct". Rectifying it in Excel does not help. When using Pandas to open the file again, the floor range will change back, so no need to be bothered about it.
print("""
Do 2 things in Excel:
      1) Populate the csv file with 'lat' and 'long' columns for each row.
      2) Ensure data in "tenure" column are in a consistent format.
      """)

uniq.to_csv(input("Enter file name for properties with missing coords: ") + ".csv", index=False)
df.to_csv(filename + ".csv", index=False)


# Further instructions.
print("""
Further instruction:

After manually searching for the estimated coords for the properties with missing coords,
fill in the estimated coords into the main csv file and save this file with the unique list of properties with estimated coords.
Working through Excel to populate the csv file was found to be faster and adaptable to future changes.
The unique list of properties will allow for comparison with future URA datasets.
    """)