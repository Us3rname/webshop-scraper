import time
import requests
from requests.exceptions import HTTPError
from services.api_scraper.python.storage import local_storage
import json

def store_response(event, context):

    localStorageService = local_storage.LocalStorageService()

    # Mechanism to stop querying when all products are loaded.
    offset = 0
    total_items = 0

    # Likelyhood of that 84 items will be loaded within the 60 sec cap of the lambda function.
    items_per_query = 30

    # This date will be used for the folder on the S3 bucket
    folder_name = time.strftime("%Y%m%d-%H%M%S") #event['dml_date']
    
    print ('prepare and execute')
    url = "https://mobileapi.jumbo.com/v16/search"

    # Iterate at least one time (start_index == 0) and continue till there are no next pages left.
    while offset <= total_items:

        print('offset', offset)

        try:
            response = requests.get(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0',
                'charset' : 'utf-8'},
                params={"offset" : offset, "limit" : items_per_query}
            )

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')
            
            # Prepare & execute url
            products = response.json()['products']['data']

            # Calculate how many 'pages' there are, because there is no official pagination. 
            total_items = response.json()['products']['total']

            fileLocation =  'jumbo/products/{}/response - {} - {} - {} - {}.json'.format(
                folder_name, 
                'groceries',
                time.strftime("%Y%m%d-%H%M%S"), 
                offset, 
                offset + len(products)
            )

            localStorageService.upload_json_gz(
                'c:/Users/kompier/Documents/Personal/Programming/webshop-scraper/services/api_scraper/jumbo/data/', 
                fileLocation, 
                json.dumps(response.json()['products'])
            )

            offset += items_per_query

    response = {
        "statusCode": 200,
        "body": "okidoki"
    }

    return response

if __name__ == "__main__":
    print ('test 123')
    store_response({'dml_date' : '01-01-1997'}, '')