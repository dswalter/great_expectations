---
title: How to configure an Expectation store to use Amazon S3
---
import Prerequisites from '../../connecting_to_your_data/components/prerequisites.jsx'


By default, newly profiled Expectations are stored in JSON format in the ``expectations/`` subdirectory of your ``great_expectations/`` folder.  This guide will help you configure Great Expectations to store them in an Amazon S3 bucket.

<Prerequisites>

- Configured a [Data Context](../../../tutorials/getting_started/initialize_a_data_context.md).
- Configured an [Expectations Suite](../../../tutorials/getting_started/create_your_first_expectations.md).
- Installed [boto3](https://github.com/boto/boto3) in your local environment.
- Identified the S3 bucket and prefix where Expectations will be stored.

</Prerequisites>

Steps
-----

1. **Configure** [boto3](https://github.com/boto/boto3) **to connect to the Amazon S3 bucket where Expectations will be stored.**

    Instructions on how to set up [boto3](https://github.com/boto/boto3) with AWS can be found at boto3's [documentation site](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html).

2. **Identify your Data Context Expectations Store**

    In your ``great_expectations.yml`` , look for the following lines.  The configuration tells Great Expectations to look for Expectations in a store called ``expectations_store``. The ``base_directory`` for ``expectations_store`` is set to ``expectations/`` by default.

    ```yaml
    expectations_store_name: expectations_store

    stores:
        expectations_store:
            class_name: ExpectationsStore
            store_backend:
                class_name: TupleFilesystemStoreBackend
                base_directory: expectations/
    ```


3. **Update your configuration file to include a new store for Expectations on S3.**

    In our case, the name is set to ``expectations_S3_store``, but it can be any name you like.  We also need to make some changes to the ``store_backend`` settings.  The ``class_name`` will be set to ``TupleS3StoreBackend``, ``bucket`` will be set to the address of your S3 bucket, and ``prefix`` will be set to the folder where Expectation files will be located.

    :::warning
    If you are also storing [Validations in S3](../configuring_metadata_stores/how_to_configure_a_validation_result_store_in_amazon_s3.md) or [DataDocs in S3](../configuring_data_docs/how_to_host_and_share_data_docs_on_amazon_s3.md),  please ensure that the ``prefix`` values are disjoint and one is not a substring of the other.
    :::

    ```yaml
    expectations_store_name: expectations_S3_store

    stores:
        expectations_S3_store:
            class_name: ExpectationsStore
            store_backend:
                class_name: TupleS3StoreBackend
                bucket: '<your_s3_bucket_name>'
                prefix: '<your_s3_bucket_folder_name>'
    ```


4. **Copy existing Expectation JSON files to the S3 bucket**. (This step is optional).

    One way to copy Expectations into Amazon S3 is by using the ``aws s3 sync`` command.  As mentioned earlier, the ``base_directory`` is set to ``expectations/`` by default. In the example below, two Expectations, ``exp1`` and ``exp2`` are copied to Amazon S3.  Your output should looks something like this:

    ```bash
    aws s3 sync '<base_directory>' s3://'<your_s3_bucket_name>'/'<your_s3_bucket_folder_name>'

    upload: ./exp1.json to s3://'<your_s3_bucket_name>'/'<your_s3_bucket_folder_name>'/exp1.json
    upload: ./exp2.json to s3://'<your_s3_bucket_name>'/'<your_s3_bucket_folder_name>'/exp2.json
    ```


5. **Confirm that the new Expectations store has been added by running** ``great_expectations --v3-api store list``.

    Notice the output contains two Expectation stores: the original ``expectations_store`` on the local filesystem and the ``expectations_S3_store`` we just configured.  This is ok, since Great Expectations will look for Expectations in the S3 bucket as long as we set the ``expectations_name`` variable to ``expectations_S3_store``.

    ```bash
    great_expectations --v3-api store list

    - name: expectations_store
    class_name: ExpectationsStore
    store_backend:
        class_name: TupleFilesystemStoreBackend
        base_directory: expectations/

    - name: expectations_S3_store
    class_name: ExpectationsStore
    store_backend:
        class_name: TupleS3StoreBackend
        bucket: '<your_s3_bucket_name>'
        prefix: '<your_s3_bucket_folder_name>'
    ```


6. **Confirm that Expectations can be accessed from Amazon S3 by running** ``great_expectations --v3-api suite list``.

    If you followed Step 4, The output should include the 2 Expectations we copied to Amazon S3: ``exp1`` and ``exp2``.  If you did not copy Expectations to the new Store, you will see a message saying no expectations were found.

    ```bash
    great_expectations --v3-api suite list

    2 Expectation Suites found:
     - exp1
     - exp2
    ```

If it would be useful to you, please comment with a +1 and feel free to add any suggestions or questions below.  Also, please reach out to us on [Slack](https://greatexpectations.io/slack) if you would like to learn more, or have any questions.
