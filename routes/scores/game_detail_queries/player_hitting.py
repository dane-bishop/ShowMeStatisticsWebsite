PLAYER_HITTING_STATS_SQL = """
    SELECT
    p.full_name,
    rm.jersey,
    pgb.ab, pgb.r, pgb.h, pgb.rbi,
    pgb.doubles, pgb.triples, pgb.hr,
    pgb.bb, pgb.ibb,
    pgb.sb, pgb.sba, pgb.cs,
    pgb.hbp, pgb.sh, pgb.sf, pgb.gdp, pgb.k,
    pgb.avg
    FROM player_game_batting pgb
    JOIN games g ON g.id = pgb.game_id
    JOIN players p ON p.id = pgb.player_id
    LEFT JOIN roster_memberships rm
    ON rm.player_id = p.id
    AND rm.team_season_id = g.team_season_id
    WHERE pgb.game_id = %s
    ORDER BY p.id, rm.id DESC;
    """