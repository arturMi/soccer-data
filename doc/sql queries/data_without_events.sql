SELECT
	* 
FROM
	(
	SELECT
		* 
	FROM
		"match",
		match_report,
		season,
		league,
		referee 
	WHERE
		"match"."id" = match_report.match_id 
		AND "match".referee_id = referee."id" 
		AND "match".season_id = season."id" 
		AND season.league_id = league."id" 
	) AS table_1
	INNER JOIN (
	SELECT
		*,
		tmp_2."date" AS tmp_2_date 
	FROM
		(
		SELECT
			*,
			team."id" AS tmp_1_team_id 
		FROM
			team,
			team_trainer_ass,
			trainer 
		WHERE
			team."id" = team_trainer_ass.team_id 
			AND trainer."id" = team_trainer_ass.trainer_id 
		) AS tmp_1,
		(
		SELECT ARRAY_AGG
			( team_player_ass."player_id" ),
			team_id,
			"date",
			ARRAY_AGG ( team_player_ass.shirt_number ),
			ARRAY_AGG ( team_player_ass."position" ),
			ARRAY_AGG ( team_player_ass.height ),
			ARRAY_AGG ( team_player_ass.weight ),
			ARRAY_AGG ( team_player_ass.age ),
			json_agg ( team_player_ass.stat_doc ) 
		FROM
			team,
			team_player_ass 
		WHERE
			team."id" = team_player_ass.team_id 
		GROUP BY
			team_player_ass.team_id,
			team_player_ass."date" 
		) AS tmp_2 
	WHERE
		tmp_1_team_id = tmp_2.team_id 
		AND tmp_1."date" = tmp_2."date" 
	) AS table_2 ON table_1.away_team_id = table_2.tmp_1_team_id 
	AND table_1."date" = table_2.tmp_2_date;