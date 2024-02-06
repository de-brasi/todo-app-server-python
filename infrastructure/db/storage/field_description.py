from dataclasses import dataclass


@dataclass
class FieldDescription:
    name: str
    type: type
