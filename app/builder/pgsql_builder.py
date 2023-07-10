from builder.base_builder import BaseBuilder
from commons.helpers import (
    copy_csv_to_table,
    mark_duplicate,
    mark_invalid_values,
    mark_length_gt,
    mark_non_decimal,
    mark_non_integer,
    replace_text,
    truncate_table,
)


class PgSQLBuilder(BaseBuilder):
    def build_staging(self):
        self.pipeline.add(
            copy_csv_to_table(
                self.staging_table, self.staging_fields, self.filepath
            )
        )

    def build_dedup(self):
        for column, alias in self.replace_aliases.items():
            for each_alias in alias["aliases"]:
                self.pipeline.add(
                    replace_text(
                        self.staging_table,
                        column,
                        new_name=alias["name"],
                        old_name=each_alias,
                    )
                )
        if self.unique_field:
            self.pipeline.add(
                mark_duplicate(self.staging_table, self.unique_field)
            )

    def build_checks(self):
        if self.integer_fields:
            self._build_check_for_integer_fields()
        if self.decimal_fields:
            self._build_check_for_decimal_fields()
        if self.max_length_fields:
            self._build_check_for_max_length_fields()
        if self.allowed_field_values:
            self._build_check_for_allowed_field_values()

    def build_cleanup(self):
        self.pipeline.add(truncate_table(self.staging_table))

    def _build_check_for_decimal_fields(self):
        for field in self.decimal_fields:
            self.pipeline.add(mark_non_decimal(self.staging_table, field))

    def _build_check_for_integer_fields(self):
        for field in self.integer_fields:
            self.pipeline.add(mark_non_integer(self.staging_table, field))

    def _build_check_for_max_length_fields(self):
        for field, value in self.max_length_fields.items():
            self.pipeline.add(mark_length_gt(self.staging_table, field, value))

    def _build_check_for_allowed_field_values(self):
        for field, values in self.allowed_field_values.items():
            self.pipeline.add(
                mark_invalid_values(self.staging_table, field, values)
            )
