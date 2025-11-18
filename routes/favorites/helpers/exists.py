def _exists(conn, entity_type: str, entity_id: int) -> bool:
    # App-level referential check
    table = {
        "player": "players",
        "team": "teams",
        "game": "games",
        "stat_high": "player_season_highs"
    }[entity_type]
    pk = "id"
    with conn.cursor() as cur:
        cur.execute(f"SELECT 1 FROM {table} WHERE {pk} = %s LIMIT 1", (entity_id,))
        return cur.fetchone() is not None
    
