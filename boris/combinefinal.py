import pandas as pd

# Load the CSV files into dataframes
csv1_path = 'final_cleaned.csv'
csv2_path = 'final2_cleaned.csv'
csv3_path =  'final3_cleaned.csv'

df1 = pd.read_csv(csv1_path)
df2 = pd.read_csv(csv2_path)
df3 = pd.read_csv(csv3_path)

# Combine the dataframes
combined_df = pd.concat([df1, df2, df3])

# Save the combined dataframe to a new CSV
combined_csv_path = 'resultDbMain.csv'
combined_df.to_csv(combined_csv_path, index=False)

print(f"Combined data saved to {combined_csv_path}")
