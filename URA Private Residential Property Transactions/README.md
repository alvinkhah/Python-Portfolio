# URA Private Residential Property Transactions
#### [Tableau visualisation for data downloaded on 01 Feb 2024](https://public.tableau.com/views/URAPrivateResidentialData01Feb2024/URAPrivateResidentialDataon01Feb2024?:language=en-US&:sid=&:display_count=n&:origin=viz_share_link)

## Overview

Most property buyer/seller depends on their property agent or pay a subscription fee to a property platform in order to get the latest transaction prices. 
However, these data have been made readily available and frequently updated by URA. 
Hence, I set out to write a few scripts to enable anyone with some basic coding knowledge to quickly analyse the latest data.
I personally prefer to use VS Code to construct and execute my codes but you can use any program you are comfortable with so long as it can run HTTP and Python codes. 
There are a total of 1 URA account, 1 OneMap account, 2 tokens, 6 python scripts and manual CSV file data entry that need to be tackled.
The final goal here is to visualise using Tableau but you can freely prepare your data for the visualisation/analytical program which you like.

## Data Retrieval
#### [URA API Reference Introduction](https://www.ura.gov.sg/maps/api/#introduction)
#### [URA Private Residential Property Transactions](https://www.ura.gov.sg/maps/api/#private-residential-property-transactions)

First we need to retrieve the data via the URA API which requires us to have an URA account. This is free to create and can be done quickly. Be sure to keep your Access Key private and safe.
Next, we will need a token which is only valid for 1 day. We can either use the link provided by URA via email when we create an URA account or we can use the cURL code provided by URA.
Finally, we will need to download the data. At the time of writing, there are 4 batches of data that needs to be downloaded and the number of batches may vary. Regardless, just changing the number after "batch=" will change the batch which you will download.
The code here are in HTTP file format. 
This is to get a token (valid for 1 day only):
```
curl "https://www.ura.gov.sg/uraDataService/insertNewToken.action"
  -H "AccessKey: <paste your access key here>"
```
This is to download the data in batches (downloaded files are in json format):
```
curl "https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_Resi_Transaction&batch=1"
  -H "AccessKey: <paste your access key here>"
  -H "Token: <paste your token here>"
```

## Data Compiler: Step1

Now that we have the raw data files, place them into a single folder. Next, run the script titled "Step1".
This Python script will compile all the raw files into a single master file while maintaining the json format. 
Do note that the 1st prompt is the name of your 1st raw file and the 2nd prompt is the name of your master file. 3rd prompt onwards will be the rest of your raw files.
It will only compile the "Result" list of dictionaries which contain all the transaction details.
The code itself is heavily documented, so you should have no trouble decipering it if you will like to understand or optimise it further.

## Map Coordinates Converter: Step2
#### [OneMap Coordinate Converters](https://www.onemap.gov.sg/apidocs/apidocs/#coordinateConverters)

All the map coordinates in the raw files are in SVY21 format but Tableau and GoogleMap use WGS84 format. Hence, we will need to convert the coordinates.
Thankfully, OneMap has a coordinate converter which does this conversion. First, register a OneMap account.
Next, at the left panel, go to "Authentication" to find a sample request of how you can request for the token (valid for 3 days only). Click "Python" to see the code in Python.
For your convenience, the Python code is as below and it is also in the file "onemap_auth":
```
import requests
      
url = "https://www.onemap.gov.sg/api/auth/post/getToken"
      
payload = {
        "email":"<paste your email here>",
        "password": "<paste your password here>"
      }
      
response = requests.request("POST", url, json=payload)
      
print(response.text)
```

Next is to subject the master file to the coordinates conversion. Insert authentication token into "headers" at line 48. Run the script titled "Step2".
Enter the name of the file output from "Step1".
Do note that not all properties have coordinates provided and the script will assign None to them.

It is my personal observation that converting close to 300 coordinate pairs at any one time have a high probability of hitting the OneMap API limit.
Hence, "Step2" was designed to feed 250 coordinates at a time and even with a stable internet connection, it will take a while.
Feel free to step away from your computer as a series of 10 incrementally loud beeps will play once the conversions are done.

## Data Flattening: Step3

As the data are nested dictionaries, it will be easier to analyse them when they are flattened. Run the script titled "Step3".
Enter the name of the file output from "Step2".
After this step is completed, the data is ready for Tableau but the properties with missing coordinates will not have them and they will not be plotted on a map.
If you will like to fill in the missing coordinates with estimated coordinates, proceed to the next step.

## Filling in Missing Coordinates: Step4

"Step4" is a script that puts the data into a Pandas dataframe and sieves out the unique properties with missing coordinates then place that into another dataframe.
Enter the name of the file output from "Step3".
It will then prompt you for a file name to save this list of properties (no duplicates) with missing coordinates into a CSV file, so we can manually search GoogleMap and Street Directory for the estimated coordinates. Let's call this file "small" for example.
It will also auto-generate a file with the same name as the file output from "Step3" but in CSV format. Let's call this file "big" for example.

This part is where the manual work comes in. As missing coordinates are usually for new property launches and certain properties which did not caveat their locations, we will need to look into GoogleMap and Street Directory for them.
You can type in the project name and GoogleMap usually have the rough location. For a more exact location, Street Directory is usually more exact. 
However, there is a large group of properties with "Landed Housing Development" as their project name. Therefore, our best guess will be the middle of their streets.
When your cursor is at where you think the property is located, simply right click and you can copy the coordinates to paste by the side of the project name.
Once you have completed filling in the coordinates for all the properties in "small" file, save it as your own record. Then populate what you gathered into "big" file.
Save both files.

## Data Wrangling: Step5

This is the last step of our data wrangling process which helps us convert some data into desired data types, generate new columns such as "price per sqft" and "remaining tenure", etc.
Run the script titled "Step5".
Enter the name of the file output from "Step4". To be more specific, the "big" file.
It will generate a CSV file beginning with "final".
Now you are ready to visualise the data and plot all the properties onto a map.
