import scrapy
from itemadapter import ItemAdapter
import json
import uuid

class VanassemSpider(scrapy.Spider):
    name = "assem"
    start_urls = [
        # All the product information can be found through this page. By the collection data field you know which collection / category it belongs (e.g Damesschoenen, Herenschoenen)
        'https://www.assem.nl/schoenen/',
        # 'https://www.assem.nl/schoenen/123/' # for debugging
    ]

    def parse(self, response):
        # For each product / item on the page proces the information.
        for product in response.css("li.product"):
            
            # Not all the information is stored on li.product level
            product_information = product.css("a.product_click_href div.product_click_detail div.product_information_block")

            item = {
                "productId": str(uuid.uuid4()),
                'brand': product.css('li[data-name]::attr(data-brand)').get(),
                "name": product.css('li[data-name]::attr(data-name)').get(),
                "product_code": product.css('li[data-name]::attr(data-productkey)').get(),
                'product_type': 'Schoenen',
                'color': product.css('li[data-name]::attr(data-color)').get(),
                'webshop': 'assem',
                'product_url': product.css('li[data-name]::attr(data-url)').get(),
                'category': product.css('li[data-name]::attr(data-category)').get(),
                'collection': product.css('li[data-name]::attr(data-collection)').get(),
                "price": product.css('li[data-name]::attr(data-price)').get(),
                # 'material': product.css('li[data-name]::attr(data-material)').get(),
                # 'type': product.css('li[data-name]::attr(data-type)').get(),
                # 'original_price': product_information.css("div.product_information_block_price::text").get(),
                'new_collection': product_information.css("div.extra_label_new_collection::text").get(),
                # 'sold_out': product_information.css("div.extra_label_sold_out::text").get(),
                'exclusive_online': product_information.css("div.extra_label_sold_out::text").get(),
                # 'sustainable': product_information.css("div.extra_label_sustainable::text").get(),
                'exclusive': product_information.css("div.extra_label_excl::text").get(),
                # 'perfect_fit': product_information.css("div.extra_label_pf::text").get(),            
            }
            
            # Scrape the product specifications
            items = scrapy.Request(product.css('li[data-name]::attr(data-url)').get(), callback=self.parse_product_details, 
                meta={ 'item': item}
            )

            yield items

        # While there's a next page keep on scraping. 
        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_product_details(self, response):
      
        item = response.meta['item']
        mapping = {
            "Hakhoogte" : 'dikte_zool', "Binnenvoering" : "materiaal_voering", "Materiaal" : "materiaal_bovenwerk", "Zool" : "materiaal_onderwerk",
            "Sluiting" : "vorm_sluiting", "Vorm neus" : "vorm_neus", "Uitneembaar voetbed" : "uitneembaar_voetbed"
        }

        for omschrijving_row in response.css("table.omschrijving_table tr"):
            
            omschrijving = omschrijving_row.css('td::text').get()
            waarde = omschrijving_row.css('td::text')[2].get()            
            key = omschrijving if omschrijving not in mapping else mapping[omschrijving]
            item[key] = waarde
       
        shoe_sizes = {}
        shoe_size_us_list = []
        for shoe_size_us in response.xpath('//ul[@id="us_selectable"]/li/text()'):
            shoe_size_us_list.append(shoe_size_us.get())

        shoe_size_eu_list = []
        for shoe_size_eu in response.xpath('//ul[@id="eu_selectable"]/li/text()'):
            shoe_size_eu_list.append(shoe_size_eu.get())    

        shoe_sizes["eu"] = shoe_size_eu_list
        shoe_sizes['us'] = shoe_size_us_list
        item['shoe_size'] = shoe_sizes
        
        return item