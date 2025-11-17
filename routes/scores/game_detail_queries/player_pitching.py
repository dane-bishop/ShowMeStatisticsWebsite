PLAYER_PITCHING_STATS_SQL = """
    SELECT
    p.full_name,
    rm.jersey,
    pgp.ip, pgp.h, pgp.r, pgp.er, pgp.bb, pgp.so, pgp.doubles, pgp.triples,
    pgp.hr, pgp.wp, pgp.bk, pgp.hbp, pgp.ibb, pgp.np, pgp.w, pgp.l, pgp.sv, pgp.gera, pgp.sera
    FROM player_game_pitching pgp
    JOIN games g ON g.id = pgp.game_id
    JOIN players p ON p.id = pgp.player_id
    LEFT JOIN roster_memberships rm
    ON rm.player_id = p.id
    AND rm.team_season_id = g.team_season_id
    WHERE pgp.game_id = %s
    ORDER BY p.id, rm.id DESC;
    """