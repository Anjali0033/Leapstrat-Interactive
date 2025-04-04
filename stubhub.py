import requests
from lxml import html
import json

# Function to scrape and process event data
def scrapper(url):
    session = requests.Session()
    headers = {
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'priority': 'u=1, i',
        'referer': 'https://www.stubhub.com/explore?lat=MjUuNDQ3ODkwMw%3D%3D&lon=LTgwLjQ3OTIxOTY%3D&to=253402300799999&tlcId=2',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'DNT': '1',
    }
    session.headers.update(headers)

    # Make the request
    response = session.get(url)
    if response.status_code != 200:
        print("Failed to fetch the webpage.")
        return None
    
    # Parsing the JSON response
    try:
        data = json.loads(response.text)
    except json.JSONDecodeError:
        print("Failed to decode JSON.")
        return None

    # Collect events
    events = []
    for event in data.get('events', []):
        event_info = {
            'title': event.get('name', ''),
            'datetime': f"{event.get('formattedDateWithoutYear', '')} {event.get('formattedTime', '')}",
            'location': event.get('formattedVenueLocation', ''),
            'image_link': event.get('imageUrl', ''),
            'event_link': event.get('url', '')
        }
        events.append(event_info)

        # 5 events
        if len(events) >= 5:
            break

    # Return events as JSON string
    return json.dumps(events, indent=4)

# URL for event data
url = 'https://www.stubhub.com/explore?method=getExploreEvents&lat=MjUuNDQ3ODkwMw%3D%3D&lon=LTgwLjQ3OTIxOTY%3D&to=253402300799999&tlcId=2'

events_data = scrapper(url)

# If successful, print and save data to file
if events_data:
    print("Event data:")
    print(events_data)
    
    try:
        # Save data to a JSON file
        with open('events_data.json', 'w') as f:
            f.write(events_data)
        print("Data saved to 'events_data.json'.")
    except Exception as e:
        print(f"Error saving data: {e}")
