from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import json
import time
import boto3    
import os
import requests



def store_response(event, context):

    s3 = boto3.resource('s3')

    bucket = event['Records'][0]['s3']['bucket']['name']
    print('## BUCKET')
    print(bucket)

    key = event['Records'][0]['s3']['object']['key']
    print('## KEY')
    print(key)

    obj = s3.get_object(Bucket=bucket, Key=key)    
    file_content = obj['Body'].read().decode('utf-8')

    return 

    # Debug purpose
    # content_object = s3.Object('dev-webshop-scraper-infra-webshopresponsefb858fde-g7l88uy1c7m0',
    #  '20210131-173709/products/response - 20210131-173709 - 0 - 50.json')
    # file_content = content_object.get()['Body'].read().decode('utf-8')

    result = json.loads(file_content)
    products = result['productListing']['navigation']['products']
    folder_name = time.strftime("%Y%m%d-%H%M%S")

    for product in products:
        # Build up the url
        base_url_product_detail = "https://ceres-catalog.debijenkorf.nl/catalog/product/show?cached=false&locale=nl_NL&api-version=2.38"
        url = base_url_product_detail + \
            "&productCode={}&productVariantCode={}".format(
                product['code'], product['currentVariantProduct']['code'])
        response = requests.get(url)
        response_json = response.json()

        s3object = s3.Object(
            os.environ['s3ResponseBucketName']
            # 'dev-webshop-scraper-infra-webshopresponsefb858fde-g7l88uy1c7m0'
            , '{}/product_details/response - {} - {} - {}.json'.format(folder_name,time.strftime("%Y%m%d-%H%M%S"), product['code'], product['currentVariantProduct']['code']))

        s3object.put(
            Body=(bytes(json.dumps(result).encode('UTF-8')))
        )
    
    return ""






















    start_index = 0
    
    next_page_query = None
    folder_name = time.strftime("%Y%m%d-%H%M%S")
    while next_page_query is not None or start_index == 0:
        
        # Prepare & execute query
        query_addition = "fh_location=//catalog01/nl_NL/categories<{catalog01_80}/categories<{catalog01_80_1040}" + "&fh_start_index={}&country=NL&chl=1&language=nl&fh_view_size={}".format(start_index, 50)
        qpl = gql(query % ('"' + query_addition + '"'))
        result = client.execute(qpl)
        
        # Count the amount of products
        products = result['productListing']['navigation']['products']
        next_page_query = None
        if result['productListing']['navigation']['pagination']['nextPage'] is not None:
            next_page_query = result['productListing']['navigation']['pagination']['nextPage']['query']

        s3object = s3.Object(os.environ['s3ResponseBucketName'], '{}/products/response - {} - {} - {}.json'.format(folder_name,time.strftime("%Y%m%d-%H%M%S"), start_index, start_index + len(products)))

        s3object.put(
            Body=(bytes(json.dumps(result).encode('UTF-8')))
        )

        start_index += 50

    response = {
        "statusCode": 200,
        "body": "okidoki"
    }

    return response

if __name__ == "__main__":
    store_response('', '')