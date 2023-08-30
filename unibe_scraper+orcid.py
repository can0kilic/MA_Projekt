import csv
import requests
from bs4 import BeautifulSoup


# URL der Webseite, die gescraped werden soll
url = "https://www.unibe.ch/facultiesinstitutes/index_eng.html"

# Führe eine GET-Anfrage durch, um den Inhalt der Webseite abzurufen
response = requests.get(url)

# Parse den Inhalt mit BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Suche nach dem speziellen Abschnitt auf der Seite, der die gewünschten Links enthält
section = soup.find('section', class_='list-orgs')

# Suche nach allen Links innerhalb dieses Abschnitts
anchor_tags = section.find_all('a')

# Speichere die gefundenen Links und deren Text in einer Liste
links = []
for anchor_tag in anchor_tags:
    try:
        href = anchor_tag.get('href')
        if href != '#':
            text = anchor_tag.get_text()
            if not text.lower() == 'homepage faculty':
                links.append([href, text])
    except:
        pass

# Speichere die gefundenen Links und deren Text in einer Liste
with open('links.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['URL', 'Text'])
    writer.writerows(links)

print("Links saved to links.csv")




# Scraper für "Über uns"-Seiten und Abteilungen

import csv
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

links = open("links.csv", "r")
aboutus = open("about_us_page.csv", "w")

links_reader = csv.reader(links)
links_writer = csv.writer(aboutus)



def extract_last_li_href(url):
    d = []  # Liste zum Speichern von Abteilungs-URLs
    try:
        response = requests.get(url)  # Fordere die Webseite an
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Versuche, alle Abteilungen (departments) aus der Seite zu extrahieren
        try:
            departments = soup.find_all('li', class_ = 'list-group-item')
            for dep_home in departments:
                achr = dep_home.find('a')  # Finde den Link für jede Abteilung
                dep_url = achr["href"]
                d.append(dep_url)  # Füge die Abteilungs-URL der Liste hinzu
        except:
            pass
        
        # Extrahiere den Link im letzten "li"-Tag des "ul"-Elements mit der Klasse 'level-1'
        ul = soup.find('ul', class_='level-1')
        li_tags = ul.find_all('li')
        last_li = li_tags[-1]
        anchor = last_li.find('a')
        href = anchor['href']
        return (href,d)  # Gib den Link aus dem letzten "li"-Tag und die Liste der Abteilungs-URLs zurück
    except:
        return None

# Zähle die gesamte Anzahl von URLs
total_urls = sum(1 for _ in links_reader)  

# Setze den Dateizeiger auf den Anfang der Datei zurück
links.seek(0)

fetched = []  # Liste zum Speichern der extrahierten Haupt-URLs
fetched_2 =[]  # Liste zum Speichern der Abteilungs-URLs
x = []  # Zwischenliste

# Gehe durch alle Links und extrahiere Informationen mit extract_last_li_href
for data in tqdm(links_reader, total=total_urls, desc="Processing URLs", unit="URL"):
    url = data[0]
    text = data[1]
    new_url = extract_last_li_href(url)
    if new_url != None:
        dep = new_url[1]
        if dep != []:
            for dep_url in dep:
                x.append([dep_url, text])
        fetched.append([new_url[0], text])
    else:
        pass

print("scrapping departments please wait a while....")

# Gehe durch die Zwischenliste x und extrahiere weitere Informationen
temp = 0
for i in x:
    temp += 1
    t = i[1]
    u = i[0]
    data_dep = extract_last_li_href(u)
    if data_dep:
        fetched_2.append([data_dep[0], t])
    print(f"processing...   [{(temp/len(x))*100}%] @ working on [{temp}] remaning [{len(x)-temp}]")

# Schreibe die extrahierten URLs in die CSV-Datei
links_writer.writerows(fetched)
links_writer.writerows(fetched_2)

# Schließt die CSV-Dateien
aboutus.close()
links.close()


import spacy

def extract_user_data(url):
    """
    Extrahiert Benutzerdaten aus einer bestimmten URL
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        ul_element = soup.find("ul", class_="level-2 open")
        data = []

        li_elements = ul_element.find_all("li")

        # Für jedes "li"-Element in der Liste
        for li in li_elements:
            anchor = li.find("a")
            href = anchor["href"]
            text = anchor.get_text(strip=True)

            # Spezielle Behandlung für Seiten mit "about us" oder ähnlichem
            if text == "about us" or text == "über uns" or text == "À notre propos":
                about_us_response = requests.get(href)
                about_us_soup = BeautifulSoup(about_us_response.content, "html.parser")
                dl_elements = about_us_soup.find_all("dl", class_="left")
                for dl in dl_elements:
                    name = dl.find_all("dd").get_text(strip=True)

                    # Extrahiere die Job-Bezeichnung und E-Mail, falls vorhanden
                    job_title_element = dl.find("dd", class_="jobTitle")
                    job_role = job_title_element.get_text(strip=True) if job_title_element else ""
                    email_element = dl.find("dd", class_="mail")
                    email_address = email_element.get_text(strip=True) if email_element else ""

                    data.append([name, job_role, email_address])

            else:
                # Für alle anderen Seiten
                response = requests.get(href)
                soup = BeautifulSoup(response.content, "html.parser")
                dl_elements = soup.find_all("dl", class_="left")

                # Ähnlicher Extraktionsprozess wie oben
                for dl in dl_elements:
                    name = dl.find("dd").get_text(strip=True)
                    job_title_element = dl.find("dd", class_="jobTitle")
                    job_role = job_title_element.get_text(strip=True) if job_title_element else ""
                    email_element = dl.find("dd", class_="mail")
                    email_address = email_element.get_text(strip=True) if email_element else ""

                    data.append([name, job_role, email_address])

        return data

    except:
        return None


def process_name(name):
    """
    Verarbeitet einen Namen, indem unerwünschte Teile entfernt werden
    """
    name = name.lower()
    name = name.split(".")
    new_name = []
    ret_name = []

    for i in name:
        j = i.split(" ")
        for k in j:
            new_name.append(k)

    # Entfernt Titel und Leerzeichen aus dem Namen
    for i in new_name:
        if i != " " and i != "dr" and i != "vda" and i != "prof" and i != "m" and i != "pd" and len(i) > 2:
            ret_name.append(i)
    return ret_name

def filter_name(name):
    """
    Nutzt Spacy, um aus einem Text einen Personennamen zu extrahieren
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(name)

    for entity in doc.ents:
        if entity.label_ == "PERSON":
            t = entity.text
            t = t.split(" ")
            return t

def filter_email(email):
    """
    Trennt den Vornamen und Nachnamen aus einer E-Mail-Adresse
    """
    name_list = []
    if email:
        email = email.split("@")[0]
        name = email.split(".")
        first_name = name[0]
        last_name = name[-1]
        if first_name:
            name_list.append(first_name)
        if last_name:
            name_list.append(last_name)
    return name_list

def GetCredentialsFromORCID(f_name,g_name):
    """
    Ruft die ORCID-ID einer Person ab, basierend auf ihrem Vor- und Nachnamen
    """
    GREEN_BOLD = "\033[1;32m"
    RED_BOLD = "\033[1;31m"
    RESET = "\033[0m"

    try:
        # Anfrage an die ORCID-API
        response = requests.get(f'https://pub.orcid.org/v3.0/expanded-search/?start=0&rows=200&q=family-name:{f_name}+AND+given-names:{g_name}+AND+ringgold-org-id:27210',
                                headers={'User-Agent': 'Mozilla/5.0', 'accept': 'application/json'})
        data = response.json()
        if 'expanded-result' in data:
            results = data['expanded-result']
            for result in results:
                if 'given-names' in result and 'family-names' in result and 'orcid-id' in result:
                    given_names = result['given-names']
                    family_names = result['family-names']
                    orcid = result['orcid-id']
                    name = f"{given_names} {family_names}"
                    print(f"{GREEN_BOLD}Name: {name}  ORCID: {orcid}{RESET}")
                    return orcid
        else:
            print(f"{RED_BOLD}No results found for {g_name} {f_name}{RESET}")
            return None
    except Exception as e:
        print(f"{RED_BOLD}No results found for {g_name} {f_name}{RESET}")
        return None

import csv

# Farbcodes für die Terminalausgabe
YELLOW_BOLD = "\033[1;33m"
RESET = "\033[0m"

# Dateien öffnen
aboutus = open("about_us_page.csv", "r")
userinfo = open("userinfo.csv", "w")
user_without_orcid = open("userxorcid.csv", "w")

userxorcid = csv.writer(user_without_orcid)

reader = csv.reader(aboutus)

# Listen zur Speicherung von Daten
info_list = []
info_list_2 = []

# Durchgehen jeder Zeile in der CSV-Datei
for data in reader:
    url = data[0]
    text = data[1]

    l = extract_user_data(url)  # Daten von der URL extrahieren
    if l:
        for i in l:
            j = i
            i.append(text)
            try:
                fullname = i[0]
                email = i[2]
                print(f"{YELLOW_BOLD}scrapped name = {fullname}{RESET}")

                # Namen verarbeiten
                name = filter_name(fullname)  # mit Spacy
                name_bkup = process_name(fullname)  # benutzerdefinierte Methode
                name_email = filter_email(email)  # E-Mail verarbeiten

                # Erste Versuch, ORCID-Referenzen mithilfe des von Spacy verarbeiteten Namens zu erhalten
                first_name = name[0]
                last_name = name[-1]

                # ORCID-ID versuchen zu holen
                orcid = GetCredentialsFromORCID(last_name, first_name)

                if orcid:
                    i.append(orcid)
                    i.append(f"{first_name} {last_name}")
                    info_list.append(i)

                # Wenn der erste Versuch fehlschlägt, wird versucht, den benutzerdefinierten Namen zu verwenden
                else:
                    first_name_bkup = name_bkup[0]
                    last_name_bkup = name_bkup[-1]
                    orcid_bkup = GetCredentialsFromORCID(last_name_bkup, first_name_bkup)

                    if orcid_bkup:
                        i.append(orcid_bkup)
                        i.append(f"{first_name_bkup} {last_name_bkup}")
                        info_list.append(i)

                    # Falls beide Namensversuche fehlschlagen, wird der aus der E-Mail extrahierte Name verwendet
                    else:
                        if name_email != []:
                            first_name_email = name_email[0]
                            last_name_email = name_email[-1]
                            orcid_email = GetCredentialsFromORCID(last_name_email, first_name_email)

                            if orcid_email:
                                i.append(orcid_email)
                                i.append(f"{first_name_email} {last_name_email}")
                                info_list.append(i)
                            else:
                                # Nutzer hat keine ORCID-ID
                                j.append(f"{first_name_bkup} {last_name_bkup}")
                                j.append(f"{first_name} {last_name}")
                                j.append(text)
                                info_list_2.append(j)

                print("===" * 20)
            except Exception as e:
                print(e)

# Daten in CSV-Dateien schreiben
writer = csv.writer(userinfo)
writer.writerows(info_list)
userxorcid.writerows(info_list_2)

# Dateien schließen
user_without_orcid.close()
userinfo.close()
aboutus.close()

# Webseiten scrapen
import requests
from bs4 import BeautifulSoup

url = "https://www.geo.unibe.ch/about_us/the_institute/institute_members/index_eng.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Informationen von der Webseite extrahieren
team_boxes = soup.find_all('article', class_='team-box')
for box in team_boxes:
    dd_tags = box.find_all('dd')
    for dd in dd_tags:
        print(dd.get_text(strip=True))

import re
url = "https://www.geo.unibe.ch/ueber_uns/unser_institut/institutsmitglieder/index_ger.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# PHP-Links von der Webseite extrahieren
links = soup.find_all("a")
php_pattern = re.compile(r'\.php\b')
for link in links:
    href = link.get("href")
    if href and php_pattern.search(href):
        print(href)
