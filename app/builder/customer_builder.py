from builder.pgsql_builder import PgSQLBuilder
from commons.models import StagingCustomer


class CustomerBuilder(PgSQLBuilder):
    staging_table = StagingCustomer.NAME
    staging_fields = StagingCustomer.COLUMNS
    unique_field = StagingCustomer.customer_id
    integer_fields = [
        StagingCustomer.customer_age,
    ]
    max_length_fields = {
        StagingCustomer.customer_gender: 10,
    }
    replace_aliases = {
        StagingCustomer.country: {
            "name": "USA",
            "aliases": [
                "United States",
            ],
        }
    }

    dimension_sqls = [
        (
            "INSERT INTO dim_country (country_name) "
            "SELECT DISTINCT sc.country "
            f"FROM {staging_table}  sc "
            "WHERE NOT EXISTS ( "
            "SELECT 1 "
            "FROM dim_country dc "
            "WHERE dc.country_name = sc.country"
            ") and sc.error_message is null"
        ),
    ]
    target_sql = (
        "insert "
        "into "
        "dim_customer (customer_id, "
        "country_id, "
        "customer_age, "
        "customer_gender) "
        "select "
        f"sc.{StagingCustomer.customer_id}, "
        "dc.country_id, "
        "cast(sc.customer_age as int)"
        f", sc.{StagingCustomer.customer_gender} "
        "from "
        f"{staging_table} sc "
        "inner join dim_country dc on "
        f"sc.{StagingCustomer.country} = dc.country_name "
        "where "
        f"sc.error_message is null"
    )
