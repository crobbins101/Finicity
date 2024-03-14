import requests
from datetime import datetime, timedelta
import json
import headers

# Function to check if the timestamp is less than 100 minutes old
def is_timestamp_valid(timestamp_str):
    try:
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()
        return current_time - timestamp < timedelta(minutes=100)
    except ValueError:
        return False

# Check if the timestamp is valid
try:
    with open('timestamp.txt', 'r') as timestamp_file:
        timestamp_str = timestamp_file.read().strip()
        if is_timestamp_valid(timestamp_str):
            print("Token still valid.")
            exit()  # Exit the script without generating a new token
except FileNotFoundError:
    pass  # No timestamp file found, proceed to generate a new token

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
    # Parse the JSON response
    data = response.json()

    # Print the token to the screen
    token = data['token']
    print("Token:", token)

    # Save the token to token.json
    with open('token.json', 'w') as token_file:
        json.dump({"token": token}, token_file)
    print("Token saved successfully.")

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

