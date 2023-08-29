import pandas as pd

csv_path = 'parsed_data.csv'
df = pd.read_csv(csv_path)
df_unique = df.drop_duplicates(subset=['first_name', 'last_name'])
unique_csv_path = 'parsed_data_cleaned.csv'
df_unique.to_csv(unique_csv_path, index=False)

print(f"Unique entries saved to {unique_csv_path}")
