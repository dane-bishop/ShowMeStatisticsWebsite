PLAYER_VOLLEYBALL_STATS_SQL = """
    SELECT 
    p.full_name,
    rm.jersey,

    pgv.wl, pgv.sp, pgv.k, pgv.ae,
    pgv.ta, pgv.h_pct, pgv.ast,
    pgv.e, pgv.sa, pgv.se,
    pgv.dre, pgv.dd, pgv.solo, pgv.blk_ast,
    pgv.blk_e, pgv.tot_blk, pgv.bhe, pgv.pts

    FROM player_game_volleyball pgv
    JOIN games g ON g.id = pgv.game_id
    JOIN players p ON p.id = pgv.player_id
    LEFT JOIN roster_memberships rm
    ON rm.player_id = p.id
    AND rm.team_season_id = g.team_season_id
    WHERE pgv.game_id = %s
    ORDER BY p.id, rm.id DESC; 
    """



