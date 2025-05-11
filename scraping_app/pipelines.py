import pymongo
from pymongo.errors import ConnectionFailure


class ScrapingAppPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE")
        )

    def open_spider(self, spider):
        try:
            self.client = pymongo.MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            # Test de connexion réelle
            self.client.admin.command('ping')
            self.db = self.client[self.mongo_db]
            spider.logger.info("✅ Connexion MongoDB réussie.")
        except ConnectionFailure as e:
            spider.logger.error(f"❌ Connexion MongoDB échouée : {e}")
            raise e  # Optionnel : arrête le spider si la DB est indisponible

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item_dict = dict(item)

        if not item_dict.get("numero_entreprise"):
            raise scrapy.exceptions.DropItem("Numéro d'entreprise manquant")

        self.db[spider.name].update_one(
            {"numero_entreprise": item_dict["numero_entreprise"]},  # Clé naturelle
            {"$set": item_dict},
            upsert=True
        )
        return item