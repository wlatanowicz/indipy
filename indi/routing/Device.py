class Device:
    def message_from_client(self, message):
        raise Exception('Not implemented')

    @property
    def routing_key(self):
        raise Exception('Not implemented')
