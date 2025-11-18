IS_FAVORITE_SQL = """
    SELECT 1 
    FROM favorites
    WHERE user_id = %s AND entity_type = 'player' AND entity_id = %s
    LIMIT 1
    """