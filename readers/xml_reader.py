from __future__ import absolute_import
import json
import csv
import parsers
import factories
from entities import Person
from writers.wd_writer import get_entity_by_viaf

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def read_file(path, element_key):
    # get an iterable
    record_counter = 0
    context = ET.iterparse(path, events=("start", "end"))

    # turn it into an iterator
    context = iter(context)

    # get the root element
    event, root = context.__next__()

    # the factory
    inl_factory = factories.INLFactory()
    files = {}
    for event, element in context:
        if 'end' in event:
            if element_key in element.tag:
                # enter the processing here
                record_counter += 1

                # cleaned element is a tree
                inl_parser = parsers.INLXmlParser(element)
                cleaned_element = inl_parser.clearxml()
                entity = inl_factory.get_entity(cleaned_element)

                # test print the entity
                if entity != None:
                    if entity.TYPE not in files:
                        files[entity.TYPE] = open("out/{}.csv".format(entity.TYPE), 'w+', encoding='utf8')
                    json_entity = entity.to_json()
                    print(json_entity)
                    #writer = csv.DictWriter(files[entity.TYPE], entity.CSV_FIELDS)
                    #writer.writerow(entity.to_dict())

                    if entity.viaf:
                        print(get_entity_by_viaf(entity.viaf))

                # TODO analys and upload the entity
                element.clear()
    print(record_counter)


if __name__ == '__main__':
    read_file(r"../../NLI-nnl10.xml", 'record')
