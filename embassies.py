import requests
import csv
import pycountry
import sys

def get_embassies(api_key, country, input_country):
    endpoint = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    query = f"{input_country} embassy in {country}"

    params = {
        'query': query,
        'key': api_key
    }

    response = requests.get(endpoint, params=params)
    results = response.json().get('results', [])
    return results

def should_exclude_address(address, name, input_country):
    return f"{input_country.capitalize()}" in address or f"{input_country.capitalize()}" not in name

def generate_csv(country, data, filename , input_country):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for place in data:
            name = place.get('name', 'N/A')
            address = place.get('formatted_address', 'N/A')
            place_id = place.get('place_id', '')
            google_maps_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"

            if not should_exclude_address(address, name, input_country):
                writer.writerow([country, name, address, google_maps_url])

def main():
    if len(sys.argv) != 2:
        print("To use the code type: python embassies.py <country>")
        sys.exit(1)

    api_key = 'AIzaSyBobPrpAfV2cyTVn2HkmTrG4SMLx-jdy-U'
    all_country_names = [country.name for country in pycountry.countries]
    input_country = sys.argv[1]
    output_filename = f"{input_country}_embassies_worldwide_filtered.csv"

    with open(output_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Country', 'Embassy Name', 'Embassy Address', 'Google Maps URL'])

    for country in all_country_names:
        embassies = get_embassies(api_key, country, input_country)

        if embassies:
            generate_csv(country, embassies, output_filename, input_country)
            print(f"Embassies in {country} added to '{output_filename}'")
            # print(f"country: {country} , embassies: {embassies}, input_country: {input_country}")
        else:
            print(f"No embassies found in {country}")

if __name__ == "__main__":
    main()