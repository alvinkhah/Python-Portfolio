# Step 1: Compiler.
# To bring all the downloaded raw files from URA into a single master file, combining all the "Result" records.
# To convert the raw json file into a more readable presentation.

# Provide raw file from URA.
# Output master file from this program will be a nicely indented json file.


import json as js


# To have a counter for the number of files to combine.
counter = int(input("Enter total number of raw files to combine: "))


# To access the first raw data file.
first_fhandle = open(input("Enter name of first raw file: ") + ".json")
# To decode json file from utf-8 to unicode and load into "batch".
first_batch = js.load(first_fhandle)

# Serializing json
first_json_object = js.dumps(first_batch, indent=4)

# To create a master json file which compiles all "Result" records. 
# Suggested master file name "master_DDMMYYYY".
master_file = input("Enter name of master file: ") + ".json"
with open(master_file, "w") as outfile:
    outfile.write(first_json_object)


# To open the newly created master file.
master_fhandle = open(master_file)
master_batch = js.load(master_fhandle)    

# To extend the "Result" list with the "Result" lists from other raw files.
while counter - 1 > 0:
    next_fhandle = open(input("Enter name of next raw file: ") + ".json")  # Open the next raw file to compile.
    next_batch = js.load(next_fhandle)
    #for e in range(len(next_batch["Result"])):
    next_result_rec = next_batch["Result"]                   # Simplify the access to result record into a variable.
        
    master_batch["Result"].extend(next_result_rec)
    counter -= 1
# After while loop is done, the code under "else" below will update master file.
else:
    # Serializing json
    master_json_object = js.dumps(master_batch, indent=4)

    # To write to a new json file.
    with open(master_file, "w") as outfile:
        outfile.write(master_json_object)


print("Compilation completed.\n")