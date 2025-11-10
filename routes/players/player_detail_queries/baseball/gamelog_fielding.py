GAMELOG_FIELDING_SQL = """
    SELECT
    pgf.id, pgf.source_game_id, pgf.wl,
    pgf.c, pgf.po, pgf.a, pgf.e, pgf.fld, pgf.dp, pgf.sba, pgf.csb, pgf.pb, pgf.ci,
    g.game_date,
    o.name AS opponent_name
    FROM player_game_fielding pgf
    JOIN games g ON g.id = pgf.game_id
    JOIN opponents o ON o.id = g.opponent_id
    WHERE pgf.player_id = %s
    ORDER BY COALESCE(g.game_date, '1900-01-01') ASC, pgf.id ASC;
    """