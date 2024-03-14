import requests
import json
import headers
from datetime import datetime, timedelta

# Read the authentication token from token.json
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

# Calculate from and to dates
to_date = int(datetime.now().timestamp())
from_date = int((datetime.now() - timedelta(days=90)).timestamp())

# Define the API endpoint with dynamic from and to dates
url = f'https://api.finicity.com/aggregation/v3/customers/{customer_id}/transactions?includePending=true&fromDate={from_date}&toDate={to_date}'

# Define the headers
headers_data = {
    'Finicity-App-Key': headers.APP_KEY,
    'Accept': headers.ACCEPT,
    'Finicity-App-Token': token,
}

# Make the GET request
response = requests.get(url, headers=headers_data)

# Check if the request was successful
if response.status_code == 200:
    # Extract and print the response JSON
    response_json = response.json()
    print("Response JSON:", response_json)
else:
    print("Request failed with status code:", response.status_code)
