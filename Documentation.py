"""
Project Doucumentation: 

Step 1: Install AWS CLI
Open Command Prompt (CMD) and run:
pip install awscli

Step 2: Configure AWS Credentials
Run:
aws configure

Enter your credentials: (Credentials Found in AWS Security Credentials)
AWS Access Key ID [None]:  <your-access-key>
AWS Secret Access Key [None]:  <your-secret-key>
Default region name [None]:  us-east-1
Default output format [None]:  json

Confirm configuration with:
aws sts get-caller-identity

Step 3: Install boto3 for Python

Install the AWS SDK for Python:
pip install boto3

Step 4: Create an S3 Bucket

On CMD: 
aws s3 mb s3://mi-bucket-de-prueba-aws


"""