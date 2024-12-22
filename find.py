#!/usr/bin/env python3  # Shebang for Linux users to run the script directly

import requests
from bs4 import BeautifulSoup
import re
import pyfiglet
import os  # To handle cross-platform paths

def print_sudo_su_logo():
    # Generate ASCII art for "sudo su"
    ascii_art = pyfiglet.figlet_format("sudo su", font="slant")  # You can change the font if desired
    print(ascii_art)

def find_api_documentation(url):
    try:
        # Fetch the content of the URL
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch URL: {url}. Status code: {response.status_code}")
            return

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Define an array of keywords and URL patterns to search for API documentation
        doc_patterns = [
            '/swagger',           # Swagger documentation
            '/swagger-ui',        # Swagger UI
            '/docs',              # General API docs
            '/swagger.json',      # Swagger JSON file
            '/openapi.json',      # OpenAPI JSON file
            '/postman',           # Postman-related docs
            '/docs/postman',      # Postman docs
            '/api-docs',          # Common API documentation endpoint
            '/raml',              # RAML API documentation
            '/reference',         # API reference docs
            '/developer',         # Developer docs
            '/api',               # Any general API endpoint
            '/api/v1',            # API version 1
            '/api/v2',            # API version 2
            '/api/v3'             # API version 3
        ]
        
        found_docs = False
        
        # Get all elements on the page and search for URLs
        elements = soup.find_all(['a', 'img', 'script', 'link'])  # Check anchor, image, script, and link tags
        for element in elements:
            # Extract URL from href or src attributes
            content = element.get('href', '') + element.get('src', '')
            urls = re.findall(r'https?://[^\s"]+', content)  # Match URLs in the content
            
            for url in urls:
                # Check if the URL contains any of the API documentation patterns
                for pattern in doc_patterns:
                    if pattern in url:
                        found_docs = True
                        print(f"API Documentation link found: {url}")

                # Additionally check for URLs containing .api or /api
                if '.api' in url or '/api' in url:
                    found_docs = True
                    print(f"API link found: {url}")

        # If no documentation link was found
        if not found_docs:
            print("No API documentation link found")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")

# Main script execution
print_sudo_su_logo()  # Display the custom "sudo su" ASCII art

# Ask for URL input from the user
url_input = input("Enter a URL to check for API documentation: ")

# Call the function to check for API documentation
find_api_documentation(url_input)