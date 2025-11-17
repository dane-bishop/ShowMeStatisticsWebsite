PLAYER_FIELDING_STATS_SQL = """
    SELECT
    p.full_name,
    rm.jersey,
    pgf.c, pgf.po, pgf.a, pgf.e, pgf.fld, pgf.dp, pgf.sba, pgf.csb, pgf.pb, pgf.ci
    FROM player_game_fielding pgf
    JOIN games g ON g.id = pgf.game_id
    JOIN players p ON p.id = pgf.player_id
    LEFT JOIN roster_memberships rm
    ON rm.player_id = p.id
    AND rm.team_season_id = g.team_season_id
    WHERE pgf.game_id = %s
    ORDER BY p.id, rm.id DESC;
    """