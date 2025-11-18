GAME_SQL = """
    SELECT
    g.game_date,
    g.location,
    o.name AS opponent_name,
    g.result,
    g.score_for,
    g.score_against,
    v.name AS venue_name,
    s.name AS sport_name
    FROM games g
    JOIN opponents o ON o.id = g.opponent_id
    LEFT JOIN venues v ON v.id = g.venue_id
    JOIN team_seasons ts ON ts.id = g.team_season_id
    JOIN teams t ON t.id = ts.team_id
    JOIN sports s ON s.id = t.sport_id
    WHERE g.id = %s
    """
