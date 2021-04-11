from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import json
import time
import boto3    
import os
import requests

def store_response(event, context):

    s3 = boto3.resource('s3')
    bucket = os.environ['s3ResponseBucketName']
    key = event['Records'][0]['messageAttributes']['ProductS3Location']['stringValue']
    folder_name = event['Records'][0]['messageAttributes']['FolderName']['stringValue']

    obj = s3.Object(bucket, key)    
    file_content = obj.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    
    # Debug purpose
    # content_object = s3.Object('dev-webshop-scraper-infra-webshopresponsefb858fde-g7l88uy1c7m0',
    #  '20210131-173709/products/response - 20210131-173709 - 0 - 50.json')
    # file_content = content_object.get()['Body'].read().decode('utf-8')

    # result = json.loads(file_content)
    products = json_content['productListing']['navigation']['products']
    

    for product in products:
        # Build up the url
        base_url_product_detail = "https://ceres-catalog.debijenkorf.nl/catalog/product/show?cached=false&locale=nl_NL&api-version=2.38"
        url = base_url_product_detail + \
            "&productCode={}&productVariantCode={}".format(product['code'], product['currentVariantProduct']['code'])
        response = requests.get(url)
        response_json = response.json()

        s3object = s3.Object(
            os.environ['s3ResponseBucketName']
            # 'dev-webshop-scraper-infra-webshopresponsefb858fde-g7l88uy1c7m0'
            , 'product_details/{}/response - {} - {} - {}.json'.format(folder_name,time.strftime("%Y%m%d-%H%M%S"), product['code'], product['currentVariantProduct']['code']))

        s3object.put(
            Body=(bytes(json.dumps(response_json).encode('UTF-8')))
        )
    
    return ""