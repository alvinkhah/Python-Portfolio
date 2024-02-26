# To get OneMap authentication token which is valid for 3 days.

import requests
      
url = "https://www.onemap.gov.sg/api/auth/post/getToken"
      
payload = {
        "email":"<your email here>",
        "password": "<your password here>"
      }
      
response = requests.request("POST", url, json=payload)
      
print(response.text)