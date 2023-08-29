import pandas as pd
from tqdm import tqdm

# Paths to CSV files
csv1_path = "parsed_names/parsed_names.csv"
csv2_path = "customparsednames.csv"

# Load CSV files into DataFrames
df1 = pd.read_csv(csv1_path)
df2 = pd.read_csv(csv2_path)

# Create new DataFrames for successful matches and failed matches
final_data = []
fail_data = []

# Iterate through each row in CSV2 and check for matches in CSV1
for _, row2 in tqdm(df2.iterrows(), total=len(df2), desc="Processing CSV2"):
    first_name = row2['first_name']
    last_name = row2['last_name']
    institute = row2['institute']
    email = row2['email']
    jd = row2['job_role']
    raw_name = row2['raw_name']
    
    try:
        # Check if both first_name and last_name are present in respective columns of CSV1
        matching_rows = df1[
            (df1['first'].str.lower().str.contains(first_name, case=False, na=False)) &
            (df1['last'].str.lower().str.contains(last_name, case=False, na=False))
        ]

        if not matching_rows.empty:
            for _, matching_row in matching_rows.iterrows():
                final_data.append({
                    'first_name': first_name,
                    'last_name': last_name,
                    'institute': institute,
                    'href': matching_row['href'],
                    'text': matching_row['text'],
                    'email' : email,
                    'job_role': jd,
                    'raw_name': raw_name
                })
        else:
            fail_data.append(row2)
    except Exception as e:
        print(f"Error processing row: {row2}, Error: {e}")

# Create DataFrames for final and failed results
final_df = pd.DataFrame(final_data)
fail_df = pd.DataFrame(fail_data)

# Save final and failed results to CSV files
final_csv_path = "final3.csv"
final_df.to_csv(final_csv_path, index=False)

print("cleaning_file")

final_csv_path = "final3.csv"


final_df = pd.read_csv(final_csv_path)
final_df_cleaned = final_df.drop_duplicates(subset=['first_name', 'last_name'])
final_cleaned_csv_path = "final3_cleaned.csv"
final_df_cleaned.to_csv(final_cleaned_csv_path, index=False)

print("all done check final.csv and final_cleaned.csv")

# =============================================================================



# Load the CSV files into dataframes
csv1_path = 'final3_cleaned.csv'
csv2_path = 'fail2.csv'

df1 = pd.read_csv(csv1_path, usecols=['first_name', 'last_name', 'institute', 'href', 'text', 'email','job_role','raw_name'])
df2 = pd.read_csv(csv2_path, usecols=['first_name', 'middle_name', 'last_name', 'institute', 'raw_name','email','job_role'])

# Create a new dataframe for filtered entries from df2
filtered_entries = []

for _, row2 in df2.iterrows():
    match = df1[(df1['email'] == row2['email'])]
    if match.empty:
        row2["first_name"] = df1['first_name']
        row2["last_name"] = df1['last_name']
        filtered_entries.append(row2)

# Create a new dataframe from the filtered entries
filtered_df = pd.DataFrame(filtered_entries)

# Save the filtered dataframe to a new CSV
filtered_csv_path = 'fail3.csv'
filtered_df.to_csv(filtered_csv_path, index=False)

print(f"Filtered entries saved to {filtered_csv_path}")
