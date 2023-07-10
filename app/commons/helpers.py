from typing import List

ERROR_COLUMN = "error_message"
ROW_ID_COLUMN = "row_id"


def copy_csv_to_table(
    table_name: str, columns: List[str], filepath: str
) -> str:
    joined_columns = ", ".join(columns)
    return (
        f"copy {table_name} ({joined_columns}) "
        f"from '{filepath}'"
        "delimiter ','"
        "csv header"
    )


def replace_text(
    table_name: str, column: str, new_name: str, old_name: str
) -> str:
    return (
        f"update {table_name} "
        f"set {column} = REPLACE({column}, '{old_name}', '{new_name}')"
    )


def truncate_table(table_name: str) -> str:
    return f"truncate {table_name}"


def trim_whitespace(table_name: str, columns: List[str]) -> str:
    operations = ["{column} = trim({column})" for column in columns]
    joined_operations = ", ".join(operations)
    return f"update {table_name} set {joined_operations}"


def mark_duplicate(table_name: str, unique_column: str) -> str:
    return (
        f"update {table_name} set "
        f"{ERROR_COLUMN} = concat({ERROR_COLUMN}, 'Duplicate Record')"
        f"where {ROW_ID_COLUMN} in ( "
        f"select {ROW_ID_COLUMN} from ( "
        f"select {ROW_ID_COLUMN}, {unique_column}, "
        f"row_number() over (partition by {unique_column} "
        f"order by {unique_column}) as row_num "
        f"from {table_name}) as subquery where row_num > 1)"
    )


def mark_non_integer(table_name: str, column_name: str) -> str:
    return (
        f"update {table_name} "
        f"set {ERROR_COLUMN} = "
        f"concat({ERROR_COLUMN}, 'Non integer {column_name};')"
        f"where {column_name} ~ '[^0-9]'"
    )


def mark_non_decimal(table_name: str, column_name: str) -> str:
    return (
        f"update {table_name} "
        f"set {ERROR_COLUMN} = "
        f"concat({ERROR_COLUMN}, 'Non decimal {column_name};')"
        rf"where {column_name} ~ '[^\-0-9.]'"
    )


def mark_length_gt(table_name: str, column_name: str, max_length: int) -> str:
    return (
        f"update {table_name} "
        f"set {ERROR_COLUMN} = concat("
        f"{ERROR_COLUMN}, 'Exceeded length {max_length} chars;') "
        f"where length({column_name}) > {max_length}"
    )


def mark_invalid_values(
    table_name: str, column_name: str, allowed_values: List[str]
):
    joined_values = "'" + "', '".join(allowed_values) + "'"
    return (
        f"update {table_name} "
        f"set {ERROR_COLUMN} = concat({ERROR_COLUMN}, 'Invalid {column_name}.')"
        f"where {column_name} not in ({joined_values})"
    )
