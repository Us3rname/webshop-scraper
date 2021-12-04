import time

import asyncio
import aiohttp
import os
from s3_service import S3Service
from process_products import ProcessProducts
import time
from datetime import datetime

# from lib.lambdaStack.layers.python.s3_service import S3Service

def handler(event, context):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

async def main():  

    bucket_name = os.environ['bucket_name']

    jumboProcessProducts = ProcessProducts()

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=10)) as session:
        numberOfProducts = await jumboProcessProducts.get_total_amount_of_products(session)    

    print("Number of products found:",numberOfProducts)

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=10)) as session:
        
        coroutines = []
        offset = 0

        while offset <= (numberOfProducts / ProcessProducts.items_per_query):
            coroutines.append(jumboProcessProducts.get_products(session, offset))
            offset += ProcessProducts.items_per_query

        results = await asyncio.gather(*coroutines, return_exceptions=True)

    err = None
    for result, coro in zip(results, coroutines):
        if isinstance(result, Exception):
            err = result
            print(f"{coro.__name__} failed:")
            traceback.print_exception(type(err), err, err.__traceback__)

    if err:
        raise RuntimeError("One or more scripts failed.")

    s3Service = S3Service()
    file_path = 'jumbo/products' + s3Service.getPartitionedFilePath(datetime.today())
    file_name = 'response - ' + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + '.json'

    s3Service.saveJsonGZFile(results, bucket_name, file_path + file_name)    