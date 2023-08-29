# import requests
# import pandas as pd
# from tqdm import tqdm

# def fetch_uri(href):
#     endpoint = f"https://boris.unibe.ch/cgi/exportview/contributors_bern/{href}/JSON/{href}.js"
#     response = requests.get(endpoint)
#     if response.status_code == 200:
#         data = response.json()
#         uris = [item.get("uri") for item in data]
#         return uris
#     else:
#         return []

# def main():
#     input_csv = "resultDbMain.csv"
#     output_csv = "uri2.csv"

#     df = pd.read_csv(input_csv)
#     href_list = df["href"].tolist()

#     unique_uris = set()
#     for href in tqdm(href_list, desc="Fetching URIs"):
#         name = href.replace(".html", "")
#         uris = fetch_uri(name)
#         unique_uris.update(uris)

#     uri_df = pd.DataFrame({"uri": list(unique_uris)})
#     uri_df.to_csv(output_csv, index=False)
#     print(f"Unique URIs saved to {output_csv}")

# if __name__ == "__main__":
#     main()


# import requests
# import pandas as pd
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from tqdm import tqdm

# MAX_THREADS = 20

# def fetch_uri(href):
#     endpoint = f"https://boris.unibe.ch/cgi/exportview/contributors_bern/{href}/JSON/{href}.js"
#     response = requests.get(endpoint)
#     if response.status_code == 200:
#         data = response.json()
#         uris = [item.get("uri") for item in data]
#         return uris
#     else:
#         return []

# def main():
#     input_csv = "resultDbMain.csv"
#     output_csv = "uri.csv"

#     df = pd.read_csv(input_csv)
#     href_list = df["href"].tolist()

#     unique_uris = set()

#     with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
#         futures = [executor.submit(fetch_uri, href.replace(".html", "")) for href in href_list]

#         for future in tqdm(as_completed(futures), total=len(futures), desc="Fetching URIs"):
#             uris = future.result()
#             unique_uris.update(uris)

#     uri_df = pd.DataFrame({"uri": list(unique_uris)})
#     uri_df.to_csv(output_csv, index=False)
#     print(f"Unique URIs saved to {output_csv}")

# if __name__ == "__main__":
#     main()

import requests
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def fetch_uri(href):
    endpoint = f"https://boris.unibe.ch/cgi/exportview/contributors_bern/{href}/JSON/{href}.js"
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        uris = [item.get("uri") for item in data]
        return uris
    else:
        return []

def process_institute(href, institute):
    uris = fetch_uri(href.replace(".html", ""))
    result = [{"uri": uri, "institute": institute} for uri in uris]
    return result

def main():
    input_csv = "resultDbMain.csv"
    output_csv = "uri.csv"

    df = pd.read_csv(input_csv)
    href_list = df["href"].tolist()
    institute_list = df["institute"].tolist()

    unique_uris = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(tqdm(
            executor.map(process_institute, href_list, institute_list),
            total=len(href_list),
            desc="Fetching URIs"
        ))

    for result in results:
        unique_uris.extend(result)
    
    uri_df = pd.DataFrame(unique_uris)
    uri_df.to_csv(output_csv, index=False)
    print(f"URIs with institutes saved to {output_csv}")

if __name__ == "__main__":
    main()
