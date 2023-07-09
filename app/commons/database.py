import logging
import os

import sqlalchemy
import sqlparse
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URI = (
    "postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database}"
)


class Database:
    def __init__(self, commit: bool = True) -> None:
        self.log = logging.getLogger(__class__.__name__)
        self.engine = sqlalchemy.create_engine(self.get_connection_uri())
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.commit = commit

    def get_connection_uri(self):
        db_credentials = {
            "username": os.environ.get("POSTGRES_USER"),
            "password": os.environ.get("POSTGRES_PASSWORD"),
            "hostname": os.environ.get("POSTGRES_HOSTNAME"),
            "port": os.environ.get("POSTGRES_PORT"),
            "database": os.environ.get("POSTGRES_DATABASE"),
        }
        return DATABASE_URI.format(**db_credentials)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_trc):
        if exc_value:
            self.session.rollback()
        elif self.commit:
            self.session.commit()
        self.session.close()

    def execute(self, raw_sql: str):
        self.log.debug(
            sqlparse.format(raw_sql, reindent=True, keyword_case="upper")
        )
        result = self.session.execute(sqlalchemy.text(raw_sql))
        return result
