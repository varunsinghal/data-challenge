from builder.pgsql_builder import PgSQLBuilder
from commons.models import StagingTransaction


class TransactionBuilder(PgSQLBuilder):
    staging_table = StagingTransaction.NAME
    staging_fields = StagingTransaction.COLUMNS
    unique_field = StagingTransaction.transaction_id
    integer_fields = [
        StagingTransaction.customer_id,
    ]
    decimal_fields = [
        StagingTransaction.amount,
    ]
    max_length_fields = {
        StagingTransaction.currency: 3,
    }
    allowed_field_values = {StagingTransaction.transaction_type: ["in", "out"]}

    dimension_sqls = [
        (
            "insert "
            "into "
            "dim_currency (currency_code) "
            "select "
            "distinct currency "
            "from "
            f"{staging_table} st "
            "where "
            "not exists ("
            "select 1 from "
            "dim_currency dc "
            "where "
            "dc.currency_code = st.currency"
            ")"
        ),
    ]

    target_sql = (
        "insert into "
        "fact_transaction (transaction_id, "
        "customer_id, "
        "transaction_type, "
        "amount, "
        "currency_id, "
        "date_id) "
        "select "
        "st.transaction_id, "
        "dim_customer.customer_id, "
        "case "
        "when st.transaction_type = 'in' then 1 "
        "else 0 end, "
        "cast(st.amount as decimal), "
        "dim_currency.currency_id, "
        "dim_calendar.date_id "
        f"from {staging_table} st "
        "inner join dim_customer on "
        "cast(st.customer_id as bigint) = dim_customer.customer_id "
        "inner join dim_calendar on "
        "cast(st.transaction_date as date) = dim_calendar.date "
        "inner join dim_currency on "
        "st.currency = dim_currency.currency_code "
        "where st.error_message is null"
    )

    extra_sqls = [
        (
            "insert into "
            "map_country_currency (country_id, "
            "currency_id) "
            "select distinct dc.country_id, "
            "ft.currency_id from "
            "dim_customer dc "
            "inner join fact_transaction ft on "
            "dc.customer_id = ft.customer_id "
            "where ft.transaction_type = 0"
        ),
    ]
