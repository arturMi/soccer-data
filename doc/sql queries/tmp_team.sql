SELECT * 
FROM (SELECT *, team."id" as tmp_1_team_id 
			FROM team, team_trainer_ass, trainer
			WHERE team."id" = team_trainer_ass.team_id AND 
						trainer."id" = team_trainer_ass.trainer_id) as tmp_1, 
			(SELECT array_agg(team_player_ass."player_id"),
							team_id, 
							"date", array_agg(team_player_ass.shirt_number),
							array_agg(team_player_ass."position"), 
							array_agg(team_player_ass.height), 
							array_agg(team_player_ass.weight), 
							array_agg(team_player_ass.age), 
							json_agg(team_player_ass.stat_doc)
				FROM team, team_player_ass
				WHERE team."id" = team_player_ass.team_id
				GROUP BY team_player_ass.team_id, team_player_ass."date") as tmp_2
WHERE tmp_1_team_id = tmp_2.team_id AND 
			tmp_1."date" = tmp_2."date";