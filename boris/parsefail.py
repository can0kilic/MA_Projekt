import pandas as pd

# Load the CSV file into a dataframe
csv_path = 'fail1.csv'
df = pd.read_csv(csv_path)

df['first_name'] = df['email'].str.split('.').str[0]
# df['last_name'] = df['email'].str.split('.').str[1]
# df['last_name'] = df['last_name'].str.split('@')[0]
df['last_name'] = df['email'].str.split('.').str[1].str.split('@').str[0]

new_csv_path = 'emailtoname.csv'
df.to_csv(new_csv_path, index=False)

print(f"New CSV saved as {new_csv_path}")
