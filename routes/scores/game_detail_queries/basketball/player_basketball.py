PLAYER_BASKETBALL_STATS_SQL = """
    SELECT 
    p.full_name,
    p.player_slug,
    rm.jersey,
    pgb.minutes, pgb.fg_made, pgb.fg_att, pgb.fg_pct,
    pgb.three_made, pgb.three_att, pgb.three_pct,
    pgb.ft_made, pgb.ft_att, pgb.ft_pct,
    pgb.off_r, pgb.dr, pgb.tr, pgb.r_avg,
    pgb.pf, pgb.ast, pgb.turnovers, pgb.blk,
    pgb.stl, pgb.pts, pgb.pts_avg
    FROM player_game_basketball pgb
    JOIN games g ON g.id = pgb.game_id
    JOIN players p ON p.id = pgb.player_id
    LEFT JOIN roster_memberships rm
    ON rm.player_id = p.id
    AND rm.team_season_id = g.team_season_id
    WHERE pgb.game_id = %s
    ORDER BY p.id, rm.id DESC; 
    """