import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

def downloadCars(site):
    print(f"Bearbeite Seite {site}")
    payload = {}
    headers = {
        'authority': 'v3-66-1.gsl.feature-app.io',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'Dnt': '1',
        'Origin': 'https://volkswagen.de',
        'Priority': 'u=1, i',
        'Referer': 'https://volkswagen.de',
        'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    url = f"https://v3-66-1.gsl.feature-app.io/bff/car/search?t_manuf=BQ&sort=DATE_OFFER&sortdirection=ASC&pageitems=12&page={site}&market=passenger&country=DE&language=de&oneapiKey=nOqkwPxxu8ViK9aaHvTkglzVZAlX4yIx&endpoint=%7B%22endpoint%22%3A%7B%22type%22%3A%22publish%22%2C%22country%22%3A%22de%22%2C%22language%22%3A%22de%22%2C%22content%22%3A%22onehub_pkw%22%2C%22envName%22%3A%22prod%22%2C%22testScenarioId%22%3Anull%2C%22isCloud%22%3Atrue%7D%2C%22signature%22%3A%22DDI5cVcqgXftyNeQrMuw%2Fbb9jUj%2BZrWtTRzYnLVkHzY%3D%22%7D&dataVersion=2A7706719FE556C689F695D1B263339A"

    response = requests.request("GET", url, headers=headers, data=payload)
    res_json = json.loads(response.text)
    return res_json

def processCars(request, all_dealers):
    for car in request["cars"]:
        dealer_key = car["dealer"]["key"]
        if dealer_key not in all_dealers:
            all_dealers[dealer_key] = {
                "dealer": car["dealer"],
                "cars": []
            }
        all_dealers[dealer_key]["cars"].append(car)

def saveDealerCars(all_dealers):
    for dealer_key, dealer_data in all_dealers.items():
        file_name = f"cars/{dealer_key}.json"
        with open(file_name, 'w') as f:
            json.dump(dealer_data, f, indent=4, sort_keys=True)

# Initial request to get the total number of pages
initial_request = downloadCars(1)
all_dealers = {}
processCars(initial_request, all_dealers)
page_max = initial_request["meta"]["pageMax"]

# Use ThreadPoolExecutor to download pages concurrently
with ThreadPoolExecutor(max_workers=128) as executor:
    futures = [executor.submit(downloadCars, i) for i in range(2, page_max + 1)]

    for future in as_completed(futures):
        try:
            request = future.result()
            processCars(request, all_dealers)
        except Exception as e:
            print(f"Fehler bei der Verarbeitung der Seite: {e}")

# Save all dealers' cars to separate JSON files
saveDealerCars(all_dealers)

dealers = []
for dealer in all_dealers:
    dealers.append(dealer["dealer"])

with open("dealers.json", 'w') as f:
    json.dump(dealers, f, indent=4, sort_keys=True)

print(f"{len(all_dealers)} Autohändler gefunden")
print(f"{sum(len(dealer['cars']) for dealer in all_dealers.values())} Autos gefunden")