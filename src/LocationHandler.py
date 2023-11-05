import requests
import os
from dotenv import load_dotenv


class LocationHandler:
    def __init__(self):
        """Constructor function to set up environmental variables"""
        load_dotenv()
        self.mapquest_api_key = os.environ.get("MAPQUEST_API_KEY")


    def getDistance(self, address1, address2):
        """Returns the time, in seconds, that it takes to travel from one address to another. Returns -1 if the
        API request fails. Returns -2 if a different error occurs. Accepts two addresses, like the following example;
        “750 Synergy Park Blvd, Richardson, TX”."""
        # Ensure all whitespace is removed from the strings
        address1 = address1.replace(' ', '+')
        address2 = address2.replace(' ', '+')
        url = f'https://www.mapquestapi.com/directions/v2/route?key={self.mapquest_api_key}&from={address1}&to={address2}'
        try:
            response = requests.get(url)  # Attempt to make the request
            if response.status_code == 200:  # Check that request was successful
                data = response.json()
                return data['route']['realTime']  # Return the time in seconds
            else:
                print(f"Request failed with status code {response.status_code}")
                return -1
        except Exception as e:
            print("Failed to make request:\n" + str(e))
            return -2
