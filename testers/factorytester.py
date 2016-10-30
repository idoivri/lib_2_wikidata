from __future__ import absolute_import
import parsers
import factories
import xml.etree.cElementTree as ET

xmlpath = 'C:/Users/Ilsar/Documents/datahack/xml_example.xml'

xmltree = ET.parse(xmlpath)
entities = list()
inl_factory = factories.INLFactory()

for record in xmltree.getroot():
    inl_parser = parsers.INLXmlParser(record)
    clean_record = inl_parser.clearxml()
    entities.append(inl_factory.get_entity(clean_record))

for entity in entities:
    entity. print_entity()

