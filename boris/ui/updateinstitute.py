import pandas as pd
import requests
from bs4 import BeautifulSoup

def extract_division_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    division_text = soup.find('h1', class_='pageTitle').text
    print(division_text.split('>')[1:])
    return division_text.split('>')[1:]

def process_division_text(text_list, institute_term):
    result = []
    for text in text_list:
        if institute_term in text:
            result.append(text.strip())
        else:
            split_text = text.strip().split()
            if len(split_text) >= 2:
                result.append(split_text[-2])
            else:
                result.append(split_text[-1])
    return result

def main():
    csv_file = "modified_publicationRecord_with_institute.csv"
    institute_term = "institute"  # Term to check in division text

   
    df = pd.read_csv(csv_file)

    division_terms = df['divisions'].unique()  

    result_list = []
    for division in division_terms:
        division_url = f"https://boris.unibe.ch/view/divisions/{division}.html"
        print(division_url)
        division_text_list = extract_division_text(division_url)
        processed_text_list = process_division_text(division_text_list, institute_term)
        result_list.append([division, processed_text_list])

    print(result_list)

if __name__ == "__main__":
    main()
