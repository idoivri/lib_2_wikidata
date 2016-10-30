import entities
from factories import BasicFactory
import xml.etree.cElementTree as ET

TAG_TO_ENTITY_MAPPING = {
    '100': entities.Person,
    '110': entities.Institution,
    '151': entities.Location
}


ENTITY_KEYS = {
    '100.a': 'name',
    '100.9': 'name_langindic',
    '046.f': 'date_of_birth',
    '046.g': 'date_of_death',
    '400.a': 'name_in_langs',
    '400.9': 'langs_langindic',
    '678.a': 'bio_data',
    '151.a': 'name',
    '151.9': 'name_langindic',
    '451:a': 'name_in_langs',
    '451:9': 'langs_langindic',
    '550.a': 'type_of_place',
    '667.a': 'comment',
    '374.a': 'profession',
    '901.a': 'viaf',
    '001.' : 'national_lib_id',
    '001' : 'national_lib_id',
}


def get_record_key(record):
    root = record.getroot()
    for field in root:
        field_tag = field.attrib.get('tag')
        if '100' in field_tag:
            return '100'
        if '151' in field_tag:
            return '151'
        if '110' in field_tag:
            return '110'

class INLFactory(BasicFactory):
    def __init__(self, tag_to_entity_mapping=None):
        self.mapping = tag_to_entity_mapping or TAG_TO_ENTITY_MAPPING

    def get_entity(self,  raw_object, entity_keys=ENTITY_KEYS):
        record_key = get_record_key(raw_object)
        #100 is person
        if record_key == '100':
            name = ''
            name_in_langs = dict()
            bio_data = list()
            comment_list = list()
            eng_name = ''
            profession = list()
            name_diff = ''
            date_of_birth = ''
            date_of_death = ''
            viaf = ''
            national_lib_id = ''
            #get the names and date of birth and bio data
            for field in raw_object.getroot():
                key = field.attrib.get('tag')
                tag = entity_keys.get(key)
                if tag == 'name':
                    name = field.text
                elif tag == 'name_langindic':
                    # chack if this english name
                    if field.text == 'lat':
                        eng_name = name
                    # else add it to name_in_langs
                    else:
                        if field.text in name_in_langs:
                            name_in_langs.get(field.text).append(name)
                        else:
                            name_in_langs.update({field.text: [name]})
                elif tag == 'date_of_birth':
                    date_of_birth = field.text
                elif tag == 'date_of_death':
                    date_of_death = field.text
                elif tag == 'name_in_langs':
                    name_diff = field.text
                elif tag == 'langs_langindic':
                    if field.text in name_in_langs:
                        name_in_langs.get(field.text).append(name_diff)
                    else:
                        name_in_langs.update({field.text: [name_diff]})
                elif tag == 'bio_data':
                    bio_data.append(field.text)
                elif tag == 'comment':
                    comment_list.append(field.text)
                elif tag == 'profession':
                    profession.append(field.text)
                elif tag == 'viaf':
                    viaf = field.text
                elif tag == 'national_lib_id':
                    national_lib_id = field.text
            return entities.Person(eng_name, date_of_birth, date_of_death, name_in_langs, bio_data, comment_list, profession, viaf, national_lib_id)
        #110 is institue
        elif record_key == '110':
            return entities.Institution()
        #151 is location
        elif record_key == '151':
            name_in_langs = dict()
            types_of_place = list()
            comment_list = list()
            eng_name = ''
            name_diff = ''
            viaf = ''
            for field in raw_object.getroot():
                key = field.attrib.get('tag')
                tag = entity_keys.get(key)
                if tag == 'name':
                    name = field.text
                elif tag == 'name_langindic':
                    # chack if this english name
                    if field.text == 'lat':
                        eng_name = name
                    # else add it to name_in_langs
                    else:
                        if field.text in name_in_langs:
                            name_in_langs.get(field.text).append(name)
                        else:
                            name_in_langs.update({field.text: [name]})
                elif tag == 'type_of_place':
                    types_of_place.append(field.text)
                elif tag == 'name_in_langs':
                    name_diff = field.text
                elif tag == 'langs_langindic':
                    if field.text in name_in_langs:
                        name_in_langs.get(field.text).append(name_diff)
                    else:
                        name_in_langs.update({field.text: [name_diff]})
                elif tag == 'comment':
                    comment_list.append(field.text)
                elif tag == 'viaf':
                    viaf = field.text
            return entities.Location(eng_name, types_of_place , name_in_langs, comment_list, viaf)
        else:
            return None
        #    raise KeyError('Key {} was not recognized for factory {}'.format(entity_keys, type(self)))


