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
	AND season.league_id = league."id";