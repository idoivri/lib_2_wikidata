try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

KNOWN_FIELD_TAGS = ['100', '110', '151']

TAG_WHITELIST = ['100', '400', '700', '678', '667', '151', '550', '451', '374', '046', '901', '001']


class INLXmlParser:
    def __init__(self, reader, whitelist=TAG_WHITELIST):
        self.reader = reader
        # self.whitelist = whitelist or KNOWN_FIELD_TAGS
        self.whitelist = whitelist

    def clearxml(self):

        # # scan the datafields in the records and copy to the new one only the tags in the whitelist
        # for record in root:    # create new record
        newRecord = ET.Element('record')
        for field in self.reader:
            fieldtag = field.attrib.get('tag')
            if fieldtag in self.whitelist:
                temptag = fieldtag
                if fieldtag == '001':
                    newTag = ET.SubElement(newRecord, 'datafield', {'tag': '001'})
                    newTag.text = field.text
                else:
                    # tag 700 and 400 are the same
                    if temptag == '700':
                        temptag = '400'
                    for data in field:
                        newFieldTag = temptag
                        newFieldTag += '.'
                        newFieldTag += data.attrib.get('code')
                        newTag = ET.SubElement(newRecord, 'datafield', {'tag': newFieldTag})
                        newTag.text = data.text

        newRecordTree = ET.ElementTree(newRecord)
        return ET.ElementTree(newRecord)
