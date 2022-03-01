import scrapy
from scrapy.http import HtmlResponse
import json


class KatapultUaSpider(scrapy.Spider):
    encoding = "utf-8"
    name = 'katapult_ukraine'
    base_url = 'https://katapult-magazin.de/de'
    custom_settings = {
        "FEED_EXPORT_ENCODING": encoding
    }

    def start_requests(self):
        urls = [
            self.base_url + '/artikel/liveblog-zur-ukraine'
        ]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):

        # parse and get raw html between selector, then split based on date selector
        previews = response.css('section.content.content-article').extract()[0] \
            .split('<div class="column text-gray-dark">')

        # remove first element (page intro)
        del previews[0]

        for preview in previews:
            # append split div to have valid html again
            preview = '<div class="column text-gray-dark">' + preview
            # manually create parseable response
            response = HtmlResponse(url="dummy", body=preview, encoding=self.encoding)
            # extract data from dummy response using selectors
            date = response.css('div.column.text-gray-dark::text').get(default='').strip()

            # multiline texts may occur
            content = '\n'.join(response.css('p::text').getall()).strip()

            # multiple images may occur
            images = response.css('figure.figure-image.center img')
            image_links = []
            for image in images:
                image_links.append(image.attrib['data-srcset'].split(',')[-1].strip().split(' ')[0])

            yield {
                'date': date,
                'content': content,
                'image': json.dumps(image_links)
            }
