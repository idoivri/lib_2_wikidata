import json

from entities.snaks import *
from entities.basic_entity import BasicEntity


class Person(BasicEntity):
    def __init__(self, name, date_of_birth, date_of_death, name_in_langs, bio_data, comments_list, profession, viaf,
                 national_lib_id):
        """

        :param name:
        :param date_of_birth:
        :param name_in_langs: Mapping of the persons's name in various languages, as a dictionary. For example:
            {
                "latin": "George"
                "heb": "[george in hebrew]"
            }
        """
        self.name = name
        dob = [date_of_birth]
        dod = [date_of_death]
        self.name_in_langs = name_in_langs
        self.national_lib_id = national_lib_id

        bio_data_dict = dict()
        struct_bio_data = dict()
        for elem in bio_data:
            elem_splitted = elem.split(":")
            if len(elem_splitted) == 2:
                bio_data_key = elem_splitted[0].strip()
                bio_data_value = elem_splitted[1].strip()

                if bio_data_key.startswith(u"תאריך לידה: "):
                    dob.append(bio_data_value)
                elif bio_data_key.startswith(u"תאריך פטירה: "):
                    dod.append(bio_data_value)
                elif bio_data_key.startswith(u"מקצוע: ") or bio_data_key.startswith(u"מיקצוע: "):
                    profession.append(bio_data_value)
                else:
                    struct_bio_data[bio_data_key] = bio_data_value

                if bio_data_key in bio_data_dict:
                    bio_data_dict.get(bio_data_key).append(bio_data_value)
                else:
                    bio_data_dict.update(
                        {bio_data_key: [bio_data_value]}
                    )
            else:
                bio_data_dict.update({elem: ''})
        self.bio_data = bio_data_dict
        self.comments_list = comments_list
        self.profession = profession
        self.viaf = viaf
        self.date_of_birth = dob
        self.date_of_death = dod
        self.struct_bio_data = struct_bio_data

    # CSV_FIELDS = ["name", "biodata", "comments", "viaf"]

    CSV_FIELDS = ["678 - biodata", "001 - national lib id"]
    TYPE = 'PERSON'

    # CSV_FIELDS = ["viaf", "name", "biodata", "comments"]
    CSV_FIELDS = ["viaf", "national_lib_id", "name", "date_of_birth", "date_of_death", "name_in_langs", "bio_data",
                  "struct_bio_data", "comments_list", "profession"]
    TYPE = 'PERSON'

    def print_entity(self):
        print("Name = " + self.name)
        print("Birth year = " + self.date_of_birth)
        print("Death year = " + self.date_of_death)
        print("Names in langs = " + str(self.name_in_langs))
        print("Bio Data = " + json.dumps(self.bio_data))
        print("Comments = " + json.dumps(self.comments_list))
        print("Profession = " + json.dumps(self.profession))

    def to_csv_dict(self):
        return {'viaf': self.viaf, 'name': self.name, 'biodata': self.bio_data,
                'comments': json.dumps(self.comments_list, ensure_ascii=False)}

    def to_wd_claims(self):
        claims = []

        if self.date_of_birth:
            claims.append({
                "type": "claim",
                "mainsnak": TimeSnak(property='P569', date=self.date_of_birth[0]).to_json()
            })
        if self.date_of_death:
            claims.append({
                "type": "claim",
                "mainsnak": TimeSnak(property='P570', date=self.date_of_death[0]).to_json()
            })
        if self.profession:
            for elem in self.profession:
                claims.append({
                    "type": "claim",
                    "mainsnak": StringSnak(property='P106', value=elem).to_json()
                })
        if self.viaf:
            claims.append({
                "type": "claim",
                "mainsnak": StringSnak(property='P214', value=self.viaf).to_json()
            })
        if self.struc_bio_data:
            for bio_key, bio_value in self.struc_bio_data.items():
                if bio_key.startswith(u"מקום לידה"):
                    claims.append({
                        "type": "claim",
                        "mainsnak": StringSnak(property='P19', value=bio_value).to_json()
                    })
                if bio_key.startswith(u"מקום פטירה"):
                    claims.append({
                        "type": "claim",
                        "mainsnak": StringSnak(property='p20', value=bio_value).to_json()
                    })

        return claims
