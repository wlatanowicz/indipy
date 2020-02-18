from indi import message
from indi.message import checks
from indi.client import elements


class Vector:
    def_message_class = None
    set_message_class = None
    new_message_class = None
    children_class = None

    def __init__(self, device, msg: message.DefVector):
        self.group = msg.group
        self.name = msg.name
        self.label = msg.label
        self.timestamp = msg.timestamp
        self.message = msg.message
        self.state = msg.state
        self.device = device

        children = checks.children(
            [elements.Element.from_message(self, c) for c in msg.children],
            self.children_class,
        )
        self.elements = {ch.name: ch for ch in children}

    def __getitem__(self, key):
        return self.elements[key]

    def __contains__(self, key):
        return key in self.elements

    @classmethod
    def from_message(cls, device, msg):
        for subclass in cls.__subclasses__():
            if isinstance(msg, subclass.def_message_class):
                return subclass(device, msg)
        return None

    def get_element(self, name):
        return self.elements.get(name)

    def process_message(self, msg):
        if isinstance(msg, self.set_message_class):
            old_state = self.state
            self.state = msg.state

            if old_state != self.state:
                self.device.client.trigger_update(self, "state")

            for ch in msg.children:
                el = self.elements.get(ch.name)
                if el:
                    el.process_message(ch)

    def submit(self):
        ch = []
        for k, el in self.elements.items():
            ch.append(el.to_new_message())

        msg = self.new_message_class(
            device=self.device.name,
            name=self.name,
            timestamp=message.now(),
            children=ch,
        )

        self.device.send_message(msg)


class NumberVector(Vector):
    def_message_class = message.DefNumberVector
    set_message_class = message.SetNumberVector
    new_message_class = message.NewNumberVector
    children_class = elements.Number


class SwitchVector(Vector):
    def_message_class = message.DefSwitchVector
    set_message_class = message.SetSwitchVector
    new_message_class = message.NewSwitchVector
    children_class = elements.Switch


class TextVector(Vector):
    def_message_class = message.DefTextVector
    set_message_class = message.SetTextVector
    new_message_class = message.NewTextVector
    children_class = elements.Text


class BLOBVector(Vector):
    def_message_class = message.DefBLOBVector
    set_message_class = message.SetBLOBVector
    new_message_class = message.NewBLOBVector
    children_class = elements.BLOB


class LightVector(Vector):
    def_message_class = message.DefLightVector
    set_message_class = message.SetLightVector
    children_class = elements.Light
