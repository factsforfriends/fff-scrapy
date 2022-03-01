import scrapy

class piqdSpider(scrapy.Spider):
    name = 'piqd'
    base_url = 'https://www.piqd.de'
    custom_settings = {
        "FEED_EXPORT_ENCODING": "utf-8"
    }

    def start_requests(self):
        urls = [
            self.base_url + '/special/ukraine?page=1'
        ]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)
    
    def parse(self, response, **kwargs):
        #
        # Parse all previews
        #
        previews = response.css('div.pq-piq_tile')

        for preview in previews:
            date = preview.css('div.pq-piq_tile-created::text').get(default='').strip()
            headline = preview.css('h2.pq-piq_tile-headline a::text').get(default='').strip()
            channel = preview.css('div.pq-piq_tile-channel a::text').get(default='').strip()
            author_name = ''.join(preview.css('span.pq-piqr-name').xpath('text()').getall()).strip()
            author_image = preview.css('div.pq-piqr-img').xpath('./a/img/@src').get()
            media_type = preview.css('div.pq-piq_tile__type').xpath('./svg/use').attrib['xlink:href'].replace('#icon-', '')
            portfolio_item = preview.attrib['id']
            url = self.base_url + preview.css('h2.pq-piq_tile-headline a').attrib['href']

            yield {
                'date': date,
                'headline': headline,
                'channel': channel,
                'author': {
                    'name': author_name,
                    'image': author_image
                },
                'media_type': media_type,
                'portfolio_item': portfolio_item,
                'url': url
            }
        
        next_page = response.css('div.pq-piq_tiles-more a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback = self.parse)