from builder.base_builder import BaseBuilder, Pipeline
from commons.database import Database


class Executor:
    # Director
    def __init__(self, builder: BaseBuilder) -> None:
        self.pipeline: Pipeline = None
        self.builder = builder

    def construct(self):
        self.pipeline = self.builder.construct()

    def execute(self, conn: Database):
        with conn:
            for query in self.pipeline:
                conn.execute(query)
