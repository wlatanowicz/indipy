from typing import Type

from indi.device.events import EventSourceDefinition
from indi.device.properties.const import Permissions, State, SwitchRule
from indi.device.properties.definition.elements import BLOB, Light, Number, Switch, Text
from indi.device.properties.instance import elements as instance_elements
from indi.device.properties.instance import vectors as instance_vectors
from indi.message import const


class Vector(EventSourceDefinition):
    element_class = Type[instance_elements.Element]
    instance_class: Type[instance_vectors.Vector]

    def __init__(
        self,
        name,
        label=None,
        state=State.OK,
        perm=Permissions.READ_WRITE,
        timeout=0,
        enabled=True,
        elements=None,
    ):
        super().__init__()
        self.name = name
        self.label = label or name
        self.state = state
        self.perm = perm
        self.timeout = timeout
        self.enabled = enabled

        if not elements:
            raise Exception("No vector elements declared")

        for k, element in elements.items():
            if self.__class__.element_class and not isinstance(
                element, self.__class__.element_class
            ):
                raise Exception("")

        self.elements = elements

    def instance(self, group):
        return self.instance_class(group=group, definition=self)

    def __getattr__(self, item):
        element = self.elements.get(item)
        if element:
            return element

        return self.__getattribute__(item)


class NumberVector(Vector):
    element_class = Number
    instance_class = instance_vectors.NumberVector


class TextVector(Vector):
    element_class = Text
    instance_class = instance_vectors.TextVector


class SwitchVector(Vector):
    element_class = Switch
    instance_class = instance_vectors.SwitchVector

    RULES = SwitchRule

    def __init__(self, *args, rule=SwitchRule.ONE_OF_MANY, default_on=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.rule = rule
        if default_on is not None:
            default_on = (default_on,) if isinstance(default_on, str) else default_on
            for k, el in self.elements.items():
                if el.name in default_on:
                    el.default = const.SwitchState.ON


class LightVector(Vector):
    element_class = Light
    instance_class = instance_vectors.LightVector

    def __init__(self, *args, **kwargs):
        if kwargs.get("perm"):
            del kwargs["perm"]
        if kwargs.get("timeout"):
            del kwargs["timeout"]

        super().__init__(*args, **kwargs)


class BLOBVector(Vector):
    element_class = BLOB
    instance_class = instance_vectors.BLOBVector
