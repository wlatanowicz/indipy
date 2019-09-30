from typing import Any, Optional, Type, Union

from indi.device.properties.instance import elements as instance_elements
from indi.message import const
from indi.typing import CallbackDefinition


class Element:
    instance_class = Union[Type[instance_elements.BLOB], Type[instance_elements.Light], Type[instance_elements.Number], Type[instance_elements.Switch], Type[instance_elements.Text]]
    default_value: Any

    def __init__(
        self,
        name: str,
        label: Optional[str] = None,
        default=None,
        enabled: bool = True,
        onchange: Optional[CallbackDefinition] = None,
        onwrite: Optional[CallbackDefinition] = None,
        onread: Optional[CallbackDefinition] = None,
    ):
        self.name = name
        self.label = label or name
        self.default = self.default_value if default is None else default
        self.enabled = enabled

        self.onchange = onchange
        self.onwrite = onwrite
        self.onread = onread

    def instance(self, vector):
        return self.instance_class(vector, self)


class Number(Element):
    instance_class = instance_elements.Number
    default_value = 0.0

    def __init__(self, *args, format="%f", min=0, max=None, step=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.format = format
        self.min = min
        self.max = max if max else min
        self.step = step


class Text(Element):
    instance_class = instance_elements.Text
    default_value = ""


class Switch(Element):
    instance_class = instance_elements.Switch
    default_value = const.SwitchState.OFF


class Light(Element):
    instance_class = instance_elements.Light
    default_value = const.State.OK


class BLOB(Element):
    instance_class = instance_elements.BLOB
    default_value = ""
