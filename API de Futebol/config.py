import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_DIR = Path(__file__).parent
DBT_PROJECT_DIR = PROJECT_DIR / 'dbt_soccer'

API_KEY = os.getenv('API_FOOTBALL_KEY', '')
API_URL = 'https://v3.football.api-sports.io/fixtures'
LEAGUE_ID = int(os.getenv('FOOTBALL_LEAGUE_ID', '71'))
SEASON = int(os.getenv('FOOTBALL_SEASON', '2023'))

SQL_SERVER = os.getenv('SQL_SERVER', 'DESKTOP-DUBDQD2')
SQL_DATABASE = os.getenv('SQL_DATABASE', 'SOCCER')
SQL_DRIVER = os.getenv('SQL_DRIVER', 'ODBC Driver 18 for SQL Server')
SQL_TRUSTED_CONNECTION = os.getenv(
    'SQL_TRUSTED_CONNECTION', 'true'
).lower() == 'true'
SQL_USERNAME = os.getenv('SQL_USERNAME')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')


def validate_config():
    if not API_KEY or API_KEY == 'coloque_sua_nova_chave_aqui':
        raise ValueError(
            'API_FOOTBALL_KEY inválida. Substitua o valor de exemplo no arquivo '
            '.env por uma chave ativa do API-Football.'
        )