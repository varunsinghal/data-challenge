from typing import List


class StagingCustomer:
    customer_id: str = "customer_id"
    country: str = "country"
    customer_age: str = "customer_age"
    customer_gender: str = "customer_gender"

    # extras
    row_id: str = "row_id"
    error_field: str = "error_message"

    NAME: str = "staging_customer"
    COLUMNS: List[str] = [
        customer_id,
        country,
        customer_age,
        customer_gender,
    ]


class StagingTransaction:
    transaction_id: str = "transaction_id"
    customer_id: str = "customer_id"
    transaction_type: str = "transaction_type"
    amount: str = "amount"
    currency: str = "currency"
    transaction_date: str = "transaction_date"
    # extras
    row_id: str = "row_id"
    error_field: str = "error_message"

    NAME: str = "staging_transaction"
    COLUMNS: List[str] = [
        transaction_id,
        customer_id,
        transaction_type,
        amount,
        currency,
        transaction_date,
    ]


class StagingExchangeRate:
    exchange_rate_id: str = "exchange_rate_id"
    from_currency: str = "from_currency"
    to_currency: str = "to_currency"
    effective_date: str = "effective_date"
    rate: str = "rate"

    # extras
    row_id: str = "row_id"
    error_field: str = "error_message"

    NAME: str = "staging_exchange_rate"
    COLUMNS: List[str] = [
        exchange_rate_id,
        from_currency,
        to_currency,
        effective_date,
        rate,
    ]
