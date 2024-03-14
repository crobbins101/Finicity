import requests
import json
import headers
from datetime import datetime, timedelta
import subprocess

# Check the timestamp in timestamp.txt
try:
    with open('timestamp.txt', 'r') as timestamp_file:
        timestamp_str = timestamp_file.read().strip()
        last_timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
except FileNotFoundError:
    print("Timestamp file not found.")
    last_timestamp = None

# Check if the last timestamp is older than 100 minutes
if last_timestamp and datetime.now() - last_timestamp < timedelta(minutes=100):
    print("Token still valid.")
else:
    # Call auth.py
    try:
        auth_output = subprocess.check_output(["python", "auth.py"], stderr=subprocess.STDOUT, universal_newlines=True)
        print("Response from auth.py:")
        print(auth_output)
    except subprocess.CalledProcessError as e:
        print("Error calling auth.py:", e.output)

    # Update the timestamp
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('timestamp.txt', 'w') as timestamp_file:
        timestamp_file.write(current_timestamp)
    print("Timestamp updated successfully.")

# Read the authentication token from token.json
try:
    with open('token.json', 'r') as token_file:
        token_data = json.load(token_file)
        token = token_data.get('token')  # Accessing the token using .get() method
except FileNotFoundError:
    print("Token file not found.")
    token = None

# Read the customer ID from customer.json
try:
    with open('customer.json', 'r') as customer_file:
        customer_data = json.load(customer_file)
        customer_id = customer_data['id']
except FileNotFoundError:
    print("Customer file not found.")
    customer_id = None

# Check if both token and customer ID are obtained successfully
if token and customer_id:
    # Define the API endpoint
    url = f'https://api.finicity.com/aggregation/v1/customers/{customer_id}/accounts'

    # Define the headers
    headers_data = {
        'Accept': headers.ACCEPT,
        'Content-Type': headers.CONTENT_TYPE,
        'Finicity-App-Token': token,
        'Finicity-App-Key': headers.APP_KEY
    }

    # Define the data payload
    data = {}

    # Make the POST request
    response = requests.post(url, headers=headers_data, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the json data from the response
        agg_data = response.json()

        # Save the json response to agg.json
        with open('agg.json', 'w') as agg_file:
            json.dump(agg_data, agg_file)

        print("Agg data saved to agg.json.")
    else:
        print("Request failed with status code:", response.status_code)
else:
    print("Failed to obtain token or customer ID.")
