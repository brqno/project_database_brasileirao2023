--consulta auxiliar par a análises de partida

select
    fixture_id                      as id_partida,
    match_date                      as data_partida,
    home_team_id                    as id_time_casa,
    home_team_name                  as nome_time_casa,
    away_team_id                    as id_time_fora,
    away_team_name                  as nome_time_fora,
    home_goals                      as gols_casa,
    away_goals                      as gols_fora
from {{ ref('stg_fixtures') }}