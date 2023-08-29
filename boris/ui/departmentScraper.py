import csv
import requests
from bs4 import BeautifulSoup

url = "https://www.unibe.ch/facultiesinstitutes/index_eng.html"

response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, "html.parser")
h4_tags = soup.find_all("h4")
extracted_text = [tag.get_text() for tag in h4_tags]

csv_filename = "derpatment_names.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Extracted Text"])
    for text in extracted_text:
        csv_writer.writerow([text])

print(f"Extracted {len(extracted_text)} items and saved to '{csv_filename}'.")
