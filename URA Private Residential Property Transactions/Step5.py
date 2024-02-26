# Step 5: Data wrangling.
# After missing coords were filled in, we further organise the data by renaming columns and deriving values from columns such as price per sqft.
# As there may be some inconsistency in data under "tenure", some editing may be required in the csv file before input.


import pandas as pd
from datetime import datetime


# Read csv file into a dataframe. 
# "index_col=0" to prevent auto-creation of an unnamed index column. "df.index" to start index from 1 instead of 0.
filename = input("Enter file name for data wrangling: ")
df = pd.read_csv(filename + ".csv", index_col=0)
df.index = range(1, len(df)+1)


# Changing to desired column names. "inplace=True" to commit to the change.
df.rename(columns={"area": "area_sqm", "floorRange": "floor_range", "noOfUnits": "no_of_units", "contractDate": "trans_yearmonth", "typeOfSale": "type_of_sale", "propertyType": "property_type", "typeOfArea": "type_of_area", "marketSegment": "market_segment", "nettPrice": "discounted_price"}, inplace=True)


# Create a column for area in sqft.
df["area_sqft"] = round(df["area_sqm"] * 10.76391042, 1)


# Create a column for price per sqft.
df["diff_price"] = pd.isnull(df["discounted_price"])

def ppsf(row):
    if row["diff_price"]:
        return round((row["price"] / row["area_sqft"]), 2)
    else:
        return round((row["discounted_price"] / row["area_sqft"]), 2)

df["price_psf"] = df.apply(ppsf, axis=1)

df.drop(columns=['diff_price'], inplace=True)


# Calculate remaining lease.
def remain(row):
    lease_length = []
    if row["tenure"] != "Freehold":
        for char in row["tenure"]:
            if char.isnumeric():
                lease_length.append(char)
            else:
                break
        lease = "".join(lease_length)
        lease = int(lease)
        start_year = int(row["tenure"][-4:])
        current_year = datetime.now().year
        return lease - (current_year - start_year)
    else:
        return "Freehold"

df["remaining_lease"] = df.apply(remain, axis=1)


# Change floor range from "06-10" which is mistaken as date to another format of "06 TO 10".
def correct_floor_range(row):
    if row["floor_range"] == "-":
        return None
    elif row["floor_range"] == "1-May":
        return "01 TO 05"
    elif row["floor_range"] == "6-Oct":
        return "06 TO 10"
    elif row["floor_range"] == "Nov-15":
        return "11 TO 15"
    else:
        low_range = row["floor_range"].split("-")[0]
        high_range = row["floor_range"].split("-")[1]
        return low_range + " TO " + high_range

df["floor_range"] = df.apply(correct_floor_range, axis=1)


# Change type_of_sale from "1", "2" or "3" to "New Sale", "Sub Sale" and "Resale", respectively.
def sale_in_words(row):
    if row["type_of_sale"] == 1:
        return "New Sale"
    elif row["type_of_sale"] == 2:
        return "Sub Sale"
    else:
        return "Resale"

df["type_of_sale"] = df.apply(sale_in_words, axis=1)
#print(df.columns)

#print(df.info())
#print(df.head(10))

# To write dataframe into a csv file.
df.to_csv("final_" + filename + ".csv", index=False)