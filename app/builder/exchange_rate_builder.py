from builder.pgsql_builder import PgSQLBuilder
from commons.models import StagingExchangeRate


class ExchangeRateBuilder(PgSQLBuilder):
    staging_table = StagingExchangeRate.NAME
    staging_fields = StagingExchangeRate.COLUMNS
    unique_field = StagingExchangeRate.exchange_rate_id
    decimal_fields = [
        StagingExchangeRate.rate,
    ]
    max_length_fields = {
        StagingExchangeRate.from_currency: 3,
        StagingExchangeRate.to_currency: 3,
    }

    dimension_sqls = [
        (
            "insert into "
            "dim_currency (currency_code) "
            "select "
            "distinct from_currency "
            "from "
            f"{staging_table}  ser "
            "where "
            "not exists ( "
            "select 1 from "
            "dim_currency dc "
            "where "
            "dc.currency_code = ser.from_currency)"
        ),
        (
            "insert into "
            "dim_currency (currency_code) "
            "select "
            "distinct to_currency "
            "from "
            f"{staging_table}  ser "
            "where "
            "not exists ( "
            "select 1 from "
            "dim_currency dc "
            "where "
            "dc.currency_code = ser.to_currency)"
        ),
    ]

    target_sql = (
        "insert into "
        "fact_exchange_rate (exchange_rate_id, "
        "from_currency_id, "
        "to_currency_id, "
        "effective_date_id, "
        "rate) "
        "select "
        "ser.exchange_rate_id, "
        "dcurr1.currency_id, "
        "dcurr2.currency_id, "
        "dcal.date_id, "
        "cast(ser.rate as decimal) "
        f"from {staging_table} ser "
        "inner join dim_currency dcurr1 on "
        "ser.from_currency = dcurr1.currency_code "
        "inner join dim_currency dcurr2 on "
        "ser.to_currency = dcurr2.currency_code "
        "inner join dim_calendar dcal on "
        "cast(ser.effective_date as date) = dcal.date "
        "where "
        "ser.error_message is null"
    )
