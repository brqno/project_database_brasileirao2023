--consulta principal para análise no Power BI.

select
    fixture_id                      as id_partida,
    match_date                      as data_partida,
    team_id                         as id_time,
    team_name                       as nome_time,
    opponent_team_id                as id_time_oponente,
    opponent_team_name              as nome_time_oponente,
    playing_at_home                 as jogando_em_casa,
    goals_for                       as gols_pro,
    goals_against                   as gols_contra,
    result                          as resultado,
    points                          as pontos
from {{ ref('int_team_matches') }}

