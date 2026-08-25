--consulta auxiliar para visualizar times e seus respectivos id's.

select distinct
    team_id               as id_time,
    team_name             as nome_time
from (
    select home_team_id as team_id, home_team_name as team_name
    from {{ ref('stg_fixtures') }}

    union

    select away_team_id as team_id, away_team_name as team_name
    from {{ ref('stg_fixtures') }}
) as teams