import json
import time
# import boto3    
import localstack_client.session as boto3
import os

def store_response(event, context):
    s3 = boto3.resource('s3')
    sqs = boto3.resource('sqs')

    response = sqs.create_queue(
        QueueName='dev-webshop-scraper-infra-webscraper-BijenkorfQueue0CAC392F-ALBMVIY0WXN9',
    )

    s3.create_bucket(Bucket='dev-webshop-scraper-infra-webshopresponsefb858fde-g7l88uy1c7m0')

    return response 

    queue = sqs.get_queue_by_name(QueueName="dev-webshop-scraper-infra-webscraper-BijenkorfQueue0CAC392F-ALBMVIY0WXN9")

    fileLocation =  'products/bijenkorf/{}/response - {} - {} - {}.json'.format(folder_name,time.strftime("%Y%m%d-%H%M%S"), start_index, start_index + len(products))
    s3object = s3.Object(os.environ['s3ResponseBucketName'], fileLocation)

    s3object.put(
        Body=(bytes(json.dumps(result).encode('UTF-8')))
    )

    response = queue.send_message(MessageBody="Producten {} t/m {}".format(start_index, start_index + len(products)), MessageAttributes = {
        'ProductS3Location': {
            'StringValue': fileLocation,
            'DataType': 'String'
        },
        'FolderName': {
            'StringValue': folder_name,
            'DataType': 'String'
        }
    })

    response = {
        "statusCode": 200,
        "body": "okidoki"
    }

    return response