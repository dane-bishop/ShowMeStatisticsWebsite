FAVORITES_SQL = """
      SELECT entity_id
      FROM favorites
      WHERE user_id = %s
      AND entity_type = 'player'
    
    """