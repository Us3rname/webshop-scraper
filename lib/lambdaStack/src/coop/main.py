import time
from process_products import ProcessProducts
import json
import aiohttp
import asyncio
from datetime import datetime
from s3_service import S3Service

def handler(event, context):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

async def main() :

    process_products = ProcessProducts()

    # Make an initial request to check how many products there are.
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=10)) as session:
        initial_request = await process_products.get_products(session, 0, limit=1, with_attributes=False)

    # Mechanism to stop querying when all products are loaded.
    offset = 0
    total_items = initial_request['total']

    print(total_items)

    # Likelyhood of that 84 items will be loaded within the 60 sec cap of the lambda function.
    items_per_query = 50

    # This date will be used for the folder on the S3 bucket
    folder_name = time #event['dml_date']
    coroutines = []

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=10)) as session:
        while offset < total_items:
            coroutines.append(process_products.get_products(session, offset, items_per_query))  
            offset += items_per_query

        results = await asyncio.gather(*coroutines, return_exceptions=True)
        store_file(results)

  
def store_file(results): 
    # bucket_name = os.environ['bucket_name']
    bucket_name = 'develop-webshop-scraper-landingzone'

    s3Service = S3Service()
    file_path = 'coop/products' + s3Service.getPartitionedFilePath(datetime.today())
    file_name = 'response - ' + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + '.json'

    s3Service.saveJsonGZFile(results, bucket_name, file_path + file_name)

if __name__ == "__main__":    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())