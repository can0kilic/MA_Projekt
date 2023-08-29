import csv
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

url = "https://boris.unibe.ch/view/contributors_bern/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
table = soup.find("table", class_="ep_view_cols ep_view_cols_3")
data = []
for row in tqdm(table.find_all("li")):
    link = row.a
    if link:
        link_text = link.get_text(strip=True)
        link_href = link["href"]
        data.append((link_text, link_href))

csv_file = "scraped_data.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Text", "Href"])
    writer.writerows(data)

print(f"Scraped data has been saved to {csv_file}")
