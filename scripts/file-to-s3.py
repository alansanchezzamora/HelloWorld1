import boto3

"""
Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python, 
which allows Python developers to write software that makes use of services like Amazon S3 and Amazon EC2
"""
# Create S3 client
s3 = boto3.client("s3")

# Define Variables
bucket_name = "mi-bucket-de-prueba-alan123"
file_path = "C:/Users/karin/OneDrive/Documentos/BYU-I Alan/CSE310/HelloWorld1/data/aws_cloud_costs_1000.json"
object_name = "aws_cloud_costs_1000.json"

# Upload File
try:
    """
    s3 Functions: upload_file(), download_file(), list_buckets(), delete_object()
    """
    s3.upload_file(file_path, bucket_name, object_name)
    print(f"File: '{object_name}' sucessfully uploaded to: '{bucket_name}'.")
except Exception as e:
    print(f"Failed to upload: {e}")
