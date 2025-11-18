TEAM_SEARCH_SQL = """
    SELECT DISTINCT ON (t.id)
        t.id,
        t.school_name,
        s.name                  AS sport_name,
        COALESCE(t.site_slug) AS team_slug,
        ts.year
    FROM teams t
    JOIN sports s ON s.id = t.sport_id
    LEFT JOIN team_seasons ts ON ts.team_id = t.id
    WHERE t.school_name ILIKE %(pat)s
       OR s.name ILIKE %(pat)s
       OR (t.school_name || ' ' || s.name) ILIKE %(pat)s
    ORDER BY t.id, ts.year DESC
    LIMIT %(limit)s OFFSET %(offset)s;
    """