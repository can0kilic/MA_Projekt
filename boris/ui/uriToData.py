# import requests
# import pandas as pd
# from concurrent.futures import ThreadPoolExecutor, as_completed

# MAX_THREADS = 100

# def fetch_boris_info(id):
#     endpoint = f"https://boris.unibe.ch/cgi/search/advanced/export_BORIS_JSON.js?screen=Search&_action_export=1&output=JSON&exp=0%7C1%7C-date%2Fcreators_name%2Ftitle%7Carchive%7C-%7Ceprintid%3Aeprintid%3AANY%3AEQ%3A{id}%7C-%7Ceprint_status%3Aeprint_status%3AANY%3AEQ%3Aarchive%7Cmetadata_visibility%3Ametadata_visibility%3AANY%3AEQ%3Ashow&n="
#     try:
#         response = requests.get(endpoint + str(id))
#         if response.status_code == 200:
#             data = response.json()
#             return data
#         else:
#             return []
#     except Exception as e:
#         print(f"Error fetching data for id {id}: {e}")
#         return []

# def process_uri(uri):
#     try:
#         id = uri.split("/")[-1]
#         boris_info = fetch_boris_info(id)

#         if boris_info:
#             retdata = {
#                 "uri": uri,
#                 "date": str(boris_info[0].get("date"))[:4],
#                 "creators": f"{boris_info[0]['creators'][0]['name']['given']} {boris_info[0]['creators'][0]['name']['family']}",
#                 "full_text_status": boris_info[0].get("full_text_status"),
#                 "title": boris_info[0]['title'][0]['text'],
#                 "divisions": boris_info[0].get("divisions", [])[0]
#             }
#             print(retdata)
#             return retdata
#     except Exception as e:
#         print(f"Error processing uri {uri}: {e}")
#         return None

# def main():
#     input_csv = "uri.csv"
#     output_csv = "publicationRecord.csv"

#     df = pd.read_csv(input_csv)
#     uri_list = df["uri"].tolist()

#     records = []

#     with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
#         futures = [executor.submit(process_uri, uri) for uri in uri_list]

#         for future in as_completed(futures):
#             record = future.result()
#             if record:
#                 records.append(record)

#     output_df = pd.DataFrame(records)
#     output_df.to_csv(output_csv, index=False)
#     print(f"Processed BORIS info saved to {output_csv}")

# if __name__ == "__main__":
#     main()

import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

MAX_THREADS = 100

def fetch_boris_info(id):
    endpoint = f"https://boris.unibe.ch/cgi/search/advanced/export_BORIS_JSON.js?screen=Search&_action_export=1&output=JSON&exp=0%7C1%7C-date%2Fcreators_name%2Ftitle%7Carchive%7C-%7Ceprintid%3Aeprintid%3AANY%3AEQ%3A{id}%7C-%7Ceprint_status%3Aeprint_status%3AANY%3AEQ%3Aarchive%7Cmetadata_visibility%3Ametadata_visibility%3AANY%3AEQ%3Ashow&n="
    try:
        response = requests.get(endpoint + str(id))
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return []
    except Exception as e:
        print(f"Error fetching data for id {id}: {e}")
        return []

def process_uri(uri, institute):
    try:
        id = uri.split("/")[-1]
        boris_info = fetch_boris_info(id)

        if boris_info:
            retdata = {
                "uri": uri,
                "institute": institute,
                "date": str(boris_info[0].get("date"))[:4],
                "creators": f"{boris_info[0]['creators'][0]['name']['given']} {boris_info[0]['creators'][0]['name']['family']}",
                "full_text_status": boris_info[0].get("full_text_status"),
                "title": boris_info[0]['title'][0]['text'],
                "divisions": boris_info[0].get("divisions", [])[0]
            }
            print(retdata)
            return retdata
    except Exception as e:
        print(f"Error processing uri {uri}: {e}")
        return None

def main():
    input_csv = "uri.csv"
    output_csv = "publicationRecord.csv"

    df = pd.read_csv(input_csv)
    uri_institute_pairs = df[["uri", "institute"]].values.tolist()

    records = []

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(process_uri, uri, institute) for uri, institute in uri_institute_pairs]

        for future in as_completed(futures):
            record = future.result()
            if record:
                records.append(record)

    output_df = pd.DataFrame(records)
    output_df.to_csv(output_csv, index=False)
    print(f"Processed BORIS info saved to {output_csv}")

if __name__ == "__main__":
    main()
