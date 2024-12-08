import pandas as pd
import json

# Step 1: Load the JSON file
with open("airbnb_node_mapping.json", "r") as file:
    json_data = json.load(file)

# Step 2: Convert JSON to a pandas DataFrame
df = pd.DataFrame(json_data)

# Step 3: Save as a CSV file
df.to_csv("airbnb_node_mapping.csv", index=False)

# # Step 4: (Optional) Save as an Excel file
# df.to_excel("airbnb_node_mapping.xlsx", index=False)