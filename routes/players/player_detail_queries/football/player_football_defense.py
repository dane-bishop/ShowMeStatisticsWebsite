GAMELOG_FOOTBALL_OFFENSE_SQL = """
    SELECT 
    pgfd.id,
    pgfd.source_game_id,
    pgfd.solo, pgfd.ast, pgfd.ttot, pgfd.tfl, pgfd.tyds,
    pgfd.stot, pgfd.syds,
    pgfd.ff, pgfd.fr, pgfd.fyds,
    pgfd.ints, pgfd.int_yds,
    pgfd.qbh, pgfd.brk, pgfd.kick, pgfd.saf,
    g.game_date,
    o.name AS opponent_name
    FROM player_game_football_defense pgfd
    LEFT JOIN games g ON g.id = pgfd.game_id
    JOIN opponents o ON o.id = g.opponent_id
    WHERE pgfd.player_id = %s
    ORDER BY COALESCE(g.game_date, '1900-01-01) ASC, pgfd.id ASC;
"""