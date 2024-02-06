from typing import List
from dataclasses import dataclass

from infrastructure.db.storage.field_description import FieldDescription


@dataclass
class TodoTaskCSVEntity:
    data: str
    data_schema: List[FieldDescription]

    def get_data(self):
        return self.data
