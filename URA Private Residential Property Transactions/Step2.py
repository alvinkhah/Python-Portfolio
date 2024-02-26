# Step 2: Coordinates converter.
# Convert coordinates from 3414(SVY21) to 4326(WGS84) aka Google Map format via OneMap Coordinates Converter.
# Extract the processed list of dictionaries into a json file.
# Note: Status Code must be "200" for all coords to be fully converted. If it is "429", it meant API limit was exceeded.

# When coords were not given by URA, they will also be stated as null, just like if they were not converted. 
# If coords were not given by URA, coords will be stated after "marketSegment" in the output file. If unconverted, they will be with "street" and "project".

# Provide the output file from Compiler.py. eg. "master_jan2024".
# After program is done, a sound will play.


import json as js
import requests
import winsound


# Create a temp file for coord conversion in batches of 250 coords at a time.
# To access json file.
file_name = (input("Enter file name for coordinates conversion: ") + ".json")
fhandle = open(file_name)
# To decode json file from utf-8 to unicode and load into "batch".
batch = js.load(fhandle)
# Serializing json
json_object = js.dumps(batch, indent=4)
# To write to a new json file.
with open("temp_" + file_name, "w") as outfile:
    outfile.write(json_object)

temp_file_name = "temp_" + file_name


# 250 records will have coordinates converted at one time. 
# This is to find out the number of such batches that need to be converted.
mul = [x for x in range(0, 30250, 250)]

def upper_range_limit_(total_num_of_rec):
    for s in range(len(mul)):
        if total_num_of_rec - mul[s] <= 0:
            return mul.index(mul[s])
        else:
            continue

counter = upper_range_limit_(len(batch["Result"])) - 1


# Insert valid OneMap Authentication token in headers.
headers = {"Authorization": "<your authentication token here>"}


#while counter > 0:
# To access json file.
temp_fhandle = open(temp_file_name)
# To decode json file from utf-8 to unicode and load into "batch".
temp_batch = js.load(temp_fhandle)
for m in range(counter):
    for n in range(mul[m], mul[m+1]):
        temp_trans_rec = temp_batch["Result"][n]

        url_base = "https://www.onemap.gov.sg/api/common/convert/3414to4326"

        # Try-except block to insert None for "x" and "y" when they are not provided.
        try:
            parameters = {
                "X" : temp_trans_rec["x"],
                "Y" : temp_trans_rec["y"]
            }

            response = requests.get(url_base, params = parameters, headers=headers)

            coord = dict(js.loads(response.text))

            temp_trans_rec.update({"x":coord["longitude"]})
            temp_trans_rec.update({"y":coord["latitude"]})
        except:
            temp_trans_rec.update({"x":None})
            temp_trans_rec.update({"y":None})

    if response.status_code == 200:
        print(f"Status Code 200. All coordinates up to the {mul[m+1]}th property were converted.")
    elif response.status_code == 429:
        print("Status Code 429. API limit exceeded. Unconverted coordinates are listed as null.")
    else:
        print("An error with the API occurred.")

#counter -= 1

# Serializing json
temp_json_object = js.dumps(temp_batch, indent=4)
# To write to a new json file.
with open(temp_file_name, "w") as temp_outfile:
    temp_outfile.write(temp_json_object)


if len(batch["Result"]) - mul[counter] > 0:
    # To access json file.
    last_fhandle = open(temp_file_name)
    # To decode json file from utf-8 to unicode and load into "batch".
    last_batch = js.load(last_fhandle)
    for o in range(mul[counter], len(batch["Result"])):
        last_trans_rec = last_batch["Result"][o]

        url_base = "https://www.onemap.gov.sg/api/common/convert/3414to4326"

        # Try-except block to insert None for "x" and "y" when they are not provided.
        try:
            parameters = {
                "X" : last_trans_rec["x"],
                "Y" : last_trans_rec["y"]
            }

            response = requests.get(url_base, params = parameters, headers=headers)

            coord = dict(js.loads(response.text))

            last_trans_rec.update({"x":coord["longitude"]})
            last_trans_rec.update({"y":coord["latitude"]})
        except:
            last_trans_rec.update({"x":None})
            last_trans_rec.update({"y":None})

    if response.status_code == 200:
        print(f"Status Code 200. All {len(batch['Result'])} coordinates were converted.")
    elif response.status_code == 429:
        print("Status Code 429. API limit exceeded. Unconverted coordinates are listed as null.")
    else:
        print("An error with the API occurred.")


    # Serializing json
    last_json_object = js.dumps(last_batch, indent=4)
    print(f"Your converted file will be named: converted_{file_name}.")
    # To write to a new json file.
    with open("converted_" + file_name, "w") as last_outfile:
        last_outfile.write(last_json_object)


print("Cooordinates conversion completed.\n")


# Play 5 beeps when the program is done running.
 
freq = 100
dur = 50
 
# loop iterates 10 times i.e, 10 beeps will be produced.
for i in range(0, 10):    
    winsound.Beep(freq, dur)    
    freq += 100
    dur += 50