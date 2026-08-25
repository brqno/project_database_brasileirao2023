# API de Futebol

Pipeline de dados esportivos usando Python, SQL Server, dbt e Power BI.

## Arquitetura

```text
API Football
    |
    v
Python (extract)
    |
    v
SQL Server (dados brutos)
    |
    v
dbt (staging -> intermediate -> marts)
    |
    v
Power BI
```

O Python consome a API e carrega todas as partidas da liga e temporada configuradas na tabela bruta `dbo.fixtures_2023`. O dbt aplica as regras de negocio e cria um modelo analitico para o Power BI.

## Estrutura

```text
extract/       Integracao com a API
load/          Carga no SQL Server
dbt_soccer/    Projeto dbt
main.py        Entrada unica do pipeline
config.py      Configuracao via .env
```

Os modelos dbt ficam em `dbt_soccer/models`:

- `staging/stg_fixtures.sql`: padroniza os campos das partidas brutas.
- `intermediate/int_team_matches.sql`: cria uma linha por time em cada partida e calcula gols, resultado e pontos.
- `marts/fact_matches.sql`: uma linha por partida.
- `marts/fact_team_matches.sql`: desempenho de cada time por partida.
- `marts/dim_team.sql`: dimensao de times.
- `marts/dim_date.sql`: dimensao de datas.

## Configuracao

1. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
.venv\\Scripts\\activate
```

2. Instale as dependencias:

```bash
pip install -r requirements.txt
```

3. Copie `.env.example` para `.env` e preencha `API_FOOTBALL_KEY`.

Com autenticacao Windows no SQL Server, mantenha:

```env
SQL_TRUSTED_CONNECTION=true
```

Com usuario e senha do SQL Server:

```env
SQL_TRUSTED_CONNECTION=false
SQL_USERNAME=seu_usuario
SQL_PASSWORD=sua_senha
```

4. Configure o perfil dbt em `%USERPROFILE%\\.dbt\\profiles.yml` usando o adapter `sqlserver`. Esse arquivo nao deve ser commitado.

## Execucao

Execute a partir da raiz:

```bash
python main.py
```

O pipeline verifica se a tabela bruta possui dados. Se possuir, pula a extracao e a carga, mas executa o `dbt build`. Caso contrario, extrai todas as partidas da liga, carrega os dados brutos e executa o dbt.

Para executar o dbt manualmente:

```bash
dbt parse --project-dir dbt_soccer
dbt build --project-dir dbt_soccer
```

## Power BI

No Power BI Desktop, use **Obter dados > SQL Server** e conecte ao banco configurado. Para o dashboard deste projeto, utilize a tabela `fact_team_matches`, que possui uma linha por partida e os campos:

- `id_partida`
- `data_partida`
- `id_time_casa` e `nome_time_casa`
- `id_time_fora` e `nome_time_fora`
- `gols_casa` e `gols_fora`

Os demais modelos (`fact_team_matches`, `dim_team` e `dim_date`) ficam disponíveis no banco para análises futuras por time e por data.


## Seguranca

Nunca versione `.env` ou credenciais. A chave da API e as credenciais do banco sao lidas em tempo de execucao.
