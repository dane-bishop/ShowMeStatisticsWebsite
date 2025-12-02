GAME_CALENDAR_SQL = """
SELECT
    g.id,
    g.game_date,
    g.game_time,
    g.location,
    g.result,
    g.score_for,
    g.score_against,
    o.name AS opponent_name,
    s.name  AS sport_name
FROM games g
JOIN team_seasons ts ON ts.id = g.team_season_id
JOIN teams t ON t.id = ts.team_id
JOIN sports s       ON s.id = t.sport_id
JOIN opponents o    ON o.id = g.opponent_id
WHERE g.game_date BETWEEN %s AND %s
ORDER BY g.game_date, g.game_time NULLS LAST, g.id;
"""