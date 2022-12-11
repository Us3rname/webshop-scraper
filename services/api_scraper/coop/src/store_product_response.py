import time
from services.api_scraper.python.storage import local_storage
from boodschappen_service import BoodschappenService
import json

def store_response(event, context):

    localStorageService = local_storage.LocalStorageService()

    boodschappen_service = BoodschappenService()
    initial_request = boodschappen_service.get_products(limit=1, with_attributes=False)

    # Mechanism to stop querying when all products are loaded.
    offset = 0
    total_items = initial_request['total']

    # Likelyhood of that 84 items will be loaded within the 60 sec cap of the lambda function.
    items_per_query = 50

    # This date will be used for the folder on the S3 bucket
    folder_name = time.strftime("%Y%m%d-%H%M%S") #event['dml_date']
    
    while offset < total_items:

        response = boodschappen_service.get_products(offset=offset, limit=items_per_query)
        products = response['elements']

        fileLocation =  'coop/products/{}/response - {} - {} - {} - {}.json'.format(
            folder_name, 
            'groceries',
            time.strftime("%Y%m%d-%H%M%S"), 
            offset, 
            offset + len(products)
        )

        localStorageService.upload_json_gz(
            'c:/Users/kompier/Documents/Personal/Programming/webshop-scraper/services/api_scraper/coop/data/', 
            fileLocation, 
            json.dumps(products)
        )

        offset += len(products)


    response = {
        "statusCode": 200,
        "body": "okidoki"
    }

    return response

if __name__ == "__main__":    
    store_response({'dml_date' : '01-01-1997'}, '')