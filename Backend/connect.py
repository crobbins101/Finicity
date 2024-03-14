import requests
from datetime import datetime
import json
import headers
import subprocess

# Function to calculate the difference in minutes between two timestamps
def calculate_time_difference(timestamp):
    current_time = datetime.now()
    timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    difference = (current_time - timestamp).total_seconds() / 60
    return difference

# Read the timestamp from timestamp.txt
try:
    with open('timestamp.txt', 'r') as timestamp_file:
        timestamp = timestamp_file.read().strip()
except FileNotFoundError:
    timestamp = None

# Check if the timestamp exists and is less than 100 minutes old
if timestamp:
    time_difference = calculate_time_difference(timestamp)
    if time_difference < 100:
        print("No need to generate a new token. Token still valid.")
        # Load token from token.json
        try:
            with open('token.json', 'r') as token_file:
                token_data = json.load(token_file)
                token = token_data['token']
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

        # Read the consumer ID from consumer.json
        try:
            with open('consumer.json', 'r') as consumer_file:
                consumer_data = json.load(consumer_file)
                consumer_id = consumer_data['id']
        except FileNotFoundError:
            print("Consumer file not found.")
            consumer_id = None

        # Check if all token, customer ID, and consumer ID are obtained successfully
        if token and customer_id and consumer_id:
            # Define the API endpoint
            url = 'https://api.finicity.com/connect/v2/generate'

            # Define the headers
            headers_data = {
                'Content-Type': headers.CONTENT_TYPE,
                'Accept': headers.ACCEPT,
                'Finicity-App-Token': token,
                'Finicity-App-Key': headers.APP_KEY,
            }

            # Define the payload data
            data = {
                "language": "en",
                "partnerId": "2445584469258",
                "customerId": customer_id,
                "consumerId": consumer_id,
                "redirectUri": "https://www.peachfinance.com/",
                "webhook": "https://webhook.site/4afa55c6-9bb0-4d0e-9fbc-dba2b7bd15be",
                "webhookContentType": "application/json",
                "optionalConsumerInfo": {
                    "ssn": "999999999",
                    "dob": 1607450357
                },
                "reportCustomFields": [
                    {
                        "label": "PeachloanID",
                        "value": "123456",
                        "shown": True
                    }
                ],
                "isWebView": True
            }

            # Make the POST request
            response = requests.post(url, headers=headers_data, json=data)

            # Check if the request was successful
            if response.status_code == 200:
                # Extract the response text
                response_text = response.text

                # Print the entire response text for debugging
                print("Response Text:", response_text)

                # Save the response text to connect.txt
                with open('connect.txt', 'w') as connect_file:
                    connect_file.write(response_text)

                print("Response saved to connect.txt.")
            else:
                print("Request failed with status code:", response.status_code)
        else:
            print("Failed to obtain token, customer ID, or consumer ID.")
    else:
        print("Token expired. Generating a new token...")
        try:
            # Call auth.py to generate a new token
            auth_output = subprocess.check_output(["python", "auth.py"], stderr=subprocess.STDOUT, universal_newlines=True)
            print("Response from auth.py:")
            print(auth_output)
        except subprocess.CalledProcessError as e:
            print("Error calling auth.py:", e.output)
else:
    print("Timestamp not found. Generating a new token...")
    try:
        # Call auth.py to generate a new token
        auth_output = subprocess.check_output(["python", "auth.py"], stderr=subprocess.STDOUT, universal_newlines=True)
        print("Response from auth.py:")
        print(auth_output)
    except subprocess.CalledProcessError as e:
        print("Error calling auth.py:", e.output)
