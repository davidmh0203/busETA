import json

def load_shuttle_json():
    with open("appmain/static/data/shuttle_backseck.json", encoding='utf-8') as f1, \
         open("appmain/static/data/shuttle_samsong.json", encoding='utf-8') as f2:
        return {
            "baekseok": json.load(f1)["data"],
            "samsong": json.load(f2)["data"]
        }
