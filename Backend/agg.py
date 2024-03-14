import requests
import json
import headers

# Read the authentication token from token.json
try:
    with open('token.json', 'r') as token_file:
        token_data = json.load(token_file)
        token = token_data['token']
except FileNotFoundError:
    print("Token file not found.")
    token = None

# Read the customer data from customer.json
try:
    with open('customer.json', 'r') as customer_file:
        customer_data = json.load(customer_file)
        customer_id = customer_data['id']  # Read customer ID directly
except FileNotFoundError:
    print("Customer file not found.")
    customer_id = None

# Define the API endpoint
url = f'https://api.finicity.com/aggregation/v1/customers/{customer_id}/accounts'

# Define the headers
headers_data = {
    'Content-Type': headers.CONTENT_TYPE,
    'Accept': headers.ACCEPT,
    'Finicity-App-Token': token,
    'Finicity-App-Key': headers.APP_KEY,
}

# Make the GET request with an empty payload
response = requests.get(url, headers=headers_data, data={})

# Check if the request was successful
if response.status_code == 200:
    # Extract and print the response JSON
    response_json = response.json()
    print("Response JSON:", response_json)

    # Save the response JSON to agg.json
    with open('agg.json', 'w') as json_file:
        json.dump(response_json, json_file)

    print("Response saved to agg.json.")

    # Print the returned data
    returned_data = response_json.get('accounts')
    if returned_data:
        print("Returned Data:", returned_data)
    else:
        print("No account data returned.")
else:
    print("Request failed with status code:", response.status_code)
