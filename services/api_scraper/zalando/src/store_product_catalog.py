from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import json
import time
import boto3
import os


def store_response(event, context):

    lambdaClient = boto3.client('lambda')

    print(event)

    categories = {

        "herenschoenen": {"categories": "herenschoenen"},
        "herenkleding": {"categories": "herenkleding"},
        "herenaccessoires": {"categories": "heren-accessoires"},
        "herenverzorging": {"categories": "verzorging"},

        "damesschoenen": {"categories": "damesschoenen"},
        "dameskleding": {"categories": "dameskleding"},
        # Heet op de website 'Accessoires voor dames', but category is tassen-accessoires
        "damesaccessoires": {"categories": "tassen-accessoires"},
        "damescosmetica": {"categories": "beauty"},
    }

    dml_date = time.strftime("%Y%m%d-%H%M%S")
    for category in categories:
        print('Invoke Lambda for',category, categories[category]['category_code'], categories[category]['sub_category_code'])

        payload = { 
            "dml_date" : dml_date,
            "category" : category, 
            "category_code" : categories[category]['category_code']
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