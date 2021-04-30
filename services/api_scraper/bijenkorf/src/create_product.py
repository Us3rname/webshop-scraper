import json
import os
import boto3
import botocore
import json
from pathlib import Path
from decimal import Decimal

s3 = boto3.resource('s3')

def hello(event, context):

    dynamodb = None
    if not dynamodb:        
        dynamodb = boto3.resource('dynamodb'
        , endpoint_url='http://localhost:8000' # For local development
        )

    table_name = 'dev-scraper-webshop-infra-webscraper-product9D4190BC-1JC7C9GEKU7M8'

    # table = dynamodb.create_table(
    #     TableName=table_name,
    #     KeySchema=[
    #         {
    #             'AttributeName': 'productId',
    #             'KeyType': 'HASH'  # Partition key
    #         },
    #         {
    #             'AttributeName': 'productType',
    #             'KeyType': 'RANGE'  # Sort key
    #         }
    #     ],
    #     AttributeDefinitions=[
    #         {
    #             'AttributeName': 'productId',
    #             'AttributeType': 'S'
    #         },
    #         {
    #             'AttributeName': 'productType',
    #             'AttributeType': 'S'
    #         },

    #     ],
    #     ProvisionedThroughput={
    #         'ReadCapacityUnits': 10,
    #         'WriteCapacityUnits': 10
    #     }
    # )

    
    # table_name = os.environ['tableName']
    table = dynamodb.Table('Product')
    # table.delete()

    # bucket = event['Records'][0]['s3']['bucket']['name']
    # print('## BUCKET')
    # print(bucket)

    # key = event['Records'][0]['s3']['object']['key']
    # print('## KEY')
    # print(event)

    # obj = s3.get_object(Bucket=bucket, Key=key)    
    parsed_json = json.loads(open(str(Path(os.path.dirname(__file__)).parents[0]) + "/src/mock/product_details/response - 20210417-185941 - 3672050001 - 367205000111430.json", "r").read())
    product = parsed_json['data']['product']
    currentVariantProduct = product['currentVariantProduct']

     # Some shoes / products don't have a category
    try:
        category = parsed_json['data']['navigationContext']['breadcrumbs'][2]['name']
    except IndexError:
        category = ''

    shoe = Shoe()
    get_product_attributes(parsed_json['data']['product']['groupedAttributes'], shoe)

    item = {
            "productId": '1-' + product['code'] + '-' + currentVariantProduct['code'], 
            "brand": product['brand']['name'],
            "name": product['name'],
            "product_code": product['code'],
            "product_variant_code": currentVariantProduct['code'],
            "productType": parsed_json['data']['navigationContext']['breadcrumbs'][1]['name'],
            "color": currentVariantProduct['color'],
            "webshop": "bijenkorf",
            "product_url": currentVariantProduct['url'],
            "category": category,
            "collection": parsed_json['data']['navigationContext']['breadcrumbs'][0]['name'],
            "price": Decimal(currentVariantProduct['sellingPrice']['value']),
            "materiaal_voering": shoe.materiaal_voering,
            "materiaal_bovenwerk": shoe.materiaal_bovenwerk,
            "materiaal_onderwerk": shoe.materiaal_onderwerk,
            "vorm_sluiting": shoe.vorm_sluiting,
            "vorm_neus": shoe.vorm_neus,
        }

    print(item)

    response = table.put_item(Item=item)  
    return response

def get_product_attributes(grouped_attributes, shoe):

    attributes = {}
    for attribute in grouped_attributes:

        if attribute['id'] == 'composition':
            for composition in attribute['attributes']:
                attributes[composition['label']] = composition['value']
                # print(composition['label'], composition['value'])
        elif attribute['id'] == 'specifications':
            for specification in attribute['attributes']:
                attributes[specification['label']] = specification['value']
                # print(specification['label'], specification['value'])
        # else:
            # print(attribute)

    shoe.dikte_zool = '' if 'Dikte zool' not in attributes else attributes['Dikte zool']
    shoe.materiaal_voering = '' if 'Materiaal voering' not in attributes else attributes[
        'Materiaal voering']
    shoe.materiaal_bovenwerk = '' if 'Materiaal bovenwerk' not in attributes else attributes[
        'Materiaal bovenwerk']
    shoe.materiaal_onderwerk = '' if 'Materiaal onderwerk' not in attributes else attributes[
        'Materiaal onderwerk']
    shoe.vorm_sluiting = '' if 'Vorm sluiting' not in attributes else attributes[
        'Vorm sluiting']
    shoe.vorm_neus = '' if 'Vorm neus' not in attributes else attributes['Vorm neus']
    shoe.schacht_hoogte = '' if 'Schachthoogte' not in attributes else attributes[
        'Schachthoogte']
    shoe.uitneembaar_voetbed = '' if 'Uitneembaar voetbed' not in attributes else attributes[
        'Uitneembaar voetbed']
  
    
class Shoe():
    productId = ""
    brand = ""
    name = ""
    product_code = ""
    product_variant_code = ""
    color = ""
    webshop = ""
    product_url = ""
    dikte_zool = ""
    materiaal_voering = ""
    materiaal_bovenwerk = ""
    materiaal_onderwerk = ""
    vorm_sluiting = ""
    vorm_neus = ""
    schacht_hoogte = ""
    category = ""
    uitneembaar_voetbed = ""
    collection = ""
    product_type = ""
    price = ""

hello(None, None)    