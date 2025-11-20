TEAM_SQL = """
    SELECT
      t.id            AS team_id,
      t.school_name,
      t.site_slug,
      s.id            AS sport_id,
      s.name          AS sport_name
    FROM teams t
    JOIN sports s ON s.id = t.sport_id
    WHERE t.site_slug = %s
    """