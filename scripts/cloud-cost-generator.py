import json
import uuid
import random
from datetime import datetime, timedelta


# Generate 1000 simulated AWS cloud cost records
def generate_cloud_cost_data(num_records=1000):
    services = [
        "Amazon EC2",
        "Amazon S3",
        "Amazon RDS",
        "AWS Lambda",
        "Amazon CloudFront",
        "Amazon DynamoDB",
        "Amazon SageMaker",
        "Amazon EKS",
        "Amazon Redshift",
        "AWS Glue",
    ]
    regions = ["us-east-1", "us-west-2", "eu-west-1", "ap-south-1"]

    data = []
    start_date = datetime(2024, 1, 1)

    for i in range(num_records):
        record = {
            "RecordID": str(uuid.uuid4()),
            "Service": random.choice(services),
            "Region": random.choice(regions),
            "Date": (start_date + timedelta(days=random.randint(0, 300))).strftime(
                "%Y-%m-%d"
            ),
            "Cost": round(random.uniform(0.1, 200.0), 2),
            "UsageHours": round(random.uniform(1, 720), 2),
        }
        data.append(record)

    return data


# Save the generated data to JSON file
output_path = "C:/Users/karin/OneDrive/Documentos/BYU-I Alan/CSE310/HelloWorld1/data/aws_cloud_costs_1000.json"
records = generate_cloud_cost_data(1000)
with open(output_path, "w") as f:
    json.dump(records, f, indent=4)

print(f"✅ Generated {len(records)} simulated cloud cost records at {output_path}")
