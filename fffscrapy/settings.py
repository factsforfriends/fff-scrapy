import os

# Scrapy settings for fffscrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'fffscrapy'

SPIDER_MODULES = ['fffscrapy.spiders']
NEWSPIDER_MODULE = 'fffscrapy.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'FactsForFriends Spider (+https://factsforfriends.de)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# AWS secrets
# 
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')

FEEDS = {
    's3://fff-ingest/%(name)s.json': {
        'format': 'json',
        'encoding': 'utf-8',
        'overwrite': True,
        'store_empty': True
    }
}
