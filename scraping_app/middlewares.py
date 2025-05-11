from scrapy import signals
from urllib.parse import urlparse
import logging


class KboSpiderMiddleware:
    """Middleware spécifique pour le spider KBO"""

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def process_spider_input(self, response, spider):
        """Vérifie que la réponse est en français"""
        if 'content-language' in response.headers and b'nl' in response.headers['content-language']:
            spider.logger.warning(f"La réponse est en néerlandais : {response.url}")
        return None

    def spider_opened(self, spider):
        spider.logger.info(f"Spider KBO démarré: {spider.name}")

    def spider_closed(self, spider):
        spider.logger.info(f"Spider KBO terminé: {spider.name}")


class KboDownloaderMiddleware:
    """Middleware de téléchargement optimisé pour KBO"""

    def __init__(self):
        self.stats = {}

    def process_request(self, request, spider):
        """Force les headers français pour toutes les requêtes KBO"""
        if 'kbopub.economie.fgov.be' in request.url:
            request.headers.setdefault('Accept-Language', 'fr-FR,fr;q=0.9')
            request.headers.setdefault('Referer', 'https://kbopub.economie.fgov.be/?lang=fr')
        return None

    def process_response(self, request, response, spider):
        """Log les stats de téléchargement"""
        domain = urlparse(request.url).netloc
        self.stats[domain] = self.stats.get(domain, 0) + 1
        return response

    def process_exception(self, request, exception, spider):
        """Gère spécifiquement les timeout pour KBO"""
        if 'kbopub.economie.fgov.be' in request.url:
            spider.logger.warning(f"Timeout sur {request.url}, réessai prévu")
            return request
        return None