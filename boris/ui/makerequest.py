import requests

def get_document_info(boris_id):
    url = f"https://boris.unibe.ch/cgi/search/advanced/export_BORIS_JSON.js?screen=Search&_action_export=1&output=JSON&exp=0%7C1%7C-date%2Fcreators_name%2Ftitle%7Carchive%7C-%7Ceprintid%3Aeprintid%3AANY%3AEQ%3A{boris_id}%7C-%7Ceprint_status%3Aeprint_status%3AANY%3AEQ%3Aarchive%7Cmetadata_visibility%3Ametadata_visibility%3AANY%3AEQ%3Ashow&n="
    
    response = requests.get(url)
    data = response.json()
    
   

    for item in data:
        date = item.get("date")
        title = item.get("title", [{"lang": "", "text": ""}])[0]["text"]
        full_text_status = item.get("full_text_status", "")
        
        year = date[:4]
        
        document_info = {
            "year" : year,
            "title": title,
            "full_text_status": full_text_status
        }
    
        return document_info

# boris_id = "179491"
# document_info = get_document_info(boris_id)

# print(document_info)


