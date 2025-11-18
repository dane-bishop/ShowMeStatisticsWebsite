SEASON_HIGHS_SQL = """
    SELECT
    stat_name,
    value,
    opponent_text,
    source_game_id,
    game_datetime
    FROM player_season_highs
    WHERE player_id = %s
    ORDER BY stat_name ASC;
    """