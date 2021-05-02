from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import json
import time
import boto3
import os


def store_response(event, context):

    lambdaClient = boto3.client('lambda')

    print(event)
    start_index = 0
    next_page_query = None
    folder_name = time.strftime("%Y%m%d-%H%M%S")

    categories = {

        "herenschoenen": {"category_code": "catalog01_80", "sub_category_code": "catalog01_80_1040"},
        "herenkleding": {"category_code": "catalog01_80", "sub_category_code": "catalog01_80_890"},
        "herenaccessoires": {"category_code": "catalog01_80", "sub_category_code": "catalog01_80_980"},
        "herenverzorging": {"category_code": "catalog01_80", "sub_category_code": "catalog01_80_800"},

        "damesschoenen": {"category_code": "catalog01_60", "sub_category_code": "catalog01_60_640"},
        "dameskleding": {"category_code": "catalog01_60", "sub_category_code": "catalog01_60_880"},
        "damestassen": {"category_code": "catalog01_60", "sub_category_code": "catalog01_60_660"},
        "damesaccessoires": {"category_code": "catalog01_60", "sub_category_code": "catalog01_60_1110"},
        "damescosmetica": {"category_code": "catalog01_60", "sub_category_code": "catalog01_60_40"},
    }

    dml_date = time.strftime("%Y%m%d-%H%M%S")
    for category in categories:
        print('Invoke Lambda for',category, categories[category]['category_code'], categories[category]['sub_category_code'])

        payload = { 
            "dml_date" : dml_date,
            "category" : category, 
            "category_code" : categories[category]['category_code'], 
            "sub_category_code" : categories[category]['sub_category_code']
        }

        lambdaClient.invoke(
            FunctionName="arn:aws:lambda:eu-central-1:390567366752:function:webshop-api-scraper-dev-storeBijenkorfProductResponse",
            InvocationType="Event",
            Payload=json.dumps(payload),
        )

    response = {
        "statusCode": 200,
        "body": "okidoki"
    }

    return response


if __name__ == "__main__":
    store_response('', '')
