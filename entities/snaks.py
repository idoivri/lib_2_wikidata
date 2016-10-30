from datetime import datetime

from libs import JsonSerializable


class BasicSnak(JsonSerializable):
    def __init__(self, snaktype, property, datatype, datavalue):
        self.snaktype = snaktype
        self.property = property
        self.datatype = datatype
        self.datavalue = datavalue


class StringSnak(BasicSnak):
    def __init__(self, property, value):
        datavalue = {
            "type": "string",
            "value": value
        }
        super().__init__(snaktype="value", property=property, datatype="string", datavalue=datavalue)


class MonoLingualStringSnak(BasicSnak):
    def __init__(self, property, value, language):
        datavalue = {
            "type": "monolingualtext",
            "value": {
                "language": language,
                "text": value
            }
        }
        super().__init__(snaktype="value", property=property, datatype="monolingualtext", datavalue=datavalue)


class EntityIdSnak(BasicSnak):
    def __init__(self, property, entity_type, entity_id):
        datavalue = {
            "value": {
                "entity-type": entity_type,
                "numeric-id": entity_id
            },
            "type": "wikibase-item"
        }
        super().__init__(snaktype="value", property=property, datatype="wikibase-entityid", datavalue=datavalue)


class UrlSnak(BasicSnak):
    def __init__(self, property, url):
        datavalue = {
            "type": "string",
            "value": url
        }
        super().__init__(snaktype="value", property=property, datatype="url", datavalue=datavalue)


class TimeSnak(BasicSnak):
    def __init__(self, property, date, precision=11):
        if not isinstance(date, datetime):
            date = datetime(date)
        datavalue = {
            "value": {
                "time": date.isoformat(),
                "timezone": 0,
                "before": 0,
                "after": 0,
                "precision": precision,
                "calendarmodel": "http:\/\/www.wikidata.org\/entity\/Q1985727"
            },
            "type": "time"
        }
        super().__init__(snaktype="value", property=property, datatype="time", datavalue=datavalue)


class GeoSnak(BasicSnak):
    def __init__(self, latitude, longitude, precision):
        datavalue = {
            "value": {
                "latitude": latitude,
                "longitude": longitude,
                "altitude": None,
                "precision": precision,
                "globe": "http:\/\/www.wikidata.org\/entity\/Q2"
            },
            "type": "globecoordinate"
        }
        super().__init__(snaktype="value", property=property, datatype="globe-coordinate", datavalue=datavalue)


class SomeValueSnak(BasicSnak):
    def __init__(self, property):
        super().__init__(snaktype="somevalue", property=property, datatype=None, datavalue=None)
