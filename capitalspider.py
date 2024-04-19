import scrapy
import pandas as pd

class NgodataSpider(scrapy.Spider):
    name = "capitalspider"
    allowed_domains = ["climatescape.org"]
    start_urls = [
        "https://climatescape.org/capital/venture-capital",
        "https://climatescape.org/capital/accelerator",
        "https://climatescape.org/capital/project-finance",
        "https://climatescape.org/capital/angel",
        "https://climatescape.org/capital/private-equity",
        "https://climatescape.org/capital/incubator",
        "https://climatescape.org/capital/grant",
        "https://climatescape.org/capital/fellowships",
        "https://climatescape.org/capital/prize",
    ]

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'capitaldata.csv'
    }

    def parse(self, response):
        # Extract type of capital from the URL
        capital_type = response.url.split("/")[-2]

        # Select all the capital program elements
        capital_programs = response.css('div.border-gray-400.border-b.flex.text-gray-900.relative')

        for program in capital_programs:
            # Extracting the name of the capital
            name = program.css('p > span.font-bold::text').get()

            # Extracting the basic info about the capital
            basic_info = program.css('p::text').get()

            # Extracting the link of the capital page
            link = program.css('a::attr(href)').get()
            if link:
                # Constructing the absolute URL
                link = response.urljoin(link).strip()

            yield {
                'Capital Type': capital_type,
                'Name': name.strip() if name else None,
                'Link': link if link else None,
                'Basic Info': basic_info.strip() if basic_info else None,
                
            }
