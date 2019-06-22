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
	SELECT
		team_id,
		"date",
		ARRAY_AGG ( team_player_ass.shirt_number) as shirt_number,
		ARRAY_AGG ( team_player_ass."player_id" ) as player_id,
		ARRAY_AGG ( team_player_ass."position" ) as "position",
		ARRAY_AGG ( team_player_ass.height ) as height,
		ARRAY_AGG ( team_player_ass.weight ) as weight,
		ARRAY_AGG ( team_player_ass.age ) as age,
		json_agg ( team_player_ass.stat_doc ) as stat_doc 
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