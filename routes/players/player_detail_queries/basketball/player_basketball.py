GAMELOG_BASKETBALL_SQL = """
    SELECT 
    pgb.id,
    pgb.source_game_id,
    pgb.minutes, pgb.fg_made, pgb.fg_att, pgb.fg_pct,
    pgb.three_made, pgb.three_att, pgb.three_pct,
    pgb.ft_made, pgb.ft_att, pgb.ft_pct,
    pgb.off_r, pgb.dr, pgb.tr, pgb.r_avg,
    pgb.pf, pgb.ast, pgb.turnovers, pgb.blk,
    pgb.stl, pgb.pts, pgb.pts_avg,
    g.game_date,
    o.name AS opponent_name
    FROM player_game_basketball pgb
    LEFT JOIN games g ON g.id = pgb.game_id
    JOIN opponents o ON o.id = g.opponent_id
    WHERE pgb.player_id = %s
    ORDER BY COALESCE(g.game_date, '1900-01-01') ASC, pgb.id ASC;
"""

