from abc import ABC, abstractmethod
from typing import Dict, Iterable, List, Optional

from commons.database import Database


class Pipeline:
    def __init__(self):
        self._queries: List[str] = []

    def __iter__(self) -> Iterable[str]:
        return iter(self._queries)

    def add(self, query: str):
        self._queries.append(query + ";")

    def execute(self, session: Database):
        with session:
            for query in self._queries:
                session.execute(query)


class BaseBuilder(ABC):
    row_id_field: str = "row_id"
    error_field: str = "error_message"

    staging_table: str = None
    staging_fields: List[str] = []

    unique_field: str = None
    integer_fields: List[str] = []
    decimal_fields: List[str] = []
    max_length_fields: Dict[str, int] = {}
    allowed_field_values: Dict[str, List] = {}

    dimension_sqls: List[str] = []
    target_sql: Optional[str] = None
    extra_sqls: List[str] = []

    def __init__(self, filepath: str) -> None:
        self.pipeline = Pipeline()
        self.filepath = filepath

    def reset(self):
        self.pipeline = Pipeline()

    @abstractmethod
    def build_staging(self):
        pass

    @abstractmethod
    def build_dedup(self):
        pass

    @abstractmethod
    def build_checks(self):
        pass

    @abstractmethod
    def build_cleanup(self):
        pass

    def build_target(self):
        if self.target_sql:
            self.pipeline.add(self.target_sql)

    def build_dimensions(self):
        for sql in self.dimension_sqls:
            self.pipeline.add(sql)

    def build_extras(self):
        for sql in self.extra_sqls:
            self.pipeline.add(sql)
