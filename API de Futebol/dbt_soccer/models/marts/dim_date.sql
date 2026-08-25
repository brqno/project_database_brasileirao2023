select distinct
    match_date                        as data_partida,
    year(match_date)                  as ano_numero,
    month(match_date)                 as mes_numero,
    datename(month, match_date)       as mes_nome,
    datepart(quarter, match_date)     as trimestre_numero
from {{ ref('stg_fixtures') }}