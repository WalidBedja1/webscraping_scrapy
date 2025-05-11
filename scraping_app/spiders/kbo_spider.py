import csv
import scrapy
from ..items import KboItem
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags, strip_html5_whitespace
from ..utils.paths import get_path
from ..utils.data_transformer import clean_processor, address_processor, date_processor

class KboSpider(scrapy.Spider):
    name = "kbo_spider"
    custom_settings = {
        "FEEDS": {
            "kbo_data.json": {
                "format": "json",
                "encoding": "utf8",
                "indent": 4,
                "overwrite": True
            }
        },
        "DOWNLOAD_DELAY": 1,
        "AUTOTHROTTLE_ENABLED": True,
        "DEFAULT_REQUEST_HEADERS": {
            "Accept-Language": "fr-FR,fr;q=0.9",
            "Referer": "https://kbopub.economie.fgov.be/"
        }
    }

    def start_requests(self):
        csv_path = get_path()
        try:
            with open(csv_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if not (enterprise_num := row.get("EnterpriseNumber")):
                        continue

                    yield scrapy.Request(
                        url=f"https://kbopub.economie.fgov.be/kbopub/zoeknummerform.html?nummer={enterprise_num}&actionLu=Rechercher&lang=fr",
                        callback=self.parse,
                        meta={"enterprise_num": enterprise_num},
                        errback=self.handle_error
                    )

        except Exception as e:
            self.logger.error(f"Erreur lecture CSV: {e}")
            raise

    def parse(self, response):
        if response.status != 200:
            self.logger.warning(f"Page non trouvée: {response.meta['enterprise_num']}")
            return

        loader = ItemLoader(item=KboItem(), selector=response)
        loader.default_input_processor = MapCompose(remove_tags, strip_html5_whitespace, clean_processor)
        loader.default_output_processor = TakeFirst()

        # Champs communs
        loader.add_value("numero_entreprise", response.meta["enterprise_num"])




        # Mapping des XPath optimisé
        field_mapping = {
            'statut': "//table//tr[3]/td[2]/strong/span/text()",
            'situation_juridique': "//table//tr[4]/td[2]/strong/span/text()",
            'date_debut': ("//table//tr[6]/td[2]/text()", date_processor),
            'denomination': "//table//tr[7]/td[2]/text()",
            'adresse_siege': ("//table//tr[10]/td[2]//text()", address_processor),
            'telephone': "//table//tr[11]/td[2]//td[1]/text()",
            'email': "//table//tr[13]/td[2]//a/text()",
            'type_entite': "//table//tr[15]/td[2]/text()",
            'forme_legale': "//table//tr[16]/td[2]/text()"
        }

        for field, xpath in field_mapping.items():
            loader.add_xpath(field, *xpath) if isinstance(xpath, tuple) else loader.add_xpath(field, xpath)

        yield loader.load_item()

    def handle_error(self, failure):
        self.logger.error(f"Erreur sur {failure.request.url}: {failure.value}")