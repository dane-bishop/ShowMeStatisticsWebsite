GAMELOG_FOOTBALL_OFFENSE_SQL = """
    SELECT 
    pgfo.id,
    pgfo.source_game_id,
    pgfo.pass_comp, pgfo.pass_att, pgfo.pass_int, pgfo.pass_pct,
    pgfo.pass_yds, pgfo.pass_tds, pgfo.pass_lng,
    pgfo.rush_att, pgfo.rush_yds, pgfo.rush_tds, pgfo.rush_lng,
    pgfo.rec, pgfo.rec_yds, pgfo.rec_tds, pgfo.rec_lng,
    pgfo.kr_ret, pgfo.kr_yds, pgfo.kr_tds, pgfo.kr_lng,
    pgfo.pr_ret, pgfo.pr_yds, pgfo.pr_tds, pgfo.pr_lng,
    g.game_date,
    o.name AS opponent_name
    FROM player_game_football_offense pgfo
    LEFT JOIN games g ON g.id = pgfo.game_id
    JOIN opponents o ON o.id = g.opponent_id
    WHERE pgfo.player_id = %s
    ORDER BY COALESCE(g.game_date, '1900-01-01') ASC, pgfo.id ASC;
"""