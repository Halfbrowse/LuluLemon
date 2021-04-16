import scrapy
import json
import re
import time


class LuluSpider(scrapy.Spider):
    name = 'lulu'
    allowed_domains = ['shop.lululemon.com', 'https://api.bazaarvoice.com']
    start_urls = [
        'https://shop.lululemon.com/api/c/woman?page=1',
        'https://shop.lululemon.com/api/c/men?page=1',
        'https://shop.lululemon.com/api/c/accessories?page=1']

    def parse(self, response):
        resps = json.loads(response.body)
        prods = resps.get("data").get("attributes").get(
            "main-content")[0].get("records")

        sizedict = {}
        for prod1 in prods:
            size = prod1.get("all-available-sizes")
            for i in size:
                sizedict.update({i: ''})

                for prod in prods:
                    name = prod.get("display-name")
                    price = prod.get("list-price")[0]
                    sku = prod.get("sku-style-order")[0].get("sku")
                    color = prod.get(
                        "sku-style-order")[0].get("color-name")
                    icon = prod.get("sku-sku-images")[0]
                    saleprice = prod.get("product-sale-price")
                    if saleprice == []:
                        saleprice = "N/A"
                    url = prod.get("pdp-url")
                    if url:
                        url = 'https://shop.lululemon.com' + url
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
            #  desc = resps.get("data").get("attributes").get(
            #      "secondary-content").get("contents")[0].get("navigation").get("properties").get("long-description")
            for size in sizedict.keys():
                yield {
                    'Brand': 'Lululemon',
                    'Name': name,
                    'Size': size,
                    'Price': price,
                    'Saleprice': saleprice,
                    'Icon': icon,
                    'Sku': sku,
                    'Product Url': url,
                    # 'Description': desc,
                    'Color': color,
                    'Time': current_time

                }

        nexturl = resps.get("links").get("next")
        if nexturl:
            yield scrapy.Request(f"https://shop.lululemon.com/api{nexturl}", callback=self.parse)
