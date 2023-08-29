import pandas as pd

# Load the CSV files into dataframes
csv1_path = 'final_cleaned.csv'
csv2_path = 'parsed_names/parsed_data_cleaned.csv'

df1 = pd.read_csv(csv1_path, usecols=['first_name', 'last_name', 'institute', 'href', 'text', 'email','job_role'])
df2 = pd.read_csv(csv2_path, usecols=['first_name', 'middle_name', 'last_name', 'institute', 'raw_name','email','job_role'])

# Create a new dataframe for filtered entries from df2
filtered_entries = []

for _, row2 in df2.iterrows():
    match = df1[(df1['first_name'] == row2['first_name']) & (df1['last_name'] == row2['last_name'])]
    if match.empty:
        filtered_entries.append(row2)

# Create a new dataframe from the filtered entries
filtered_df = pd.DataFrame(filtered_entries)

# Save the filtered dataframe to a new CSV
filtered_csv_path = 'fail1.csv'
filtered_df.to_csv(filtered_csv_path, index=False)

print(f"Filtered entries saved to {filtered_csv_path}")
