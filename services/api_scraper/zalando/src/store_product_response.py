import json
import time
import boto3    
import os
import requests
# from s3_service import S3Service

def store_response(event, context):

    start_index = 0
    # s3Service = S3Service()
    s3 = boto3.client('s3')
    sqs = boto3.resource('sqs')

    # queue = sqs.get_queue_by_name(QueueName=os.environ['BijenkorfProductSpecificationSQSTopicName'])

    # Mechanism to stop querying when all products are loaded.
    current_page = 0
    page_count = 0

    # Likelyhood of that 84 items will be loaded within the 60 sec cap of the lambda function.
    items_per_query = 84

    # This date will be used for the folder on the S3 bucket
    folder_name = event['dml_date']

    # Iterate at least one time (start_index == 0) and continue till there are no next pages left.
    while current_page <= page_count:
        
        # Prepare & execute url
        url = "https://www.zalando.nl/api/catalog/articles?categories={}&limit={}&offset={}".format(event['category_code'], items_per_query, current_page * items_per_query )
        print(url)
        response = requests.get(url)

        articles = response.text['articles']
        page_count = response.text['pagination']['page_count']

        fileLocation =  'products/zalando/{}/response - {} - {} - {} - {}.json.gz'.format(
            folder_name, 
            event['category'],
            time.strftime("%Y%m%d-%H%M%S"), 
            current_page * items_per_query, 
            (current_page * items_per_query) + len(articles)
        )

        s3Service.upload_json_gz(s3, os.environ['s3ResponseBucketName'], fileLocation, response.text)

        
        current_page += 1

    response = {
        "statusCode": 200,
        "body": "okidoki"
    }

    return response

if __name__ == "__main__":
    store_response({"category": "damescosmetica", "category_code": "catalog01_60", "sub_category_code": "catalog01_60_40", "dml_date": "1900-01-01"}, '')