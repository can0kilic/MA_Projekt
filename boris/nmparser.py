import csv
from nameparser import HumanName

def parse_csv_to_name_dicts(csv_file):
    name_dict_list = []

    with open(csv_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            text = row["Text"]
            href = row["Href"]

            # Parse the name using name-parser
            parsed_name = HumanName(text)

            # Create a name dictionary without "suffix"
            name_dict = {
                "first": parsed_name.first,
                "middle": parsed_name.middle,
                "last": parsed_name.last,
                "href": href,
                "text": text
            }

            name_dict_list.append(name_dict)

    return name_dict_list

def write_parsed_data_to_csv(parsed_data, output_csv_file):
    with open(output_csv_file, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["first", "middle", "last", "href","text"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(parsed_data)

csv_file = "scraped_data.csv"
parsed_names = parse_csv_to_name_dicts(csv_file)

for name_dict in parsed_names:
    print(name_dict)
    print("-" * 30)

output_csv_file = "parsed_names.csv"
write_parsed_data_to_csv(parsed_names, output_csv_file)

print(f"Parsed data has been saved to {output_csv_file}")
