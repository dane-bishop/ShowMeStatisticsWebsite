ROSTER_SQL = """
    SELECT
      p.id                           AS player_id,
      p.full_name,
      p.player_slug,

      rm.id                          AS roster_membership_id,
      rm.team_season_id,
      rm.jersey,
      rm.position,
      rm.class_year,
      rm.height_raw,
      rm.weight_lbs,
      rm.bats_throws,
      rm.hometown,
      rm.high_school,

      ts.id                          AS team_season_id,
      ts.team_id                     AS ts_team_id,
      ts.year                        AS season_year,

      t.id                           AS t_id,
      t.sport_id                     AS t_sport_id,

      s.id                           AS s_id,
      s.name                         AS sport_name
    FROM roster_memberships rm
    JOIN players       p  ON p.id  = rm.player_id
    JOIN team_seasons  ts ON ts.id = rm.team_season_id
    JOIN teams         t  ON t.id  = ts.team_id
    JOIN sports        s  ON s.id  = t.sport_id
    WHERE t.site_slug = %s
      AND ts.year = %s
      AND p.player_slug IS NOT NULL
      AND p.player_slug <> ''
    ORDER BY
      -- Try jersey numerical sort when numeric, otherwise by name
      (CASE WHEN rm.jersey ~ '^[0-9]+$' THEN rm.jersey::int END) NULLS LAST,
      p.full_name ASC;
    """