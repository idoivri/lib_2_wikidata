from entities.basic_entity import BasicEntity


class Institution(BasicEntity):
    def __init__(self, viaf=None):
        super().__init__(viaf)
        raise NotImplementedError()
