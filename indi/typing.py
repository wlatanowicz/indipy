from typing import Callable, Union

Callback = Callable[..., None]
CallbackDefinition = Union[Callback, str]
