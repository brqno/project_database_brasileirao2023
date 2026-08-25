import pyodbc
from config import (
    SQL_DATABASE,
    SQL_DRIVER,
    SQL_PASSWORD,
    SQL_SERVER,
    SQL_TRUSTED_CONNECTION,
    SQL_USERNAME,
)

TABLES = {
    'fixtures': 'dbo.fixtures_2023',
}


def get_connection(
    server,
    database,
    driver='ODBC Driver 17 for SQL Server',
    trusted_connection=True,
    username=None,
    password=None,
):
    if trusted_connection:
        connection_string = (
            f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};'
            'Trusted_Connection=yes;TrustServerCertificate=yes;'
        )
    else:
        if not username or password is None:
            raise ValueError(
                'Informe username e password para autenticação SQL Server.'
            )
        connection_string = (
            f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};'
            f'UID={username};PWD={password};'
            'TrustServerCertificate=yes;'
        )


    return pyodbc.connect(connection_string)


def create_table(cursor, table_name):
    cursor.execute(f'''
        IF OBJECT_ID(N'{table_name}', N'U') IS NULL
        BEGIN
            CREATE TABLE {table_name} (
                fixture_id BIGINT NOT NULL PRIMARY KEY,
                match_date DATE NOT NULL,
                home_team_id INT NOT NULL,
                home_team_name NVARCHAR(100) NOT NULL,
                away_team_id INT NOT NULL,
                away_team_name NVARCHAR(100) NOT NULL,
                home_goals INT NULL,
                away_goals INT NULL
            )
        END
    ''')

def has_loaded_data(connection):
    cursor = connection.cursor()

    for table_name in TABLES.values():
        table_exists = cursor.execute(
            'SELECT OBJECT_ID(?, ?)', table_name, 'U'
        ).fetchone()[0]
        if table_exists is None:
            return False

        result = cursor.execute(
            f'SELECT CASE WHEN EXISTS (SELECT 1 FROM {table_name}) '
            'THEN 1 ELSE 0 END'
        ).fetchone()
        if result[0] == 0:
            return False

    return True


def load_team(cursor, table_name, df):
    create_table(cursor, table_name)
    cursor.execute(f'DELETE FROM {table_name}')

    rows = [
        (
            row.fixture_id,
            row.date,
            row.home_team_id,
            row.home_team_name,
            row.away_team_id,
            row.away_team_name,
            row.home_goals,
            row.away_goals,
        )
        for row in df.itertuples(index=False)
    ]

    cursor.fast_executemany = True
    cursor.executemany(f'''
        INSERT INTO {table_name} (
            fixture_id, match_date, home_team_id, home_team_name,
            away_team_id, away_team_name, home_goals, away_goals
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', rows)


def load_to_sql_server(
    extracted_data,
    server,
    database,
    driver='ODBC Driver 17 for SQL Server',
    trusted_connection=True,
    username=None,
    password=None,
):
    with get_connection(
        server,
        database,
        driver,
        trusted_connection,
        username,
        password,
    ) as connection:
        cursor = connection.cursor()
        for team, df in extracted_data.items():
            load_team(cursor, TABLES[team], df)
        connection.commit()


if __name__ == '__main__':
    from extract.extract_data import extract_all_data

    load_to_sql_server(
        extract_all_data(),
        SQL_SERVER,
        SQL_DATABASE,
        SQL_DRIVER,
        SQL_TRUSTED_CONNECTION,
        SQL_USERNAME,
        SQL_PASSWORD,
    )