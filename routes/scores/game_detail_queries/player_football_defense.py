PLAYER_FOOTBALL_DEFENSE_STATS_SQL = """
    SELECT 
    p.full_name,
    rm.jersey,
    pgfd.solo, pgfd.ast, pgfd.ttot, pgfd.tfl, pgfd.tyds,
    pgfd.stot, pgfd.syds,
    pgfd.ff, pgfd.fr, pgfd.fyds,
    pgfd.ints, pgfd.int_yds,
    pgfd.qbh, pgfd.brk, pgfd.kick, pgfd.saf
    FROM player_game_football_defense pgfd
    JOIN games g ON g.id = pgfd.game_id
    JOIN players p ON p.id = pgfd.player_id
    LEFT JOIN roster_memberships rm
    ON rm.player_id = p.id
    AND rm.team_season_id = g.team_season_id
    WHERE pgfd.game_id = %s
    ORDER BY p.id, rm.id DESC;
    """