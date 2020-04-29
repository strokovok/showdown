import json
import random
import requests

from run import run

MAX_ID = 16
GAME_ID = 1
GAME_PASSWORD = "password"

def add_game_management(res):
    res["game"] = {
        "id": GAME_ID,
        "manager_token": GAME_PASSWORD
    }

def send_request(route, data):
    add_game_management(data)
    headers = {
        'Content-type': 'application/json',
        'Accept': 'text/plain',
        'Content-Encoding': 'utf-8'
    }
    url = f"http://127.0.0.1:5000/api/matches/{route}"
    answer = requests.post(url, data=json.dumps(data), headers=headers)
    return answer.json()


def run_multiple():
    while True:
        # Create match
        ids = random.sample(range(1, MAX_ID + 1), k=2)
        data = {"participants": ids}
        match_id = send_request("create", data)["id"]

        # Start match
        send_request(f"{match_id}/start", dict())
        res = run(ids)

        # Finish match
        answer = send_request(f"{match_id}/finish", res)

#         res = run(ids)
#         add_game_management(res)
#         print(json.dumps(res, indent=4))




run_multiple()
