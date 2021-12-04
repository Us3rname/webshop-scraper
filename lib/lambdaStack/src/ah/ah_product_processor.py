from api_service import ApiService
import json 

class AHProductProcessor:
    url = "https://www.ah.nl/zoeken/api/products/search"
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0','charset' : 'utf-8'}
    items_per_query = 50
    
    def __init__(self) -> None:
        self.api_service = ApiService()


    def get_categories(self):
        return [
        'aardappel-groente-fruit', 
        'salades-pizza-maaltijden', 
        'vlees-kip-vis-vega', 
        'kaas-vleeswaren-tapas', 'zuivel-plantaardig-en-eieren',
        'bakkerij-en-banket', 'ontbijtgranen-broodbeleg-tussendoor', 'frisdrank-sappen-koffie-thee', 'wijn-en-bubbels', 'bier-en-aperitieven',
        'pasta-rijst-en-wereldkeuken', 'soepen-sauzen-kruiden-olie', 'snoep-koek-chips-en-chocolade', 'diepvries', 'baby-verzorging-en-hygiene',
        'bewuste-voeding', 'huishouden-huisdier', 'koken-tafelen-vrije-tijd'
        ]

    async def get_total_amount_of_products(self, session, category):

        params={"taxonomySlug" : category, "size" : self.items_per_query}
        response = await self.api_service.fetch_json(session, self.url, self.headers, params)

        return response['page']['totalPages']

    async def get_products_per_category(self, session,category, page):
        
        try:
            print('Category', category, 'Page', page)
            params={"taxonomySlug" : category, "size" : self.items_per_query}
            response = await self.api_service.fetch_json(session, self.url, self.headers, params)
            
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6            

        return response['cards']

    def write_response_to_tmp_file(self, data, category) :
        file_name = '/tmp/' + category + '-response.json'
        with open(file_name, 'w') as outfile:
            json.dump(data, outfile)
    
        return file_name