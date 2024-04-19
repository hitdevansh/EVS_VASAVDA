import scrapy
import re

class NgodataSpider(scrapy.Spider):
    name = "ngodata"
    allowed_domains = ["climatescape.org"]
    start_urls = [
        "https://climatescape.org/categories/atmosphere",
        "https://climatescape.org/categories/buildings-and-cities",
        "https://climatescape.org/categories/carbon",
        "https://climatescape.org/categories/climate-risk",
        "https://climatescape.org/categories/consumer-goods",
        "https://climatescape.org/categories/energy",
        "https://climatescape.org/categories/food-and-agriculture",
        "https://climatescape.org/categories/health",
        "https://climatescape.org/categories/industrial",
        "https://climatescape.org/categories/transportation",
        "https://climatescape.org/categories/waste",
        "https://climatescape.org/categories/water"
    ]

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'ngodata.csv'
    }

    def parse(self, response):
        category_match = re.search(r"/categories/(.*?)/?$", response.url)
        if category_match:
            category = category_match.group(1)
        else:
            category = "Unknown"  # Default category if regex match fails

        ngos = response.xpath('//div[@class="border-gray-400 border-b flex text-gray-900 relative"]')

        for ngo in ngos:
            yield {
                "Area": category,
                "Name": ngo.css('span.font-bold.mr-2::text').get(),
                "Link": response.urljoin(ngo.css('a::attr(href)').get()),  # Extracting and joining the link
                "Basic info": ngo.xpath('.//div[@class="flex-grow flex flex-col justify-center sm:pl-4"]/p/text()').get(),
                "Type": ngo.xpath('.//span[@class="inline-block mt-1 px-2 py-1 text-xs rounded-full text-gray-700 mr-2"]/text()').get(),
                "Location": ngo.xpath('.//span[@class="inline-block mt-1 px-2 py-1 text-xs rounded-full text-gray-700 mr-2"][2]/text()').get(),
                "public/private": ngo.xpath('.//span[@class="inline-block mt-1 px-2 py-1 text-xs rounded-full text-gray-700 mr-2"][4]/text()').get(),
                
            }

        # Follow pagination links if present
        next_page = response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)
