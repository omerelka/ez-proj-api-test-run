import requests
import json
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter


def fetch_all_plants(token):
    base_url = 'https://trefle.io/api/v1/plants'
    all_plants = []
    page = 1

    while True:
        params = {
            'token': token,
            'page': page
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            # Add plants from current page
            all_plants.extend(data['data'])

            # Check if there's a next page
            if 'next' not in data['links'] or data['links']['next'] is None:
                break

            page += 1
            print(f"Fetching page {page}...")

        except requests.RequestException as e:
            print(f"Error fetching plants: {e}")
            break

    return all_plants


def pretty_print_json(data):
    # Convert to formatted JSON string
    formatted_json = json.dumps(data, indent=4)

    # Colorful terminal output
    print(highlight(formatted_json, JsonLexer(), TerminalFormatter()))

def save_plants_to_file(all_plants, filename='plants_data.txt'):
   try:
       with open(filename, 'w', encoding='utf-8') as file:
           json.dump(all_plants, file, indent=4, ensure_ascii=False)
       print(f"Data saved to {filename}")
   except Exception as e:
       print(f"Error saving file: {e}")

def main():
    token = 'XcGpvb5czAnA9eBDhqsezSzvJ12YIwjBvBjaXbNN3IA'
    all_plants = fetch_all_plants(token)
    save_plants_to_file(all_plants)

    print(f"\nTotal plants fetched: {len(all_plants)}")

    # Optional: print the first few or all plants
    # pretty_print_json(all_plants[:10])  # First 10
    # or
    # pretty_print_json(all_plants)  # All plants


if __name__ == '__main__':
    main()