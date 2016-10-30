class BasicFactory(object):
    def get_entity(self, entity_key, raw_object):
        raise NotImplementedError("get_entity() method must be implemented class {}".format(type(self)))
