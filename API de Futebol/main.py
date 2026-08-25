import subprocess

from config import DBT_PROJECT_DIR, validate_config
from extract.extract_data import extract_all_data
from load.load_to_sql import (
    SQL_DATABASE,
    SQL_DRIVER,
    SQL_PASSWORD,
    SQL_SERVER,
    SQL_TRUSTED_CONNECTION,
    SQL_USERNAME,
    get_connection,
    has_loaded_data,
    load_to_sql_server,
)


def run_dbt():
    subprocess.run(
        ['dbt', 'build', '--project-dir', str(DBT_PROJECT_DIR)],
        check=True,
    )


def main():
    validate_config()

    with get_connection(
        SQL_SERVER,
        SQL_DATABASE,
        SQL_DRIVER,
        SQL_TRUSTED_CONNECTION,
        SQL_USERNAME,
        SQL_PASSWORD,
    ) as connection:
        if has_loaded_data(connection):
            print('Os dados brutos já estão no banco. Pulando extração e carga.')
        else:
            print('Dados brutos não encontrados. Iniciando extração...')
            extracted_data = extract_all_data()
            print('Extração concluída. Iniciando carga...')
            load_to_sql_server(
                extracted_data,
                SQL_SERVER,
                SQL_DATABASE,
                SQL_DRIVER,
                SQL_TRUSTED_CONNECTION,
                SQL_USERNAME,
                SQL_PASSWORD,
            )
            print('Carga dos dados brutos concluída.')

    print('Iniciando transformações dbt...')
    run_dbt()
    print('Transformações dbt concluídas com sucesso.')


if __name__ == '__main__':
    main()


