from api_service import ApiService

class ProcessProducts:
    url = "https://mobileapi.jumbo.com/v16/search"
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0',
                    'charset' : 'utf-8'}
    items_per_query = 30
    
    def __init__(self) -> None:
        self.api_service = ApiService()


    async def get_total_amount_of_products(self, session):
        params={"offset" : 0, "limit" : 1}
        response = await self.api_service.fetch_json(session, self.url, self.headers, params)

        return response['products']['total']

    async def get_products(self, session, offset):

        # Iterate at least one time (start_index == 0) and continue till there are no next pages left.
        try:
            params={"offset" : offset, "limit" : self.items_per_query}
            print ('Url', self.url, 'Params', params)
            response = await self.api_service.fetch_json(session, self.url, self.headers, params)

        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success! Offset', offset)

        return response