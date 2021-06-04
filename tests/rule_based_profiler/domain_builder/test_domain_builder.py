from typing import List

from great_expectations.core import IDDict
from great_expectations.core.batch import BatchDefinition
from great_expectations.rule_based_profiler.domain_builder import (
    ActiveBatchTableDomainBuilder,
    ColumnDomainBuilder,
    DomainBuilder,
)
from great_expectations.rule_based_profiler.domain_builder.domain import Domain
from great_expectations.self_check.util import build_pandas_validator_with_data
from great_expectations.validator.validator import Validator


# noinspection PyPep8Naming
def test_active_batch_table_domain_builder(
    two_column_pandas_test_df,
    table_Users_domain,
):
    batch_definition: BatchDefinition = BatchDefinition(
        datasource_name="my_datasource",
        data_connector_name="my_data_connector",
        data_asset_name="my_data_asset",
        batch_identifiers=IDDict({}),
    )

    validator: Validator = build_pandas_validator_with_data(
        df=two_column_pandas_test_df,
        batch_definition=batch_definition,
    )

    domain_builder: DomainBuilder = ActiveBatchTableDomainBuilder()
    domains: List[Domain] = domain_builder.get_domains(
        validator=validator,
    )

    assert len(domains) == 1
    assert domains == [
        {
            "domain_kwargs": {
                "batch_id": "f576df3a81c34925978336d530453bc4",
            },
        }
    ]

    domain: Domain = domains[0]
    # Assert Domain object equivalence.
    assert domain == table_Users_domain
    # Also test that the dot notation is supported properly throughout the dictionary fields of the Domain object.
    assert domain.domain_kwargs.batch_id == "f576df3a81c34925978336d530453bc4"


# noinspection PyPep8Naming
def test_column_domain_builder(
    two_column_pandas_test_df,
    column_Age_domain,
    column_Date_domain,
):
    batch_definition: BatchDefinition = BatchDefinition(
        datasource_name="my_datasource",
        data_connector_name="my_data_connector",
        data_asset_name="my_data_asset",
        batch_identifiers=IDDict({}),
    )

    validator: Validator = build_pandas_validator_with_data(
        df=two_column_pandas_test_df,
        batch_definition=batch_definition,
    )

    domain_builder: DomainBuilder = ColumnDomainBuilder()
    domains: List[Domain] = domain_builder.get_domains(
        validator=validator,
    )

    assert len(domains) == 2
    assert domains == [
        {
            "domain_kwargs": {
                "column": "Age",
                "batch_id": "f576df3a81c34925978336d530453bc4",
            },
        },
        {
            "domain_kwargs": {
                "column": "Date",
                "batch_id": "f576df3a81c34925978336d530453bc4",
            },
        },
    ]
    # Assert Domain object equivalence.
    domain: Domain
    domain = domains[0]
    assert domain == column_Age_domain
    domain = domains[1]
    assert domain == column_Date_domain
