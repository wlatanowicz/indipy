from typing import Dict, Optional, Tuple, Type, Union

from indi.device.events import EventSourceDefinition
from indi.device.properties.const import (
    Permissions,
    PermissionsType,
    State,
    StateType,
    SwitchRule,
    SwitchRuleType,
)
from indi.device.properties.definition.elements import (
    BLOB,
    Element,
    Light,
    Number,
    Switch,
    Text,
)
from indi.device.properties.instance import vectors as instance_vectors
from indi.message import const


class Vector(EventSourceDefinition):
    element_class: Type[Element]
    instance_class: Type[instance_vectors.Vector]

    def __init__(
        self,
        name: str,
        label: Optional[str] = None,
        state: StateType = State.OK,
        perm: PermissionsType = Permissions.READ_WRITE,
        timeout: float = 0,
        enabled: bool = True,
        elements: Optional[Dict[str, Element]] = None,
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
                raise Exception(
                    f"Element '{k}' of vector {self.name} of type {self.__class__.__name__} "
                    f"is expected to be of type {self.__class__.element_class.__name__}, "
                    f"{element.__class__.__name__} given"
                )

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

    def __init__(
        self,
        *args,
        rule: SwitchRuleType = SwitchRule.ONE_OF_MANY,
        default_on: Optional[Union[str, Tuple[str, ...]]] = None,
        **kwargs,
    ):
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
