import time
import requests
from requests.exceptions import HTTPError
from services.api_scraper.python.storage import local_storage
import logging
from picnic_api import PicnicAPI
import json

def store_response(event, context):

    localStorageService = local_storage.LocalStorageService()

    try:
        picnic_api = PicnicAPI()
        # picnic_api.login("patrickkompier@gmail.com", "16PicNic.nl")
        categories = picnic_api.get_categories(3)
    except Exception as err:
        logging.info(err)
        print(f'Other error occurred: {err}')  # Python 3.6

    # This date will be used for the folder on the S3 bucket
    folder_name = time.strftime("%Y%m%d-%H%M%S") #event['dml_date']

    for category in categories:        

        print(category['name'])

        fileLocation =  'picnic/products/{}/response - {} - {} - {} - {}.json'.format(
            folder_name, 
            category['name'],
            time.strftime("%Y%m%d-%H%M%S"), 
            1, 
            len(category['items'])
        )

        localStorageService.upload_json_gz(
            'c:/Users/kompier/Documents/Personal/Programming/webshop-scraper/services/api_scraper/picnic/data/', 
            fileLocation, 
            json.dumps(category)
        )        

    response = {
        "statusCode": 200,
        "body": "okidoki"
    }

    return response

if __name__ == "__main__":    

    # picnic_api = PicnicAPI()
    # picnic_api.login("patrickkompier@gmail.com", "16PicNic.nl")
    # categories = picnic_api.get_categories(3)
    # print(categories)

    # for category in categories:
    #     for item in category['items']:
    #         # print('Categorie:', category['name'], 'Subcategorie:', item['name'], 'Link:', category['links'][0]['href'] )

    # print(len(picnic_api.get_sublist(list_id="21724", sublist_id="21747")))
    # print(picnic_api.get_sublist(list_id="21724", sublist_id="21747"))


    print(store_response({'dml_date' : '01-01-1997'}, ''))