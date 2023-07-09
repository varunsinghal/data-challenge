import logging
from logging.handlers import TimedRotatingFileHandler

import click

from builder.customer_builder import CustomerBuilder
from builder.exchange_rate_builder import ExchangeRateBuilder
from builder.transaction_builder import TransactionBuilder
from commons.database import Database
from executor import Executor

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        TimedRotatingFileHandler(
            "logs/system.log", when="midnight", interval=1
        ),
        logging.StreamHandler(),
    ],
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logging.getLogger("sqlalchemy").setLevel(logging.CRITICAL)


session = Database()


@click.group(name="cli")
def cli():
    pass


@cli.command(name="customer_csv", help="ingestion of customer via csv file")
@click.option("--file_path", required=True)
def customer_csv_cli(file_path: str):
    builder = CustomerBuilder(filepath=file_path)
    executor = Executor(builder)
    executor.construct()
    executor.execute(session)


@cli.command(
    name="transaction_csv", help="ingestion of transaction data via csv file"
)
@click.option("--file_path", required=True)
def transaction_csv_cli(file_path: str):
    builder = TransactionBuilder(filepath=file_path)
    executor = Executor(builder)
    executor.construct()
    executor.execute(session)


@cli.command(
    name="exchange_rate_csv", help="ingestion of exchange rates via csv file"
)
@click.option("--file_path", required=True)
def exchange_rate_csv_cli(file_path: str):
    builder = ExchangeRateBuilder(filepath=file_path)
    executor = Executor(builder)
    executor.construct()
    executor.execute(session)


if __name__ == "__main__":
    cli()
