import json
import requests


def send_request(url, data):
    headers = {
        'Content-type': 'application/json',
        'Accept': 'text/plain',
        'Content-Encoding': 'utf-8'
    }
    return requests.post(url, data=json.dumps(data), headers=headers)


def auth_bot(master_ip, game_id, token, bot_id, bot_token):
    url = f"http://{master_ip}/api/bots/{bot_id}/authorize"
    data = {
        "access_token": bot_token
    }
    try:
        res = send_request(url, _add_game_management(data, game_id, token))
    except Exception as e:
        print(e)
        return None
    if res.status_code != 200:
        print(res.json())
        return None
    if res.json()["success"] != True:
        return None
    return True


def _add_game_management(data, game_id, token):
    data["game"] = {
        "id": game_id,
        "manager_token": token
    }
    return data


def create_match(master_ip, game_id, token, bots_ids):
    url = f"http://{master_ip}/api/matches/create"
    data = {
        "participants": bots_ids
    }
    try:
        res = send_request(url, _add_game_management(data, game_id, token))
    except Exception as e:
        print(e)
        return None
    if res.status_code != 200:
        print(res.json())
        return None
    return res.json()["id"]


def start_match(master_ip, game_id, token, match_id):
    url = f"http://{master_ip}/api/matches/{match_id}/start"
    try:
        res = send_request(url, _add_game_management(dict(), game_id, token))
    except Exception as e:
        print(e)
        return None
    if res.status_code != 200:
        print(res.json())
        return None
    return True


def finish_match(master_ip, game_id, token, match_id, data):
    url = f"http://{master_ip}/api/matches/{match_id}/finish"
    try:
        res = send_request(url, _add_game_management(data, game_id, token))
    except Exception as e:
        print(e)
        return None
    if res.status_code != 200:
        print(res.json())
        return None
    return True
