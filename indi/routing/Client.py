class Client:
    def message_from_device(self, message):
        raise Exception('Not implemented')

    @property
    def routing_key(self):
        return None
