
import asyncio
import aiohttp
from datetime import datetime
from s3_service import S3Service
import os
from process_products import ProcessProducts

def handler(event, context):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

async def main():

    dirkProductProcessor = ProcessProducts()
    category_ids = await dirkProductProcessor.get_categories()

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=10)) as session:
        
        coroutines = []
        for category_id in category_ids:      
            coroutines.append(dirkProductProcessor.get_products_per_category(session,category=category_id ))  

        results = await asyncio.gather(*coroutines, return_exceptions=True)

        store_file(results)

def store_file(results): 
    bucket_name = os.environ['bucket_name']
    # bucket_name = 'develop-webshop-scraper-landingzone'

    s3Service = S3Service()
    file_path = 'dirk/products' + s3Service.getPartitionedFilePath(datetime.today())
    file_name = 'response - ' + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + '.json'

    s3Service.saveJsonGZFile(results, bucket_name, file_path + file_name)

if __name__ == "__main__":    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    