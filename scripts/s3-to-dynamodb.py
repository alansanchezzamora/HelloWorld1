import boto3
import json
from botocore.exceptions import ClientError, NoCredentialsError

# CONFIG

BUCKET_NAME = "mi-bucket-de-prueba-alan123"
OBJECT_NAME = "aws_cloud_costs_1000.json"
TABLE_NAME = "AWS_Cloud_Costs"

# Add clientes
s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
dynamo_client = boto3.client("dynamodb")


"""
STEP 1 : DOWNLOAD JSON FROM S3
"""


def download_json_from_s3(bucket, object_name, local_path="temp_download.json"):
    print(f"Downloading {object_name} from {bucket}...")
    s3.download_file(bucket, object_name, local_path)
    with open(local_path, "r") as f:
        data = json.load(f)
    print(f"data loaded {len(data)} records from file")
    return data


"""
STEP 2 : CREATE DYNAMODB TABLE
"""


def create_dynamodb_table():
    tables = dynamo_client.list_tables()["TableNames"]
    if TABLE_NAME in tables:
        print(f"{TABLE_NAME} already exist")
        return dynamodb.Table(TABLE_NAME)

    print(f"Creating {TABLE_NAME}...")
    table = dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[{"AttributeName": "RecordID", "KeyType": "HASH"}],  # Partition key
        AttributeDefinitions=[
            {"AttributeName": "RecordID", "AttributeType": "S"}  # S = String
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )

    table.wait_until_exists()
    print("Table created successfully")
    return table


"""
STEP 3 : INSERT DATA
"""


def insert_data(table, records):
    print("Inserting data")
    count = 0
    for record in records:
        item = {k: str(v) for k, v in record.items()}
        table.put_item(Item=item)
        count += 1
    print(f"{count} records added on DynamoDB")


"""
PIPELINE
"""


def main():
    print("Starting pipeline s3 -> DynamoDB")
    records = download_json_from_s3(BUCKET_NAME, OBJECT_NAME)
    table = create_dynamodb_table()
    insert_data(table, records)
    print("Pipeline completed successfully. ")


if __name__ == "__main__":
    main()
