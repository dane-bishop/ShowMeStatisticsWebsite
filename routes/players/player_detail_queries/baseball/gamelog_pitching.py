GAMELOG_PITCHING_SQL = """
    SELECT
    pgp.id,
    pgp.source_game_id,
    pgp.wl,
    pgp.ip, pgp.h, pgp.r, pgp.er, pgp.bb, pgp.so, pgp.doubles, pgp.triples,
    pgp.hr, pgp.wp, pgp.bk, pgp.hbp, pgp.ibb, pgp.np, pgp.w, pgp.l, pgp.sv, pgp.gera, pgp.sera,
    g.game_date,
    o.name AS opponent_name
    FROM player_game_pitching pgp
    JOIN games g ON g.id = pgp.game_id
    JOIN opponents o ON o.id = g.opponent_id
    WHERE pgp.player_id = %s
    ORDER BY COALESCE(g.game_date, '1900-01-01') ASC, pgp.id ASC;
    """
