import pywikibot
from pywikibot import pagegenerators
from pywikibot.data import wikidataquery

repo = pywikibot.Site().data_repository()


def write_to_wd(entity):
    if entity.viaf:
        a = get_entity_by_viaf(entity.viaf)


# Finds the matching record in Wikidata by VIAF identifier
def get_entity_by_viaf(viaf):
    sparql = "SELECT ?item WHERE {{ ?item wdt:P214 ?VIAF filter(?VIAF = '{}') }}".format(viaf)

    entities = pagegenerators.WikidataQueryPageGenerator(sparql)
    entities = list(entities)
    if len(entities) == 0:
        print("No entity found for VIAF: {}".format(viaf))
        return None
    elif len(entities) > 1:
        # TODO: is it possible to have multiple VIAFs?
        raise Exception('VIAF is expected to be unique')
    import pdb; pdb.set_trace()
    return entities[0]