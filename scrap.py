import requests
from bs4 import BeautifulSoup
import os

def scrape_website(url, output_folder):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Create the output folder if it doesn't exist
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Save the HTML content to a file
            html_file_path = os.path.join(output_folder, 'index.html')
            with open(html_file_path, 'w', encoding='utf-8') as html_file:
                html_file.write(str(soup))
            print(f"HTML content saved to {html_file_path}")

            # Download and save CSS files
            css_links = soup.find_all('link', rel='stylesheet')
            for link in css_links:
                css_url = link.get('href')
                if css_url.startswith('http'):
                    css_response = requests.get(css_url)
                    if css_response.status_code == 200:
                        css_file_path = os.path.join(output_folder, os.path.basename(css_url))
                        with open(css_file_path, 'wb') as css_file:
                            css_file.write(css_response.content)
                        print(f"CSS file saved: {css_file_path}")
                else:
                    print(f"Skipping CSS link: {css_url}")

        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Example usage
url = 'https://www.chase.com/'
output_folder = 'website_data'
scrape_website(url, output_folder)
