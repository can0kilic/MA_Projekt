import pandas as pd

input_filename = 'publicationRecord.csv'
output_filename = 'modified_publicationRecord_with_institute.csv'
data = pd.read_csv(input_filename)
data['full_text_status'] = data['full_text_status'].apply(lambda status: 'open' if status == 'public' else 'closed')
data.to_csv(output_filename, index=False)

print(f"Modified data saved to {output_filename}")
