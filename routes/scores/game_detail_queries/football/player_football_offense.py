PLAYER_FOOTBALL_OFFENSE_STATS_SQL = """
    SELECT 
    p.full_name,
    rm.jersey,
    pgfo.pass_comp, pgfo.pass_att, pgfo.pass_int, pgfo.pass_pct,
    pgfo.pass_yds, pgfo.pass_tds, pgfo.pass_lng,
    pgfo.rush_att, pgfo.rush_yds, pgfo.rush_tds, pgfo.rush_lng,
    pgfo.rec, pgfo.rec_yds, pgfo.rec_tds, pgfo.rec_lng,
    pgfo.kr_ret, pgfo.kr_yds, pgfo.kr_tds, pgfo.kr_lng,
    pgfo.pr_ret, pgfo.pr_yds, pgfo.pr_tds, pgfo.pr_lng
    FROM player_game_football_offense pgfo
    JOIN games g ON g.id = pgfo.game_id
    JOIN players p ON p.id = pgfo.player_id
    LEFT JOIN roster_memberships rm
    ON rm.player_id = p.id
    AND rm.team_season_id = g.team_season_id
    WHERE pgfo.game_id = %s
    ORDER BY p.id, rm.id DESC; 
    """