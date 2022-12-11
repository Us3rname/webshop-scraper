import time
import requests
from requests.exceptions import HTTPError
from services.api_scraper.python.storage import local_storage
import logging

def store_response(event, context):

    localStorageService = local_storage.LocalStorageService()

    # Mechanism to stop querying when all products are loaded.
    offset = 1
    total_items = 10000

    # Likelyhood of that 84 items will be loaded within the 60 sec cap of the lambda function.
    items_per_query = 1

    # This date will be used for the folder on the S3 bucket
    folder_name = time.strftime("%Y%m%d-%H%M%S") #event['dml_date']
    product_categorie_ids = [1,2,7,8,9,10,11,12,13,14,15,16,18,19,20,21,22,23,24,25,26,27,28,29,30,31,33,34,35,36,37,38,39,40,
    41,42,43,44,46,48,51,53,58,62,63,64,66,68,69,73,74,75,76,77,78,79,80,81,82,83,91,92,93,94,95,96,97,98,99,100,101,102,103,
    104,105,106,118,119,120,121,128,129,130,131,132,133,135,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,162,
    163,164,165,166,169,172,174,175,176,177,178,179,180,181,182, 183,185,186,187,188,189,191,193,195,196,197,198,199,200,201,
    204,205,206,207,208,209,210,211,212,213,214, 215,216,217,218,219,223,228,247,248,249,250,251,252,253,254,255,256,257,258,
    259,260,262,265,266,279,293, 294,295,296,297,298,299,303,305,307,311,321,323,325,326,327,328,329,330,331,332,333,334,335,
    361,362,363, 364,365,366,367,368,369,371,372,373,374,375,376,378,379,380,381,382,383,385,386,387,388,389,390,392,393,394,
    395,396, 397,398,399,401,402,403,404,405,406,407,408,409,410,411,412,413,417,418,419,420,422,423,424,425,426,427,428,429,
    430, 433,434,435,436,448,449,450,451,452,453,454,456,457,458,459,460,462,463,464,465,466,467,468,469,470,471,472,473,476,
    481,488,489,490,492,493,498,499,505,506,507,508,509,511,514,515,516,517,518,519,520,521,522,523,524,525,526,527,528,529,
    530,531,542,560,563,564,611,612,613,620,624,645,646,647,655,660,666,667,668,670,674,679,680,681,682,683,684,685,686,687,
    688,689,690,691,692,693,694,695,696,697,698,699,700,701,702,703,704,707,708,709,710,711,712,714,715,716,717,718,719,720,
    721,722,723,725,727,728,729,730,732,733,735,736,737,738,739,740,741,742,743,744,745,746,747,748,749,750,751,752,753,754,
    755,756,757,759,760,761,764,765,768,769,772,773,774,775,776,777,779,780,781,783,784,785,786,787,788,789,790,791,793,794,
    795,798,799,800,802,803,804,805,807,809,810,811,812,813,814,815,816,817,818,819,820,822,823,824,825,826,827,829,830,831,
    832,833,834,836,837,838,840,842,843,844,845,846,847,848,849,850,851,852,853,855,858,860,861,862,864,865,866,867,868,869,
    870,871,872,873,875,876,877,878,879,880,881,882,883,884,885,886,887,888,889,890,891,892,893,894,896,897,898,899,900,901,
    902,903,904,905,906,907,908,909,910,911,912,914,915,916,917,918,919,920,921,922,923,924,925,926,928,929,930,931,932,933,
    934,935,936,937,938,939,940,941,942,943,944,945,946,947,948,949,950,951,952,954,955,956,957,959,960,961,967,968,969,970,
    971,972,973,974,975,976,977,978,979,980,981,982,983,984,985,986,987,988,989,991,994,1003,1004,1005,1006,1007,1008,1009,
    1012,1013,1014,1015,1016,1018,1019,1020,1025,1026,1027,1028,1029,1030,1032,1033]

    base_url = "https://api.dirk.nl/v1/assortmentcache/group/66/"

    # Iterate at least one time (start_index == 0) and continue till there are no next pages left.
    for i in product_categorie_ids:

        try:
            
            url = base_url + str(i)
            response = requests.get(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0',
                'charset' : 'utf-8'},
                params={"api_key" : '6d3a42a3-6d93-4f98-838d-bcc0ab2307fd'}
            )

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            logging.info(err)
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            # print('Success!', offset)
            
            # # Prepare & execute url
            print('Page:', offset , 'Producten:', len(response.json()),
            'Categorie:', response.json()[0]['WebSubGroups'][0]['WebGroup']['WebDepartment']['Description'],
            'Subcategorie:', response.json()[0]['WebSubGroups'][0]['WebGroup']['Description'],
            'Filter:', response.json()[0]['WebSubGroups'][0]['Description']
            )

            # # Calculate how many 'pages' there are, because there is no official pagination. 
            total_items = len(response.json())

            fileLocation =  'dirk/products/{}/response - {} - {} - {} - {} - {} - {}.json'.format(
                folder_name, 
                response.json()[0]['WebSubGroups'][0]['WebGroup']['WebDepartment']['Description'],
                response.json()[0]['WebSubGroups'][0]['WebGroup']['Description'],
                response.json()[0]['WebSubGroups'][0]['Description'],
                time.strftime("%Y%m%d-%H%M%S"), 
                offset, 
                total_items
            )

            localStorageService.upload_json_gz(
                'c:/Users/kompier/Documents/Personal/Programming/webshop-scraper/services/api_scraper/dirk/data/', 
                fileLocation, 
                response.text
            )

        offset += items_per_query

    response = {
        "statusCode": 200,
        "body": "okidoki"
    }

    return response

if __name__ == "__main__":    
    store_response({'dml_date' : '01-01-1997'}, '')