PLAYER_SEARCH_SQL = """
    SELECT DISTINCT ON (p.id)
        p.id,
        p.full_name,
        p.player_slug,
        ts.year                AS season_year,
        t.school_name,
        s.name                 AS sport_name
    FROM players p
    JOIN roster_memberships rm ON rm.player_id = p.id
    JOIN team_seasons ts       ON ts.id = rm.team_season_id
    JOIN teams t               ON t.id = ts.team_id
    JOIN sports s              ON s.id = t.sport_id
    WHERE p.full_name ILIKE %(pat)s
       OR p.player_slug ILIKE %(pat)s
       OR t.school_name ILIKE %(pat)s
       OR s.name ILIKE %(pat)s
    ORDER BY p.id, ts.year DESC
    LIMIT %(limit)s OFFSET %(offset)s;
    """