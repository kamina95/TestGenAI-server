import os

import requests
import json

# Example of constructing a file path with os
file_name = 'classes_tests.json'
file_path = os.path.join(os.getcwd(), "tests_cases", file_name)
# script_directory = Path(__file__).parent
# file_path = script_directory / 'classes_tests.json'
print(file_path)


# URL of the API
api_url = 'http://localhost:8080/api/submit_gpt'

# Load the JSON data from the file
with open(file_path, 'r') as file:
    data = json.load(file)

# Loop through each entry in the JSON data and make the API call
for entry in data:
    # Make the API request with the code and test inputs
    response = requests.post(api_url, json=entry)

    # Check if the request was successful
    if response.status_code == 200:
        print('Request successful:')#, response.json())
    else:
        print('Request failed:') #, response.status_code)
