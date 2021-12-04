
from api_service import ApiService

BASE_URL = "https://api.coop.nl/INTERSHOP/rest/WFS/COOP-COOPBase-Site/-;"
PRODUCT_ATTRIBUTES = "sku,salePrice,listPrice,availability,manufacturer,image,minOrderQuantity,inStock,promotions,packingUnit,mastered,productMaster,productMasterSKU,roundedAverageRating,longtail,sticker,maxXLabel,Inhoud"

class ProcessProducts :    

    def __init__(self):
        self.api_service = ApiService()

    def get_categories(self,session, category = "cur=EUR/categories") :

        category_url = BASE_URL + category
        return self.api_service.fetch_json(session, category_url, None,None )

    async def get_products(self,session, offset = 0, limit = 50, with_attributes = True ) :

        category_url = BASE_URL + "cur=EUR/products"   

        params =  { "amount": limit, "offset" : offset}

        if  with_attributes:
            params["attrs"] = PRODUCT_ATTRIBUTES
            
        return await self.api_service.fetch_json(session, category_url, None, params)