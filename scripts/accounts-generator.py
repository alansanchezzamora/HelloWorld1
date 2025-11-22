import json
import random

# Random Account Names
account_names = ["Prod", "Dev", "Test", "Analytics", "Alan"]
domains = ["example.com", "company.com", "demo.com"]

# Simulated accounts
accounts = []
for i in range(1, 6):
    account_id = [f"ACC{i:03}" for i in range(1, 6)]
    account_name = account_names[i - 1]
    owner_email = f"{account_name.lower()}@{random.choice(domains)}"

    accounts.append(
        {
            "account_id": account_id,
            "account_name": account_name,
            "owner_email": owner_email,
        }
    )

output_file = "data/aws_accounts.json"
with open(output_file, "w") as f:
    json.dump(accounts, f, indent=2)

print(f"Generated {len(accounts)} account records -> {output_file}")
