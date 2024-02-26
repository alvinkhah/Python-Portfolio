# Step 3: Flatten.
# Flatten "Result" and "transaction" lists into a single list of dictionaries; "transaction" records.
# Convert the various data from str to respective data types or format the str data.
# Extract the processed list of dictionaries into a json file.
# Provide the output file from Step 2. eg. "convert_master_DDMMYYYY".
# Completed output file name will be saved with "processed_" in front at the front. eg. "processed_master_jan2024". It is a json file.


import json as js


# To access json file.
file_name = input("Enter converted file name: ")
fhandle = open(file_name + ".json")
# To decode json file from utf-8 to unicode and load into "batch".
batch = js.load(fhandle)


# To bring the fields at the "Result" list into its nested "transaction" list. ie. Flatten the file.
for i in range(len(batch["Result"])):
    for k in range(len(batch["Result"][i]["transaction"])):
        result_rec = batch["Result"][i] # Simplify the access to result record into a variable.
        trans_rec = batch["Result"][i]["transaction"][k] # Simplify the access to transaction record into a variable.
        
        # Copy marketSegment from result record to transaction record.
        trans_rec["marketSegment"] = result_rec.get("marketSegment", None) # Use .get() method to escape error if that field is null.
        trans_rec.update({"marketSegment":trans_rec["marketSegment"]}) # Create a new key:value pair in each of the transaction record.

        # Copy street from result record to transaction record.
        trans_rec["street"] = result_rec.get("street", None)
        trans_rec.update({"street":trans_rec["street"]})

        # Copy project from result record to transaction record.
        trans_rec["project"] = result_rec.get("project", None)
        trans_rec.update({"project":trans_rec["project"]})

        # Copy longitude from result record to transaction record.
        # Need to remain as string to convert from 3414(SVY21) to 4326(WGS84) aka Google Map format.
        trans_rec["long"] = result_rec.get("x", None)
        trans_rec.update({"long":trans_rec["long"]})

        # Copy latitude from result record to transaction record.
        # Need to remain as string to convert from 3414(SVY21) to 4326(WGS84) aka Google Map format.
        trans_rec["lat"] = result_rec.get("y", None)
        trans_rec.update({"lat":trans_rec["lat"]})

# As all data were in str data type, the following are to convert them into their respective data types or format the str.
        # Convert area from str to float.
        trans_rec.update({"area":float(trans_rec["area"])})

        # Convert noOfUnits from str to int.
        trans_rec.update({"noOfUnits":int(trans_rec["noOfUnits"])})

        # Change format of contractDate from mmyy to yyyy-mm.
        year = trans_rec["contractDate"][2:]
        month = trans_rec["contractDate"][:2]
        new_date = "20" + year + "-" + month
        trans_rec.update({"contractDate":new_date})

        # Convert price from str to float.
        trans_rec.update({"price":float(trans_rec["price"])})


# Put transaction record into a list.
data = []
for a in range(len(batch["Result"])):
    for b in range(len(batch["Result"][a]["transaction"])):
        trans_rec = batch["Result"][a]["transaction"][b] # Simplify the access to transaction record into a variable.
        data.append(trans_rec)


# Serializing json
json_object = js.dumps(data, indent=4)

# To write to a new json file.
date = input("Enter date which data was downloaded in DDMMYYYY format: ").lower()
print(f"Your file will be named: processed_{date}.")
with open("processed_" + date + ".json", "w") as outfile:
    outfile.write(json_object)


print("Data processed and ready for Tableau.")