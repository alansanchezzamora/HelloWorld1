import pandas as pd

df = pd.read_json("data/aws_cloud_costs_1000.json")

print(df.columns)
