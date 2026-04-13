CREATE OR REPLACE FUNCTION main.tennis.get_player_tier(ranking INT)
RETURNS STRING
RETURN
  CASE
    WHEN ranking <= 10 THEN 'Elite'
    WHEN ranking <= 50 THEN 'Pro'
    WHEN ranking <= 200 THEN 'Competitive'
    ELSE 'Developing'
  END;
