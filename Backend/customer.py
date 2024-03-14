import os
import requests
import json
import headers
import random
import string
from datetime import datetime, timedelta
import subprocess

# Function to generate a random username
def generate_username():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))

# Check if timestamp.txt exists and has a valid timestamp
if os.path.exists('timestamp.txt'):
    try:
        with open('timestamp.txt', 'r') as timestamp_file:
            timestamp_str = timestamp_file.read().strip()
            last_timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    except (ValueError, IOError) as e:
        print("Error reading timestamp file:", e)
        last_timestamp = None
else:
    print("Timestamp file not found.")
    last_timestamp = None

# Check if the last timestamp is more than 100 minutes ago
if last_timestamp and datetime.now() - last_timestamp > timedelta(minutes=100):
    # Call auth.py to generate a new token
    try:
        subprocess.run(["python", "auth.py"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error generating new token:", e)
    else:
        print("New token generated successfully.")
else:
    print("No need to generate a new token at this time.")

# Read the authentication token from token.json
try:
    with open('token.json', 'r') as token_file:
        token_data = json.load(token_file)
        token = token_data['token']
except FileNotFoundError:
    print("Token file not found.")
    token = None

# Check if the token is obtained successfully
if token:
    # Generate random username
    username = generate_username()

    # Define the API endpoint
    url = 'https://api.finicity.com/aggregation/v2/customers/testing'

    # Define the headers with the obtained token
    headers_data = {
        'Content-Type': headers.CONTENT_TYPE,
        'Accept': headers.ACCEPT,
        'Finicity-App-Key': headers.APP_KEY,
        'Finicity-App-Token': token  # Assign the obtained token here
    }

    # Define the data payload
    data = {
        "username": username,
        "firstName": "John",
        "lastName": "Smith"
    }

    # Make the POST request
    response = requests.post(url, headers=headers_data, json=data)

    # Check if the request was successful
    if response.status_code == 201:
        # Extract the customer data from the response
        customer_data = response.json()

        # Print the customer id and username to the screen
        print("Customer ID:", customer_data['id'])
        print("Username:", username)

        # Save the customer data to customer.json
        with open('customer.json', 'w') as customer_file:
            json.dump(customer_data, customer_file)

        print("Customer data saved to customer.json.")

        # You can use the customer id in other parts of your code as needed
    else:
        print("Request failed with status code:", response.status_code)
else:
    print("Failed to obtain token.")
