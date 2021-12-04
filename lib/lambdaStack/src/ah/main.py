import asyncio
import aiohttp
import os
from process_products import ProcessProducts
from s3_service import S3Service
import time
from datetime import datetime
import json

def handler(event, context):

    ahProductProcessor = ProcessProducts()
    categories = ahProductProcessor.get_categories()
    file_paths = []

    for category in categories:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(ahProductProcessor, category, file_paths))

    result = []
    for file in file_paths:
        with open(file, "rb") as infile:
            result.append(json.load(infile))

    store_file(result)

async def main(ahProductProcessor, category, file_paths):  

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=10)) as session:
        totalPages = await ahProductProcessor.get_total_amount_of_products(session, category)    

    print("Number of products found:",totalPages)    

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=10)) as session:
        
        coroutines = []
        page = 0
        while page <= totalPages:        
            coroutines.append(ahProductProcessor.get_products_per_category(session, category, page))  
            page += 1

        results = await asyncio.gather(*coroutines, return_exceptions=True)

    err = None
    for result, coro in zip(results, coroutines):
        if isinstance(result, Exception):
            err = result
            print(f"{coro.__name__} failed:")
            traceback.print_exception(type(err), err, err.__traceback__)

    if err:
        raise RuntimeError("One or more scripts failed.")

    file_paths.append(ahProductProcessor.write_response_to_tmp_file(results, category))

def store_file(results): 
    bucket_name = os.environ['bucket_name']
    # bucket_name = 'develop-webshop-scraper-landingzone'

    s3Service = S3Service()
    file_path = 'ah/products' + s3Service.getPartitionedFilePath(datetime.today())
    file_name = 'response - ' + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + '.json'

    s3Service.saveJsonGZFile(results, bucket_name, file_path + file_name)


if __name__ == "__main__":    
    handler(None, None) 