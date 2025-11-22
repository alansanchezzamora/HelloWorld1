import boto3
from botocore.exceptions import NoCredentialsError, ClientError

"""
Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python, 
which allows Python developers to write software that makes use of services like Amazon S3 and Amazon EC2
"""

# Create S3 client
s3 = boto3.client("s3")

# Define Variables
bucket_name = "mi-bucket-de-prueba-alan123"
files_to_upload = [
    {
        "local_path": "data/aws_cloud_costs_1000.json",
        "s3_key": "aws_cloud_costs_1000.json",
    },
    {"local_path": "data/aws_accounts.json", "s3_key": "aws_accounts.json"},
]


# Upload File
def upload_file(file_path, bucket, object_name):
    """Sube un archivo a un bucket de S3"""
    try:
        s3.upload_file(file_path, bucket, object_name)
        print(f"Uploaded '{object_name}' to bucket '{bucket}'.")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except NoCredentialsError:
        print("AWS credentials not configured.")
    except ClientError as e:
        print(f"Error uploading {object_name}: {e}")


def main():
    print("Uploading datasets to S3...")
    for f in files_to_upload:
        upload_file(f["local_path"], bucket_name, f["s3_key"])
    print("All uploads completed successfully.")


if __name__ == "__main__":
    main()
