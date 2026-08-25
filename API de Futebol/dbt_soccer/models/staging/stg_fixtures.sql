select
	fixture_id,
	cast(match_date as date) as match_date,
	home_team_id,
	home_team_name,
	away_team_id,
	away_team_name,
	home_goals,
	away_goals
from {{ source('soccer', 'fixtures_2023') }}
