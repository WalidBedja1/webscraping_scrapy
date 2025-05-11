import scrapy


class KboItem(scrapy.Item):
    # Section Généralités
    numero_entreprise = scrapy.Field()
    statut = scrapy.Field()
    situation_juridique = scrapy.Field()
    date_debut = scrapy.Field()
    denomination = scrapy.Field()
    adresse_siege = scrapy.Field()
    telephone = scrapy.Field()
    fax = scrapy.Field()
    email = scrapy.Field()
    adresse_web = scrapy.Field()
    type_entite = scrapy.Field()
    forme_legale = scrapy.Field()
    nombre_etablissements = scrapy.Field()

    # Autres sections
    fonctions = scrapy.Field()
    capacites_entrepreneuriales = scrapy.Field()
    qualites = scrapy.Field()
    autorisations = scrapy.Field()
    nace_codes = scrapy.Field()
    donnees_financieres = scrapy.Field()
    liens_entre_entites = scrapy.Field()
    liens_externes = scrapy.Field()


