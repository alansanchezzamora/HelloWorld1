import boto3
import json
from botocore.exceptions import ClientError, NoCredentialsError

# CONFIG

BUCKET_NAME = "sprint1-bucket"
ACCOUNTS_FILE = "aws_accounts.json"
COSTS_FILE = "aws_cloud_costs.json"
ACCOUNTS_TABLE = "AWS_Accounts"
COSTS_TABLE = "AWS_Cloud_Costs"

# Add clientes
s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
dynamo_client = boto3.client("dynamodb")


"""
STEP 1 : DOWNLOAD JSON FROM S3
"""


def download_json_from_s3(bucket, object_name, local_path="temp.json"):
    print(f"Downloading {object_name} from {bucket}...")
    s3.download_file(bucket, object_name, local_path)
    with open(local_path, "r") as f:
        data = json.load(f)
    print(f"Loaded {len(data)} records from {object_name}")
    return data


"""
STEP 2 : CREATE DYNAMODB TABLE
"""


def create_accounts_table():
    tables = dynamo_client.list_tables()["TableNames"]
    if ACCOUNTS_TABLE in tables:
        print(f"Table {ACCOUNTS_TABLE} already exists.")
        return dynamodb.Table(ACCOUNTS_TABLE)

    print(f"Creating {ACCOUNTS_TABLE}...")
    table = dynamodb.create_table(
        TableName=ACCOUNTS_TABLE,
        KeySchema=[{"AttributeName": "account_id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "account_id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    table.wait_until_exists()
    print(f"Table {ACCOUNTS_TABLE} created.")
    return table


def create_cloudcosts_table():
    tables = dynamo_client.list_tables()["TableNames"]
    if COSTS_TABLE in tables:
        print(f"Table {COSTS_TABLE} already exists.")
        return dynamodb.Table(COSTS_TABLE)

    print(f"Creating {COSTS_TABLE}...")
    table = dynamodb.create_table(
        TableName=COSTS_TABLE,
        KeySchema=[
            {"AttributeName": "RecordID", "KeyType": "HASH"},
            {"AttributeName": "account_id", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "RecordID", "AttributeType": "S"},
            {"AttributeName": "account_id", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    table.wait_until_exists()
    print(f"Table {COSTS_TABLE} created.")
    return table


"""
STEP 3 : INSERT DATA
"""


def insert_data(table, records, limit=20):
    print(f"Inserting data into {table.table_name}...")
    count = 0
    for record in records[:limit]:  # limit for testing
        item = {k: str(v) for k, v in record.items()}
        table.put_item(Item=item)
        count += 1
    print(f"{count} records inserted into {table.table_name}")


"""
PIPELINE
"""


def main():
    print("Starting pipeline S3 -> DynamoDB")

    # Download both JSON files
    accounts_data = download_json_from_s3(BUCKET_NAME, ACCOUNTS_FILE)
    cost_data = download_json_from_s3(BUCKET_NAME, COSTS_FILE)

    # Create both tables
    accounts_table = create_accounts_table()
    costs_table = create_cloudcosts_table()

    # Insert records
    insert_data(accounts_table, accounts_data)
    insert_data(costs_table, cost_data)

    print("Pipeline completed successfully!")


if __name__ == "__main__":
    main()
