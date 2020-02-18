from indi.message.IndiMessage import IndiMessage


class OneLight(IndiMessage):
    from_device = True

    def __init__(self, name, value, **junk):
        self.name = name
        self.value = value
