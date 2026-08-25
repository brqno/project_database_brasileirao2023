import requests
import pandas as pd
from config import API_KEY, API_URL, LEAGUE_ID, SEASON

headers = {"x-apisports-key": API_KEY}

def team_data(team_id):
    parametros = {
        "league": LEAGUE_ID,
        "season": SEASON,
    }
    if team_id is not None:
        parametros["team"] = team_id

    response = requests.get(API_URL, headers=headers, params=parametros)
    response.raise_for_status()

    dados = response.json().get("response", [])
    lista_formatada = []

    for item in dados:
        info = {
            "fixture_id": item["fixture"]["id"],
            "date": item["fixture"]["date"][:10],
            "home_team_id": item["teams"]["home"]["id"],
            "home_team_name": item["teams"]["home"]["name"],
            "away_team_id": item["teams"]["away"]["id"],
            "away_team_name": item["teams"]["away"]["name"],
            "home_goals": item["goals"]["home"],
            "away_goals": item["goals"]["away"]
        }

        lista_formatada.append(info)

    return pd.DataFrame(lista_formatada)

def extract_all_data():
    return {'fixtures': team_data(None)}