from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import json
import time
import boto3    
import os

def store_response(event, context):

    transport = AIOHTTPTransport(url="https://www.debijenkorf.nl/api/graphql")    
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = """
            query { productListing(query: %s, locale: "nl-NL") { 
            metaInformation {
                
            query
            title
            alternativeLanguages {
                
            locale
            url

            }

            }
            navigation {
                products {
                    
            brand {
                
            name

            }
            code
            colorCount
            currentVariantProduct {
                
            availability {
                
            available
            availableFuture
            stock

            }
            code
            color
            current
            images {
                
            position
            type
            url

            }
            overriddenPrices {
                
            currencyCode
            type
            value

            }
            sellingPrice {
                
            currencyCode
            type
            value

            }
            signings {
                
            discount {
                
            key
            text

            }
            merchandise {
                
            key
            text

            }

            }
            trackingMetadata
            size
            url

            }
            defaultVariantCode
            description
            designer
            displayName
            displayProperties {
                
            currentVariantSelected
            detailPageVariation

            }
            gift
            name
            subBrand {
                
            name

            }
            supplierModel
            sustainable
            trackingMetadata
            url
            variantProducts (limit:4, groupBy: COLOR) {
                
            availability {
                
            available
            availableFuture
            stock

            }
            code
            color
            current
            images {
                
            position
            type
            url

            }
            overriddenPrices {
                
            currencyCode
            type
            value

            }
            sellingPrice {
                
            currencyCode
            type
            value

            }
            signings {
                
            discount {
                
            key
            text

            }
            merchandise {
                
            key
            text

            }

            }
            size
            url

            }
            recommendationRanking

                }
                pagination {
                    
            currentPage {
                
            pageNumber
            query
            relativeUrl

            }
            nextPage {
                
            pageNumber
            query
            relativeUrl

            }
            previousPage {
                
            pageNumber
            query
            relativeUrl

            }
            totalItemCount
            viewSize

                }
            }
        } }
        """

    start_index = 0
    s3 = boto3.resource('s3')
    sqs = boto3.resource('sqs')

    queue = sqs.get_queue_by_name(QueueName="dev-webshop-scraper-infra-webscra-SaveBijenkorfProductSpecificatio-13J4BX35A2HOM")

    next_page_query = None
    items_per_query = 40

    # This date will be used for the folder on the S3 bucket
    folder_name = event['dml_date']

    # Iterate at least one time (start_index == 0) and continue till there are no next pages left.
    while next_page_query is not None or start_index == 0:
        
        # Prepare & execute query
        query_addition = "fh_location=//catalog01/nl_NL/categories<{{{}}}/categories<{{{}}}&fh_start_index={}&country=NL&chl=1&language=nl&fh_view_size={}".format(event['category_code'],event['sub_category_code'],start_index, items_per_query)
        print(query_addition)
        
        qpl = gql(query % ('"' + query_addition + '"'))
        result = client.execute(qpl)
        
        # Get all the products
        products = result['productListing']['navigation']['products']
        next_page_query = None
        if result['productListing']['navigation']['pagination']['nextPage'] is not None:
            next_page_query = result['productListing']['navigation']['pagination']['nextPage']['query']

        fileLocation =  'products/bijenkorf/{}/response - {} - {} - {} - {}.json'.format(
            folder_name, 
            event['category'],
            time.strftime("%Y%m%d-%H%M%S"), 
            start_index, 
            start_index + len(products)
        )

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

        start_index += items_per_query

    response = {
        "statusCode": 200,
        "body": "okidoki"
    }

    return response

if __name__ == "__main__":
    store_response('', '')