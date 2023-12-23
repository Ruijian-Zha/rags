import requests
import json
from urllib.parse import urlparse, urlunparse
import os

def crawling_helper(url_to_crawl, output_directory):
    print("Triggered the recursively crawling")
    # Parse the input URL to construct the match pattern
    parsed_url = urlparse(url_to_crawl)
    path_parts = parsed_url.path.split('/')
    if path_parts[-1]:
        path_parts[-1] = '**'  # Replace the last part with '**'
    else:
        path_parts.append('**')   # If the last part is empty, replace the second last
    match_pattern = urlunparse(parsed_url._replace(path='/'.join(path_parts)))
    print(f"Match pattern added: {match_pattern}")

    # Define the configuration data
    config_data = {
        "url": url_to_crawl,
        "match": match_pattern,
        "maxPagesToCrawl": 10,
        "outputFileName": "/Users/chuci/Documents/GitKraken/gpt-crawler/output-1.json",
    }

    # Convert the config data to JSON and save it as a file
    config_file_path = f"{output_directory}/config.json"
    with open(config_file_path, 'w') as config_file:
        json.dump(config_data, config_file)

    # Define the URL of the API endpoint
    api_url = 'https://apparent-remarkably-satyr.ngrok-free.app/crawl'

    # Open the config file in binary mode to send as a file
    with open(config_file_path, 'rb') as config_file:
        files = {
            'config': ('config.json', config_file, 'application/json')
        }

        # Send the POST request with the file
        response = requests.post(api_url, files=files)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the response content as output.json in the specified output directory
        output_file_path = f"{output_directory}\\output.json"
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(response.text)
        print(f"Output saved as {output_file_path}")

        # Read the saved output.json file
        with open(output_file_path, 'r', encoding='utf-8') as output_file:
            data = json.load(output_file)

        # Create a directory for separated output if it doesn't exist
        separated_output_dir = os.path.join(output_directory, 'separated_output')
        os.makedirs(separated_output_dir, exist_ok=True)

        # Iterate over each dictionary in the list and save it as a separate JSON file
        for index, item in enumerate(data):
            individual_file_path = os.path.join(separated_output_dir, f"{index+1}.json")
            with open(individual_file_path, 'w', encoding='utf-8') as individual_file:
                json.dump(item, individual_file, ensure_ascii=False, indent=4)

        print(f"All items saved in separated JSON files in {separated_output_dir}")
    else:
        print(f"Error: {response.status_code} - {response.text}")