GAMELOG_HITTING_SQL = """
    SELECT
    pgb.id,
    pgb.source_game_id,
    pgb.wl,
    pgb.gs,
    pgb.ab, pgb.r, pgb.h, pgb.rbi,
    pgb.doubles, pgb.triples, pgb.hr,
    pgb.bb, pgb.ibb,
    pgb.sb, pgb.sba, pgb.cs,
    pgb.hbp, pgb.sh, pgb.sf, pgb.gdp, pgb.k,
    pgb.avg,
    g.game_date,        
    o.name AS opponent_name 
    FROM player_game_batting pgb
    LEFT JOIN games g ON g.id = pgb.game_id
    JOIN opponents o ON o.id = g.opponent_id
    WHERE pgb.player_id = %s
    ORDER BY COALESCE(g.game_date, '1900-01-01') ASC, pgb.id ASC;
    """



