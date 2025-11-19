EVENTS_SQL = """
        SELECT
            g.id,
            g.game_date,
            s.name AS sport_name,
            t.school_name,
            o.name AS opponent_name,
            g.location,
            g.result,
            g.score_for,
            g.score_against,
            g.source_game_id
        FROM games g
        JOIN team_seasons ts ON ts.id = g.team_season_id
        JOIN teams t ON t.id = ts.team_id
        JOIN sports s ON s.id = t.sport_id
        LEFT JOIN opponents o ON o.id = g.opponent_id
        WHERE g.game_date >= %s AND g.game_date <= %s
        """