# Database Testing Results
Generated on: 2024-11-22 23:46:11

Schema Version: 1.0
Category: validation_queries
Description: Validation queries to ensure the IPL statistics platform functions correctly

---
## Question 9
### User Query
Find matches where the player was both the captain and the player of the match.

### Explanation
Identifies matches where a player served as both the team captain and was awarded Player of the Match.

### SQL Query
```sql
SELECT m.id as match_id, m.date, t.id as team_id, t.full_name as team_name, p.id as player_id, p.name as player_name FROM ipl.matches m JOIN ipl.player_match_roles pmr ON m.id = pmr.match_id AND pmr.is_captain = TRUE JOIN ipl.players p ON pmr.player_id = p.id JOIN ipl.points_table pt ON m.season_id = pt.season_id AND pt.team_id = m.winner_id JOIN ipl.batting_aggregate ba ON p.id = ba.player_id AND ba.match_id = m.id WHERE pt.winner = TRUE AND m.player_of_match_id = p.id ORDER BY m.date DESC
```

### Error
```json
{
  "error": "column ba.match_id does not exist",
  "detail": "42703"
}
```

---

## Question 19
### User Query
Find matches where a captain also took a wicket.

### Explanation
Identifies matches where the team captain also took at least one wicket, including match and player details.

### SQL Query
```sql
SELECT DISTINCT m.id as match_id, m.date, p.id as player_id, p.name as player_name, t.short_name as team FROM ipl.matches m JOIN ipl.player_match_roles pmr ON m.id = pmr.match_id AND pmr.is_captain = TRUE JOIN ipl.player_match_performance pmp ON pmr.player_id = pmp.player_id AND m.id = pmp.match_id JOIN ipl.players p ON pmp.player_id = p.id JOIN ipl.teams t ON pmp.team_id = t.id WHERE pmp.did_bowl = TRUE AND pmp.wickets > 0 ORDER BY m.date DESC
```

### Error
```json
{
  "error": "column pmp.wickets does not exist",
  "detail": "42703"
}
```

---

