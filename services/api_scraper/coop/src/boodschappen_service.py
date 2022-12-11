
from services.api_scraper.python.api.api_service import ApiService


BASE_URL = "https://api.coop.nl/INTERSHOP/rest/WFS/COOP-COOPBase-Site/-;"
PRODUCT_ATTRIBUTES = "sku,salePrice,listPrice,availability,manufacturer,image,minOrderQuantity,inStock,promotions,packingUnit,mastered,productMaster,productMasterSKU,roundedAverageRating,longtail,sticker,maxXLabel,Inhoud"

class BoodschappenService :    

    def __init__(self):
        self.api_service = ApiService()

    def get_categories(self, category = "cur=EUR/categories") :

        category_url = BASE_URL + category
        raw_resonse = self.api_service.do_get_request(url=category_url)

        return raw_resonse.json()

    def get_products(self, offset = 0, limit = 50, with_attributes = True ) :

        category_url = BASE_URL + "cur=EUR/products"   

        params =  { "amount": limit, "offset" : offset}

        if  with_attributes:
            params["attrs"] = PRODUCT_ATTRIBUTES
            
        raw_resonse = self.api_service.do_get_request(url=category_url, params=params)

        return raw_resonse.json()

