import csv

def combine_csv_files(file1, file2, combined_file):
    with open(file1, "r", newline="", encoding="utf-8") as f1, \
            open(file2, "r", newline="", encoding="utf-8") as f2, \
            open(combined_file, "w", newline="", encoding="utf-8") as combined_f:
        reader1 = csv.reader(f1)
        header1 = next(reader1)
        reader2 = csv.reader(f2)
        next(reader2) 
        combined_writer = csv.writer(combined_f)
        new_header = ["name_full", "job_role", "email", "institute"]
        combined_writer.writerow(new_header)

        for row in reader1:
            combined_writer.writerow(row[:4])

        for row in reader2:
            combined_writer.writerow(row[:4])

# CSV file paths
file1 = "userinfo.csv"
file2 = "userxorcid.csv"
combined_file = "unibe_data.csv"

combine_csv_files(file1, file2, combined_file)

print(f"Combined data has been saved to {combined_file}")
