import boto3
from boto3.dynamodb.conditions import Attr

# -------------------------------------------------
# Initialize DynamoDB and reference both tables
# -------------------------------------------------

dynamodb = boto3.resource("dynamodb")

accounts_table = dynamodb.Table("AWS_Accounts")
costs_table = dynamodb.Table("AWS_Cloud_Costs")


# -------------------------------------------------
# CRUD for AWS_Accounts table
# -------------------------------------------------


def create_account(account_id, account_name, owner_email):
    item = {
        "account_id": account_id,
        "account_name": account_name,
        "owner_email": owner_email,
    }
    accounts_table.put_item(Item=item)
    print(f"Account {account_id} added successfully.")


def get_account(account_id):
    response = accounts_table.get_item(Key={"account_id": account_id})
    return response.get("Item")


def update_account(account_id, new_name=None, new_email=None):
    update_expr = []
    expr_attr_values = {}

    if new_name:
        update_expr.append("account_name = :n")
        expr_attr_values[":n"] = new_name
    if new_email:
        update_expr.append("owner_email = :e")
        expr_attr_values[":e"] = new_email

    if not update_expr:
        print("Nothing to update.")
        return

    accounts_table.update_item(
        Key={"account_id": account_id},
        UpdateExpression="SET " + ", ".join(update_expr),
        ExpressionAttributeValues=expr_attr_values,
    )
    print(f"Account {account_id} updated successfully.")


def delete_account(account_id):
    accounts_table.delete_item(Key={"account_id": account_id})
    print(f"Account {account_id} deleted successfully.")


def list_all_accounts():
    response = accounts_table.scan()
    return response.get("Items", [])


# -------------------------------------------------
# CRUD for AWS_Cloud_Costs table
# -------------------------------------------------


def create_cost(record_id, account_id, service, region, date, cost, usage_hours):
    item = {
        "RecordID": record_id,
        "account_id": account_id,
        "Service": service,
        "Region": region,
        "Date": date,
        "Cost": str(cost),
        "UsageHours": str(usage_hours),
    }
    costs_table.put_item(Item=item)
    print(f"Cost record {record_id} added successfully.")


def get_cost(record_id):
    response = costs_table.get_item(Key={"RecordID": record_id})
    return response.get("Item")


def list_costs_by_account(account_id):
    response = costs_table.scan(FilterExpression=Attr("account_id").eq(account_id))
    return response.get("Items", [])


def delete_cost(record_id):
    costs_table.delete_item(Key={"RecordID": record_id})
    print(f"Cost record {record_id} deleted successfully.")


def list_all_costs():
    response = costs_table.scan()
    return response.get("Items", [])


# -------------------------------------------------
# Optional manual test section
# -------------------------------------------------

if __name__ == "__main__":
    print("📌 Running manual tests...")
    print(list_all_accounts())
