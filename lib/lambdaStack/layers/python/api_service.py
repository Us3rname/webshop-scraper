class ApiService:

    async def fetch_response(self, session, url, headers, params):
        async with session.get(url, headers=headers, params=params) as response:
            return await response


    async def fetch_json(self, session, url, headers, params):
        async with session.get(url, headers=headers, params=params) as response:
            return await response.json()

    async def fetch_text(self, session, url):
        async with session.get(url, ) as response:
            return await response.text()