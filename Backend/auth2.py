import requests
from datetime import datetime
import headers

# API endpoint and headers
url = 'https://api.finicity.com/aggregation/v2/partners/authentication'
api_headers = {
    'Content-Type': headers.CONTENT_TYPE,
    'Finicity-App-Key': headers.APP_KEY,
    'Accept': headers.ACCEPT,
}

# Request payload
payload = {
    "partnerId": headers.PARTNER_ID,
    "partnerSecret": headers.PARTNER_SECRET
}

# Make the API call
response = requests.post(url, headers=api_headers, json=payload)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Get the timestamp of the successful response
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp in a readable format

    # Print the timestamp to the screen
    print("Timestamp:", timestamp)

    # Save the timestamp to timestamp.txt
    try:
        with open('timestamp.txt', 'w') as file:
            file.write(timestamp)
        print("Timestamp saved successfully.")
    except IOError as e:
        print("Error occurred while saving the timestamp:", e)
else:
    print(f"Failed to make API call. Status code: {response.status_code}")

print("End of script")
