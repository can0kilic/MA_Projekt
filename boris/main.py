import pandas as pd
from tqdm import tqdm

# Paths to CSV files
csv1_path = "parsed_names/parsed_names.csv"
csv2_path = "parsed_names/parsed_data_cleaned.csv"

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
    
    try:
        # Check if both first_name and last_name are present in respective columns of CSV1
        matching_rows = df1[
            (df1['first'].str.contains(first_name, case=False, na=False)) &
            (df1['last'].str.contains(last_name, case=False, na=False))
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
                    'job_role': jd
                })
        else:
            fail_data.append(row2)
    except Exception as e:
        print(f"Error processing row: {row2}, Error: {e}")

# Create DataFrames for final and failed results
final_df = pd.DataFrame(final_data)
fail_df = pd.DataFrame(fail_data)

# Save final and failed results to CSV files
final_csv_path = "final.csv"
final_df.to_csv(final_csv_path, index=False)

print("cleaning_file")

final_csv_path = "final.csv"


final_df = pd.read_csv(final_csv_path)
final_df_cleaned = final_df.drop_duplicates(subset=['first_name', 'last_name'])
final_cleaned_csv_path = "final_cleaned.csv"
final_df_cleaned.to_csv(final_cleaned_csv_path, index=False)

print("all done check final.csv and final_cleaned.csv")
