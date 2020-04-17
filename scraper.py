# coding: utf-8
import scrapy
import csv
from scrapy import signals
from scrapy.crawler import CrawlerProcess

class HouseSpider(scrapy.Spider):
	name = "house_spider"
	start_urls = ['https://batdongsan.com.vn/cho-thue-nha-rieng-tp-hcm']
	pc = 1
	def parse(self, response):
		HouseSpider.pc += 1
		for house in response.css('.vip0') + response.css('.vip1') + response.css('.vip2') + response.css('.vip3') + response.css('.vip4') + response.css('.vip5'):
			TITLE_SELECTOR = 'a ::text'
			PRICE_SELECTOR = '.product-price ::text'
			AREA_SELECTOR = '.product-area ::text'
			DISTRICT_SELECTOR = '.product-city-dist ::text'
			TIME_SELECTOR = '.uptime ::text'
			dic = {
				'title': house.css(TITLE_SELECTOR).extract_first(),
				'price' : house.css(PRICE_SELECTOR).extract_first(),
				'area' : house.css(AREA_SELECTOR).extract_first(),
				'district' : house.css(DISTRICT_SELECTOR).extract_first(),
				'time' : house.css(TIME_SELECTOR).extract_first()
			}
			yield dic
		print(response.url)
		if response.url != 'https://batdongsan.com.vn/cho-thue-nha-rieng-tp-hcm/p300':
			yield scrapy.Request('https://batdongsan.com.vn/cho-thue-nha-rieng-tp-hcm/p' + str(HouseSpider.pc),callback=self.parse)


process = CrawlerProcess(settings={
	'LOG_ENABLED' : 'False'
})

items = []
def add_item(item):
	items.append(item)

crawler = process.create_crawler(HouseSpider)
crawler.signals.connect(add_item, signals.item_passed)
process.crawl(crawler)
process.start()


for item in items:
	item['title'] = item['title'].replace('CHO THUÊ','').replace('CHÍNH CHỦ','').strip()
	item['price'] = item['price'].replace('triệu/tháng','').strip()
	item['district'] = item['district'].replace('Hồ Chí Minh','').strip().strip(',').strip()
	item['area'] = item['area'].replace('m²','').replace('Không xác định','N/A').strip()


keys = items[0].keys()
with open('houses.csv', 'w',encoding='utf-8-sig',newline='') as output_file:
	dict_writer = csv.DictWriter(output_file, keys)
	dict_writer.writeheader()
	dict_writer.writerows(items)

# for item in items:
# 	print(item['title'])
# 	print(item['price'])
# 	print(item['area'])
# 	print(item['district'])
# 	print(item['time'])
# 	print()