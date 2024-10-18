from typing import List, Optional, Type, Union
from uuid import UUID
from tortoise.fields import Field
from tortoise import Model

class StrArrayField(Field[List[str]]):
    class _db_postgres:
        SQL_TYPE="TEXT[]"
    def to_db_value(self, value: list[str], instance: "Union[Type[Model], Model]") -> Optional[str]:
        return value

    def to_python_value(self, value: list[str]) -> Optional[Union[list[str]]]:
        return value

class UUIDArrayField(Field[List[UUID]]):
    class _db_postgres:
        SQL_TYPE="UUID[]"
    def to_db_value(self, value: list[UUID], instance: "Union[Type[Model], Model]") -> Optional[UUID]:
        return value

    def to_python_value(self, value: list[UUID]) -> Optional[Union[list[UUID]]]:
        return value