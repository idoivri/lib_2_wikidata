import json


class JsonSerializable(object):
    def __repr__(self):
        return str(self.to_json())

    def to_json(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

    def to_dict(self):
        return self.__dict__