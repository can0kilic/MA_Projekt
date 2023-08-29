import csv
from nameparser import HumanName

def parse_name(name):
    parsed_name = HumanName(name)
    return {
        "first_name": parsed_name.first,
        "middle_name": parsed_name.middle,
        "last_name": parsed_name.last,
    }

def parse_userinfo_csv(csv_file):
    parsed_userinfo_list = []

    with open(csv_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            name_full = row["name_full"]
            email = row["email"]
            jd = row["job_role"]
            parsed_name_dict = parse_name(name_full)
            
            institute = row["institute"]

            parsed_userinfo = {
                **parsed_name_dict,
                "institute": institute,
                "raw_name": name_full,
                "email": email,
                "job_role": jd
            }

            parsed_userinfo_list.append(parsed_userinfo)

    return parsed_userinfo_list

def write_parsed_data_to_csv(parsed_data, output_csv_file):
    with open(output_csv_file, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["first_name", "middle_name", "last_name", "institute", "raw_name", "email","job_role"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(parsed_data)

userinfo_csv_file = "unibe_data.csv"
output_csv_file = "parsed_names/parsed_data.csv"

parsed_userinfo = parse_userinfo_csv(userinfo_csv_file)

# Print the list of dictionaries
for userinfo_dict in parsed_userinfo:
    print(userinfo_dict)
    print("-" * 30)

# Write parsed data to CSV
write_parsed_data_to_csv(parsed_userinfo, output_csv_file)

print(f"Parsed data has been saved to {output_csv_file}")
