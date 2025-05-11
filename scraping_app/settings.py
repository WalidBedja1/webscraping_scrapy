MONGO_URI = "mongodb://localhost:27017/scraping_app"  # ou URI distant
MONGO_DATABASE = "scraping_app"

BOT_NAME = "scraping_app"

SPIDER_MODULES = ["scraping_app.spiders"]
NEWSPIDER_MODULE = "scraping_app.spiders"

ADDONS = {}


# Obey robots.txt rules
ROBOTSTXT_OBEY = False


FEED_EXPORT_ENCODING = "utf-8"

ITEM_PIPELINES = {
    "scraping_app.pipelines.ScrapingAppPipeline": 300,
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scraping_app.middlewares.KboDownloaderMiddleware': 543,
}

SPIDER_MIDDLEWARES = {
    'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,
    'scraping_app.middlewares.KboSpiderMiddleware': 500,
}
