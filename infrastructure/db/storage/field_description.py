from dataclasses import dataclass

from typing import Callable


@dataclass
class FieldDescription:
    name: str
    type: Callable
