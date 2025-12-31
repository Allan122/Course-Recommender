import pandas as pd
import os

# Load the CSV
base_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(base_dir, "data", "courses.csv"))

# Print the column names
print("YOUR COLUMNS ARE:")
print(list(df.columns))