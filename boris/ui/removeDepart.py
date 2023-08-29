import pandas as pd

department_names_df = pd.read_csv('derpatment_names.csv')
publication_record_df = pd.read_csv('modified_publicationRecord_with_institute.csv')
department_names_set = set(department_names_df['Extracted Text'])
filtered_publication_record_df = publication_record_df[~publication_record_df['institute'].isin(department_names_set)]
filtered_publication_record_df.to_csv('modified_publicationRecord_with_institute_no_depart.csv', index=False)
