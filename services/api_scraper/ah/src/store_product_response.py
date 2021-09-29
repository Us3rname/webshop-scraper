import time
import requests
from requests.exceptions import HTTPError
from services.api_scraper.python.storage import local_storage
import json

def store_response(event, context):

    localStorageService = local_storage.LocalStorageService()

    
    
    offset = 0

    # Likelyhood of that 84 items will be loaded within the 60 sec cap of the lambda function.
    items_per_query = 36

    # This date will be used for the folder on the S3 bucket
    folder_name = time.strftime("%Y%m%d-%H%M%S") #event['dml_date']
    
    print ('prepare and execute')
    base_url = "https://www.ah.nl/zoeken/api/products/search"

    categories = [
        'aardappel-groente-fruit', 'salades-pizza-maaltijden', 'vlees-kip-vis-vega', 'kaas-vleeswaren-tapas', 'zuivel-plantaardig-en-eieren',
        'bakkerij-en-banket', 'ontbijtgranen-broodbeleg-tussendoor', 'frisdrank-sappen-koffie-thee', 'wijn-en-bubbels', 'bier-en-aperitieven',
        'pasta-rijst-en-wereldkeuken', 'soepen-sauzen-kruiden-olie', 'snoep-koek-chips-en-chocolade', 'diepvries', 'baby-verzorging-en-hygiene',
        'bewuste-voeding', 'huishouden-huisdier', 'koken-tafelen-vrije-tijd'
    ]
    # Iterate at least one time (start_index == 0) and continue till there are no next pages left.
    for category in categories:
        
        # Mechanism to stop querying when all products are loaded.
        page = 0
        total_pages = 1
        while page <= total_pages:
            print('offset', category)
            
            try:
                response = requests.get(
                    base_url, 
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0',
                        'charset' : 'utf-8'
                    },
                    params={"taxonomySlug" : category, "size" : items_per_query}
                )

                # If the response was successful, no Exception will be raised
                response.raise_for_status()
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')  # Python 3.6
                break
            except Exception as err:
                print(f'Other error occurred: {err}')  # Python 3.6
                break
            else:
                print('Success!')
                
                # Prepare & execute url
                products = response.json()['cards']

                # Calculate how many 'pages' there are, because there is no official pagination. 
                total_pages = response.json()['page']['totalPages']

                fileLocation =  'ah/products/{}/response - {} - {} - {} - {}.json'.format(
                    folder_name, 
                    category,
                    time.strftime("%Y%m%d-%H%M%S"), 
                    offset, 
                    offset + len(products)
                )

                localStorageService.upload_json_gz(
                    'c:/Users/kompier/Documents/Personal/Programming/webshop-scraper/services/api_scraper/ah/data/', 
                    fileLocation, 
                    json.dumps(products)
                )

                offset += items_per_query
                page += 1

    response = {
        "statusCode": 200,
        "body": "okidoki"
    }

    return response

if __name__ == "__main__":
    print ('test 123')
    store_response({'dml_date' : '01-01-1997'}, '')