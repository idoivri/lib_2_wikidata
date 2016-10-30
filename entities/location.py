import json

from entities.basic_entity import BasicEntity


class Location(BasicEntity):
    def __init__(self, name, types_of_place, name_in_langs, comments_list, viaf):
        self.name = name
        self.types_of_place = types_of_place
        self.name_in_langs = name_in_langs
        self.comments_list = comments_list
        self.viaf = viaf

    # CSV_FIELDS = ["name", "comments"]
    CSV_FIELDS = ["viaf", "name", "types_of_place", "name_in_langs", "comments_list"]
    TYPE = "LOCATION"


    def print_entity(self):
        print("Name = " + self.name)
        print("Name in langs = " + str(self.name_in_langs))
        print("Types = " + str(self.types_of_place))
        print("Comments = " + str(self.comments_list))

    def to_csv_dict(self):
        return {'name': self.name,
                'comments': json.dumps(self.comments_list, ensure_ascii=False)}
