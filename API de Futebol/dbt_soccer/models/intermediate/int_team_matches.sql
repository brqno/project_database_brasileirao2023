with fixtures as (

	select *
	from {{ ref('stg_fixtures') }}
),

home_matches as (

	select
		fixture_id,
		match_date,
		home_team_id as team_id,
		home_team_name as team_name,
		away_team_id as opponent_team_id,
		away_team_name as opponent_team_name,
		'Home' as playing_at_home,
		home_goals as goals_for,
		away_goals as goals_against
	from fixtures
),

away_matches as (

	select
		fixture_id,
		match_date,
		away_team_id as team_id,
		away_team_name as team_name,
		home_team_id as opponent_team_id,
		home_team_name as opponent_team_name,
		'Away' as playing_at_home,
		away_goals as goals_for,
		home_goals as goals_against
	from fixtures
)

select
	fixture_id,
	match_date,
	team_id,
	team_name,
	opponent_team_id,
	opponent_team_name,
	playing_at_home,
	goals_for,
	goals_against,
	case
		when goals_for > goals_against then 'Win'
		when goals_for = goals_against then 'Draw'
		when goals_for < goals_against then 'Loss'
		else 'Unknown'
	end as result,
	case
		when goals_for > goals_against then 3
		when goals_for = goals_against then 1
		else 0
	end as points
from home_matches

union all

select
	fixture_id,
	match_date,
	team_id,
	team_name,
	opponent_team_id,
	opponent_team_name,
	playing_at_home,
	goals_for,
	goals_against,
	case
		when goals_for > goals_against then 'Win'
		when goals_for = goals_against then 'Draw'
		when goals_for < goals_against then 'Loss'
		else 'Unknown'
	end as result,
	case
		when goals_for > goals_against then 3
		when goals_for = goals_against then 1
		else 0
	end as points
from away_matches
