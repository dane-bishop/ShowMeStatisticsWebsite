PLAYER_SQL = """
    SELECT
    p.id,
    p.full_name,
    p.player_slug,
    p.player_id       AS external_player_id,
    rm.position,
    rm.jersey,
    rm.class_year,
    rm.bats_throws,
    rm.hometown,
    rm.high_school,
    ts.year           AS season_year,
    t.school_name,
    s.name            AS sport_name
    FROM players p
    JOIN roster_memberships rm ON rm.player_id = p.id
    JOIN team_seasons ts       ON rm.team_season_id = ts.id
    JOIN teams t               ON ts.team_id = t.id
    JOIN sports s              ON t.sport_id = s.id
    WHERE p.player_slug = %s
    ORDER BY ts.year DESC
    LIMIT 1;
    """