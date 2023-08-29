import pandas as pd

# Load the CSV files
publication_df = pd.read_csv("publicationRecord.csv")
institute_df = pd.read_csv("li_tags_data.csv")

url_to_institute = {row["URL"]: row["Institute"] for _, row in institute_df.iterrows()}
publication_df["institute"] = publication_df["divisions"].map(url_to_institute)
publication_df.to_csv("publicationRecord_with_institute.csv", index=False)

print("Updated publicationRecord saved to publicationRecord_with_institute.csv")
