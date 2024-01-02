import requests
import json

# Configuration
api_base_url = "https://api.fantasypros.com/v2/json/nba/team-stats-allowed/"
headers = {
    'x-api-key': 'CHi8Hy5CEE4khd46XNYL23dCFX96oUdw6qOt1Dnh'
}
timeframes = ['7', '15', '30']

def execute():
    # Loop through each timeframe and fetch data
    for timeframe in timeframes:
        # Construct the filename for each timeframe
        filename = f"2023-24/defense_vpos/team_defense_vpos_{timeframe}.json"

        # Set the parameters for the GET request
        params = {'range': timeframe}

        # Make the GET request to the API
        response = requests.get(api_base_url, headers=headers, params=params)

        # Check if the response is OK (status code 200)
        if response.status_code == 200:
            # Save the data to a file for each timeframe
            with open(filename, 'w') as file:
                json.dump(response.json(), file, indent=4)
            #print(f"Data for timeframe {timeframe} saved to {filename}.")
        else:
            print(f"Failed to fetch data for timeframe {timeframe}. Status code: {response.status_code}")

    #print("Data fetching complete.")
