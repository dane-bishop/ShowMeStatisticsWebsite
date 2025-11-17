GAMELOG_VOLLEYBALL_SQL = """
    SELECT 
    pgv.id,
    pgv.source_game_id,

    pgv.wl, pgv.sp, pgv.k, pgv.ae,
    pgv.ta, pgv.h_pct, pgv.ast,
    pgv.e, pgv.sa, pgv.se,
    pgv.dre, pgv.dd, pgv.solo, pgv.blk_ast,
    pgv.blk_e, pgv.tot_blk, pgv.bhe, pgv.pts,

    g.game_date,
    o.name AS opponent_name
    FROM player_game_volleyball pgv
    LEFT JOIN games g ON g.id = pgv.game_id
    JOIN opponents o ON o.id = g.opponent_id
    WHERE pgv.player_id = %s
    ORDER BY COALESCE(g.game_date, '1900-01-01') ASC, pgv.id ASC;
"""