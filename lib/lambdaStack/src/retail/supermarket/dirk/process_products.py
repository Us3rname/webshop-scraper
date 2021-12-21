from api_service import ApiService
import aiohttp

class ProcessProducts : 
    url = "https://api.dirk.nl/"
    api_key = "6d3a42a3-6d93-4f98-838d-bcc0ab2307fd"
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0',
        'charset' : 'utf-8'
    }
    items_per_query = 50
    
    def __init__(self) -> None:
        self.api_service = ApiService()

    async def get_categories(self):

        url = self.url + 'v1/departments'
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=10)) as session:
            params={"api_key" : self.api_key}
            response = await self.api_service.fetch_json(session, url, self.headers, params)

        return self._get_category_ids_from_response(response)

    def _get_category_ids_from_response(self, response):
        category_ids = []
        for webDepartment in response:
            for webGroup in webDepartment['WebGroups']:
                for webSubGroup in webGroup['WebSubGroups']:
                    category_ids.append(webSubGroup['WebSubGroupID'])
        
        return category_ids

    async def get_products_per_category(self, session,category):
        url = self.url + 'v1/assortmentcache/group/66/' + str(category)
        try:
            params={"api_key" : self.api_key}
            return await self.api_service.fetch_json(session, url, self.headers, params)
            
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6