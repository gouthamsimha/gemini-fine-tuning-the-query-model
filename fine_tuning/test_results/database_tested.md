# Database Testing Results
Generated on: 2024-11-22 23:46:11

Schema Version: 1.0
Category: validation_queries
Description: Validation queries to ensure the IPL statistics platform functions correctly

---
## Question 1
### User Query
List all matches where the team won by more than 50 runs.

### Explanation
Retrieves matches where the winning team won by more than 50 runs, including match and team details.

### SQL Query
```sql
SELECT m.id as match_id, m.date, t1.id as team1_id, t1.full_name as team1_name, t2.id as team2_id, t2.full_name as team2_name, m.winner_id, m.win_margin, m.win_margin_type FROM ipl.matches m JOIN ipl.teams t1 ON m.team1_id = t1.id JOIN ipl.teams t2 ON m.team2_id = t2.id WHERE m.win_margin > 50 AND m.win_margin_type = 'runs' ORDER BY m.win_margin DESC
```

### Result
```json
[
  {
    "match_id": 630,
    "date": "2017-05-06",
    "team1_id": 1,
    "team1_name": "Delhi Capitals",
    "team2_id": 4,
    "team2_name": "Mumbai Indians",
    "winner_id": 4,
    "win_margin": 146,
    "win_margin_type": "runs"
  },
  {
    "match_id": 539,
    "date": "2016-05-14",
    "team1_id": 5,
    "team1_name": "Royal Challengers Bangalore",
    "team2_id": 1045,
    "team2_name": "Gujarat Lions",
    "winner_id": 5,
    "win_margin": 144,
    "win_margin_type": "runs"
  },
  {
    "match_id": 35,
    "date": "2008-04-18",
    "team1_id": 5,
    "team1_name": "Royal Challengers Bangalore",
    "team2_id": 12,
    "team2_name": "Kolkata Knight Riders",
    "winner_id": 12,
    "win_margin": 140,
    "win_margin_type": "runs"
  },
  {
    "match_id": 515,
    "date": "2015-05-06",
    "team1_id": 5,
    "team1_name": "Royal Challengers Bangalore",
    "team2_id": 2,
    "team2_name": "Punjab Kings",
    "winner_id": 5,
    "win_margin": 138,
    "win_margin_type": "runs"
  },
  {
    "match_id": 330,
    "date": "2013-04-23",
    "team1_id": 5,
    "team1_name": "Royal Challengers Bangalore",
    "team2_id": 356,
    "team2_name": "Pune Warriors India",
    "winner_id": 5,
    "win_margin": 130,
    "win_margin_type": "runs"
  },
  {
    "note": "... and 86 more rows"
  }
]
```

---

## Question 2
### User Query
Find players with more than 100 sixes in their career.

### Explanation
Identifies players who have scored more than 100 sixes across all seasons, including team information.

### SQL Query
```sql
SELECT ba.player_id, ba.player_name, ba.team_id, ba.team_full_name, SUM(ba.sixes) as total_sixes FROM ipl.batting_aggregate ba GROUP BY ba.player_id, ba.player_name, ba.team_id, ba.team_full_name HAVING SUM(ba.sixes) > 100 ORDER BY total_sixes DESC
```

### Result
```json
[
  {
    "player_id": "ba607b88",
    "player_name": "V Kohli",
    "team_id": 5,
    "team_full_name": "Royal Challengers Bangalore",
    "total_sixes": 273
  },
  {
    "player_id": "db584dad",
    "player_name": "CH Gayle",
    "team_id": 5,
    "team_full_name": "Royal Challengers Bangalore",
    "total_sixes": 239
  },
  {
    "player_id": "c4487b84",
    "player_name": "AB de Villiers",
    "team_id": 5,
    "team_full_name": "Royal Challengers Bangalore",
    "total_sixes": 238
  },
  {
    "player_id": "740742ef",
    "player_name": "RG Sharma",
    "team_id": 4,
    "team_full_name": "Mumbai Indians",
    "total_sixes": 230
  },
  {
    "player_id": "a757b0d8",
    "player_name": "KA Pollard",
    "team_id": 4,
    "team_full_name": "Mumbai Indians",
    "total_sixes": 223
  },
  {
    "note": "... and 13 more rows"
  }
]
```

---

## Question 3
### User Query
Get the top 5 teams with the highest average first innings score.

### Explanation
Fetches the top 5 teams based on their average scores in the first innings of matches.

### SQL Query
```sql
SELECT t.id as team_id, t.full_name as team_name, AVG(i.total_score) as avg_first_innings_score FROM ipl.innings i JOIN ipl.teams t ON i.batting_team_id = t.id JOIN ipl.matches m ON i.match_id = m.id WHERE i.innings_number = 1 GROUP BY t.id, t.full_name ORDER BY avg_first_innings_score DESC LIMIT 5
```

### Result
```json
[
  {
    "team_id": 1760,
    "team_name": "Lucknow Super Giants",
    "avg_first_innings_score": 178.91304347826087
  },
  {
    "team_id": 1754,
    "team_name": "Gujarat Titans",
    "avg_first_innings_score": 178.8095238095238
  },
  {
    "team_id": 3,
    "team_name": "Chennai Super Kings",
    "avg_first_innings_score": 169.93846153846152
  },
  {
    "team_id": 5,
    "team_name": "Royal Challengers Bangalore",
    "avg_first_innings_score": 168.73846153846154
  },
  {
    "team_id": 664,
    "team_name": "Sunrisers Hyderabad",
    "avg_first_innings_score": 167.6595744680851
  }
]
```

---

## Question 4
### User Query
List venues that have hosted more than 20 matches.

### Explanation
Displays venues that have hosted more than 20 IPL matches, including location details.

### SQL Query
```sql
SELECT v.id as venue_id, v.name as venue_name, v.city, COUNT(m.id) as total_matches FROM ipl.venues v JOIN ipl.matches m ON v.id = m.venue_id GROUP BY v.id, v.name, v.city HAVING COUNT(m.id) > 20 ORDER BY total_matches DESC
```

### Result
```json
[
  {
    "venue_id": 8,
    "venue_name": "Eden Gardens",
    "city": "Kolkata",
    "total_matches": 77
  },
  {
    "venue_id": 4,
    "venue_name": "Wankhede Stadium",
    "city": "Mumbai",
    "total_matches": 73
  },
  {
    "venue_id": 3,
    "venue_name": "M Chinnaswamy Stadium",
    "city": "Bangalore",
    "total_matches": 65
  },
  {
    "venue_id": 1,
    "venue_name": "Feroz Shah Kotla",
    "city": "Delhi",
    "total_matches": 60
  },
  {
    "venue_id": 5,
    "venue_name": "Rajiv Gandhi International Stadium, Uppal",
    "city": "Hyderabad",
    "total_matches": 49
  },
  {
    "note": "... and 10 more rows"
  }
]
```

---

## Question 5
### User Query
Show players who have taken more than 150 wickets in their career.

### Explanation
Finds bowlers with over 150 career wickets, including their team information.

### SQL Query
```sql
SELECT ba.player_id, ba.player_name, ba.team_id, ba.team_full_name, SUM(ba.wickets) as total_wickets FROM ipl.bowling_aggregate ba GROUP BY ba.player_id, ba.player_name, ba.team_id, ba.team_full_name HAVING SUM(ba.wickets) > 150 ORDER BY total_wickets DESC
```

### Result
```json
[
  {
    "player_id": "9d430b40",
    "player_name": "SP Narine",
    "team_id": 12,
    "team_full_name": "Kolkata Knight Riders",
    "total_wickets": 180
  },
  {
    "player_id": "a12e1d51",
    "player_name": "SL Malinga",
    "team_id": 4,
    "team_full_name": "Mumbai Indians",
    "total_wickets": 172
  },
  {
    "player_id": "462411b3",
    "player_name": "JJ Bumrah",
    "team_id": 4,
    "team_full_name": "Mumbai Indians",
    "total_wickets": 168
  },
  {
    "player_id": "2e81a32d",
    "player_name": "B Kumar",
    "team_id": 664,
    "team_full_name": "Sunrisers Hyderabad",
    "total_wickets": 157
  }
]
```

---

## Question 6
### User Query
Find all matches that ended in a tie.

### Explanation
Retrieves all matches that ended in a tie, including participating teams and match dates.

### SQL Query
```sql
SELECT m.id as match_id, m.date, t1.id as team1_id, t1.full_name as team1_name, t2.id as team2_id, t2.full_name as team2_name, m.result_type FROM ipl.matches m JOIN ipl.teams t1 ON m.team1_id = t1.id JOIN ipl.teams t2 ON m.team2_id = t2.id WHERE m.result_type = 'tie' ORDER BY m.date DESC
```

### Result
```json
[
  {
    "match_id": 824,
    "date": "2021-04-25",
    "team1_id": 1,
    "team1_name": "Delhi Capitals",
    "team2_id": 664,
    "team2_name": "Sunrisers Hyderabad",
    "result_type": "tie"
  },
  {
    "match_id": 806,
    "date": "2020-10-18",
    "team1_id": 12,
    "team1_name": "Kolkata Knight Riders",
    "team2_id": 664,
    "team2_name": "Sunrisers Hyderabad",
    "result_type": "tie"
  },
  {
    "match_id": 780,
    "date": "2020-10-18",
    "team1_id": 4,
    "team1_name": "Mumbai Indians",
    "team2_id": 2,
    "team2_name": "Punjab Kings",
    "result_type": "tie"
  },
  {
    "match_id": 761,
    "date": "2020-09-28",
    "team1_id": 5,
    "team1_name": "Royal Challengers Bangalore",
    "team2_id": 4,
    "team2_name": "Mumbai Indians",
    "result_type": "tie"
  },
  {
    "match_id": 798,
    "date": "2020-09-20",
    "team1_id": 1,
    "team1_name": "Delhi Capitals",
    "team2_id": 2,
    "team2_name": "Punjab Kings",
    "result_type": "tie"
  },
  {
    "note": "... and 9 more rows"
  }
]
```

---

## Question 7
### User Query
List the top 10 highest individual scores in IPL history.

### Explanation
Displays the top 10 highest individual scores by players in IPL history, including match and innings details.

### SQL Query
```sql
SELECT dbs.match_id, dbs.innings_id, dbs.batter_id, dbs.batter_name, dbs.runs_scored, dbs.balls_faced, dbs.strike_rate FROM ipl.detailed_batting_scorecard dbs ORDER BY dbs.runs_scored DESC, dbs.balls_faced ASC LIMIT 10
```

### Result
```json
[
  {
    "match_id": 330,
    "innings_id": 662,
    "batter_id": "db584dad",
    "batter_name": "CH Gayle",
    "runs_scored": 175,
    "balls_faced": 65,
    "strike_rate": 269.23
  },
  {
    "match_id": 35,
    "innings_id": 69,
    "batter_id": "b8a55852",
    "batter_name": "BB McCullum",
    "runs_scored": 158,
    "balls_faced": 73,
    "strike_rate": 216.44
  },
  {
    "match_id": 920,
    "innings_id": 1867,
    "batter_id": "372455c4",
    "batter_name": "Q de Kock",
    "runs_scored": 140,
    "balls_faced": 70,
    "strike_rate": 200.0
  },
  {
    "match_id": 497,
    "innings_id": 1003,
    "batter_id": "c4487b84",
    "batter_name": "AB de Villiers",
    "runs_scored": 133,
    "balls_faced": 58,
    "strike_rate": 229.31
  },
  {
    "match_id": 760,
    "innings_id": 1535,
    "batter_id": "b17e2f24",
    "batter_name": "KL Rahul",
    "runs_scored": 132,
    "balls_faced": 68,
    "strike_rate": 194.12
  },
  {
    "note": "... and 5 more rows"
  }
]
```

---

## Question 8
### User Query
Show teams with the most championships won.

### Explanation
Lists teams based on the number of championships they have won, including team names and title counts.

### SQL Query
```sql
SELECT t.id as team_id, t.full_name as team_name, COUNT(pt.id) as titles_won FROM ipl.teams t JOIN ipl.points_table pt ON t.id = pt.team_id WHERE pt.winner = TRUE GROUP BY t.id, t.full_name ORDER BY titles_won DESC
```

### Result
```json
[
  {
    "team_id": 3,
    "team_name": "Chennai Super Kings",
    "titles_won": 5
  },
  {
    "team_id": 4,
    "team_name": "Mumbai Indians",
    "titles_won": 5
  },
  {
    "team_id": 12,
    "team_name": "Kolkata Knight Riders",
    "titles_won": 3
  },
  {
    "team_id": 664,
    "team_name": "Sunrisers Hyderabad",
    "titles_won": 1
  },
  {
    "team_id": 14,
    "team_name": "Rajasthan Royals",
    "titles_won": 1
  },
  {
    "note": "... and 2 more rows"
  }
]
```

---

## Question 10
### User Query
Find all centuries scored in IPL matches.

### Explanation
Retrieves all instances where a player scored 100 or more runs in an IPL match, including match details and batting statistics.

### SQL Query
```sql
SELECT m.id as match_id, m.date, dbs.batter_id as player_id, dbs.batter_name as player_name, dbs.runs_scored, dbs.balls_faced, dbs.team as batting_team FROM ipl.detailed_batting_scorecard dbs JOIN ipl.matches m ON dbs.match_id = m.id WHERE dbs.runs_scored >= 100 ORDER BY m.date DESC
```

### Result
```json
[
  {
    "match_id": 1087,
    "date": "2024-05-10",
    "player_id": "d5130a30",
    "player_name": "B Sai Sudharsan",
    "runs_scored": 103,
    "balls_faced": 51,
    "batting_team": "GT"
  },
  {
    "match_id": 1087,
    "date": "2024-05-10",
    "player_id": "b4b99816",
    "player_name": "Shubman Gill",
    "runs_scored": 104,
    "balls_faced": 55,
    "batting_team": "GT"
  },
  {
    "match_id": 1056,
    "date": "2024-05-06",
    "player_id": "271f83cd",
    "player_name": "SA Yadav",
    "runs_scored": 102,
    "balls_faced": 51,
    "batting_team": "MI"
  },
  {
    "match_id": 1035,
    "date": "2024-04-28",
    "player_id": "9caf69a1",
    "player_name": "WG Jacks",
    "runs_scored": 100,
    "balls_faced": 40,
    "batting_team": "RCB"
  },
  {
    "match_id": 1085,
    "date": "2024-04-26",
    "player_id": "abb83e27",
    "player_name": "JM Bairstow",
    "runs_scored": 108,
    "balls_faced": 48,
    "batting_team": "PBKS"
  },
  {
    "note": "... and 96 more rows"
  }
]
```

---

## Question 11
### User Query
List all matches where no team reached 150 runs.

### Explanation
Lists matches where both teams scored less than 150 runs in their respective innings, including team names and scores.

### SQL Query
```sql
SELECT m.id as match_id, m.date, t1.short_name as team1, i1.total_score as team1_score, t2.short_name as team2, i2.total_score as team2_score FROM ipl.matches m JOIN ipl.innings i1 ON m.id = i1.match_id AND i1.innings_number = 1 JOIN ipl.innings i2 ON m.id = i2.match_id AND i2.innings_number = 2 JOIN ipl.teams t1 ON i1.batting_team_id = t1.id JOIN ipl.teams t2 ON i2.batting_team_id = t2.id WHERE i1.total_score < 150 AND i2.total_score < 150 ORDER BY m.date DESC
```

### Result
```json
[
  {
    "match_id": 1032,
    "date": "2024-05-26",
    "team1": "SRH",
    "team1_score": 113,
    "team2": "KKR",
    "team2_score": 114
  },
  {
    "match_id": 1055,
    "date": "2024-05-15",
    "team1": "RR",
    "team1_score": 144,
    "team2": "PBKS",
    "team2_score": 145
  },
  {
    "match_id": 1040,
    "date": "2024-05-12",
    "team1": "RR",
    "team1_score": 141,
    "team2": "CSK",
    "team2_score": 145
  },
  {
    "match_id": 1061,
    "date": "2024-04-30",
    "team1": "MI",
    "team1_score": 144,
    "team2": "LSG",
    "team2_score": 145
  },
  {
    "match_id": 1078,
    "date": "2024-04-21",
    "team1": "PBKS",
    "team1_score": 142,
    "team2": "GT",
    "team2_score": 146
  },
  {
    "note": "... and 287 more rows"
  }
]
```

---

## Question 12
### User Query
Identify players with a strike rate above 180 in the powerplay phase.

### Explanation
Identifies players who have achieved a strike rate above 180 during powerplay overs, with a minimum of 10 balls faced, including total runs and balls faced.

### SQL Query
```sql
SELECT p.id as player_id, p.name as player_name, SUM(d.runs_batter) as total_runs, SUM(CASE WHEN d.is_legal_ball THEN 1 ELSE 0 END) as total_balls_faced, ROUND((SUM(d.runs_batter)::numeric / NULLIF(SUM(CASE WHEN d.is_legal_ball THEN 1 ELSE 0 END), 0)) * 100, 2) as strike_rate FROM ipl.deliveries d JOIN ipl.overs o ON d.over_id = o.id JOIN ipl.innings i ON o.innings_id = i.id JOIN ipl.players p ON d.batter_id = p.id WHERE d.phase = 'powerplay' GROUP BY p.id, p.name HAVING SUM(CASE WHEN d.is_legal_ball THEN 1 ELSE 0 END) >= 10 AND ROUND((SUM(d.runs_batter)::numeric / NULLIF(SUM(CASE WHEN d.is_legal_ball THEN 1 ELSE 0 END), 0)) * 100, 2) > 180 ORDER BY strike_rate DESC
```

### Result
```json
[
  {
    "player_id": "9b6e1b3f",
    "player_name": "J Fraser-McGurk",
    "total_runs": 266,
    "total_balls_faced": 104,
    "strike_rate": 255.77
  },
  {
    "player_id": "bbd41817",
    "player_name": "AD Russell",
    "total_runs": 41,
    "total_balls_faced": 17,
    "strike_rate": 241.18
  },
  {
    "player_id": "0dc00542",
    "player_name": "Shahid Afridi",
    "total_runs": 43,
    "total_balls_faced": 18,
    "strike_rate": 238.89
  },
  {
    "player_id": "12b610c2",
    "player_name": "TM Head",
    "total_runs": 412,
    "total_balls_faced": 208,
    "strike_rate": 198.08
  }
]
```

---

## Question 13
### User Query
Retrieve matches where the winning team chased down a target under 20 overs.

### Explanation
Fetches matches where the winning team successfully chased the target in less than 20 overs, including match and team details.

### SQL Query
```sql
SELECT m.id as match_id, m.date, tw.short_name as winning_team, tw.id as winning_team_id, i2.total_score as chase_score, o.over_number FROM ipl.matches m JOIN ipl.innings i1 ON m.id = i1.match_id AND i1.innings_number = 1 JOIN ipl.innings i2 ON m.id = i2.match_id AND i2.innings_number = 2 JOIN ipl.teams tw ON m.winner_id = tw.id JOIN ipl.overs o ON i2.id = o.innings_id WHERE i2.total_score >= i1.total_score AND o.over_number < 20 ORDER BY m.date DESC
```

### Result
```json
[
  {
    "match_id": 1032,
    "date": "2024-05-26",
    "winning_team": "KKR",
    "winning_team_id": 12,
    "chase_score": 114,
    "over_number": 0
  },
  {
    "match_id": 1032,
    "date": "2024-05-26",
    "winning_team": "KKR",
    "winning_team_id": 12,
    "chase_score": 114,
    "over_number": 1
  },
  {
    "match_id": 1032,
    "date": "2024-05-26",
    "winning_team": "KKR",
    "winning_team_id": 12,
    "chase_score": 114,
    "over_number": 2
  },
  {
    "match_id": 1032,
    "date": "2024-05-26",
    "winning_team": "KKR",
    "winning_team_id": 12,
    "chase_score": 114,
    "over_number": 3
  },
  {
    "match_id": 1032,
    "date": "2024-05-26",
    "winning_team": "KKR",
    "winning_team_id": 12,
    "chase_score": 114,
    "over_number": 4
  },
  {
    "note": "... and 10756 more rows"
  }
]
```

---

## Question 14
### User Query
List matches where a player took more than 5 wickets in an innings.

### Explanation
Retrieves matches where a bowler took more than five wickets in a single innings, including match, bowler, and both teams' details.

### SQL Query
```sql
SELECT dbs.match_id, dbs.innings_id, dbs.bowler_id, dbs.bowler_name, dbs.bowling_team, dbs.team_id as bowling_team_id, t_batting.short_name as batting_team, t_batting.id as batting_team_id, dbs.wickets, dbs.overs_bowled, dbs.runs_conceded, dbs.economy_rate FROM ipl.detailed_bowling_scorecard dbs JOIN ipl.innings i ON dbs.innings_id = i.id JOIN ipl.teams t_batting ON i.batting_team_id = t_batting.id WHERE dbs.wickets > 5 ORDER BY dbs.wickets DESC, dbs.economy_rate ASC
```

### Result
```json
[
  {
    "match_id": 1004,
    "innings_id": 2035,
    "bowler_id": "4bd09374",
    "bowler_name": "Akash Madhwal",
    "bowling_team": "MI",
    "bowling_team_id": 4,
    "batting_team": "LSG",
    "batting_team_id": 1760,
    "wickets": 6,
    "overs_bowled": "3.3",
    "runs_conceded": 5,
    "economy_rate": 1.43
  },
  {
    "match_id": 709,
    "innings_id": 1430,
    "bowler_id": "b0946605",
    "bowler_name": "AS Joseph",
    "bowling_team": "MI",
    "bowling_team_id": 4,
    "batting_team": "SRH",
    "batting_team_id": 664,
    "wickets": 6,
    "overs_bowled": "3.4",
    "runs_conceded": 12,
    "economy_rate": 3.27
  },
  {
    "match_id": 32,
    "innings_id": 63,
    "bowler_id": "64d43928",
    "bowler_name": "Sohail Tanvir",
    "bowling_team": "RR",
    "bowling_team_id": 14,
    "batting_team": "CSK",
    "batting_team_id": 3,
    "wickets": 6,
    "overs_bowled": "4.0",
    "runs_conceded": 14,
    "economy_rate": 3.5
  },
  {
    "match_id": 528,
    "innings_id": 1065,
    "bowler_id": "14f96089",
    "bowler_name": "A Zampa",
    "bowling_team": "RPS",
    "bowling_team_id": 1036,
    "batting_team": "SRH",
    "batting_team_id": 664,
    "wickets": 6,
    "overs_bowled": "4.0",
    "runs_conceded": 19,
    "economy_rate": 4.75
  },
  {
    "match_id": 531,
    "innings_id": 1072,
    "bowler_id": "bbd41817",
    "bowler_name": "AD Russell",
    "bowling_team": "KKR",
    "bowling_team_id": 12,
    "batting_team": "PBKS",
    "batting_team_id": 2,
    "wickets": 6,
    "overs_bowled": "4.0",
    "runs_conceded": 20,
    "economy_rate": 5.0
  },
  {
    "note": "... and 3 more rows"
  }
]
```

---

## Question 15
### User Query
Retrieve matches that had a super over due to a tie.

### Explanation
Lists matches that were decided by a super over following a tie, including team names and super over details.

### SQL Query
```sql
SELECT m.id as match_id, m.date, t1.short_name as team1, t2.short_name as team2, m.winner_id, so.batting_team_id as super_over_batting_team, so.total_score as super_over_score FROM ipl.matches m JOIN ipl.innings i1 ON m.id = i1.match_id AND i1.innings_number = 1 JOIN ipl.innings i2 ON m.id = i2.match_id AND i2.innings_number = 2 JOIN ipl.innings so ON m.id = so.match_id AND so.is_super_over = TRUE JOIN ipl.teams t1 ON i1.batting_team_id = t1.id JOIN ipl.teams t2 ON i2.batting_team_id = t2.id WHERE m.super_over = TRUE AND m.result_type = 'tie' ORDER BY m.date DESC
```

### Result
```json
[
  {
    "match_id": 824,
    "date": "2021-04-25",
    "team1": "DC",
    "team2": "SRH",
    "winner_id": 1,
    "super_over_batting_team": 664,
    "super_over_score": 7
  },
  {
    "match_id": 824,
    "date": "2021-04-25",
    "team1": "DC",
    "team2": "SRH",
    "winner_id": 1,
    "super_over_batting_team": 1,
    "super_over_score": 8
  },
  {
    "match_id": 780,
    "date": "2020-10-18",
    "team1": "MI",
    "team2": "PBKS",
    "winner_id": 2,
    "super_over_batting_team": 2,
    "super_over_score": 15
  },
  {
    "match_id": 806,
    "date": "2020-10-18",
    "team1": "KKR",
    "team2": "SRH",
    "winner_id": 12,
    "super_over_batting_team": 12,
    "super_over_score": 3
  },
  {
    "match_id": 806,
    "date": "2020-10-18",
    "team1": "KKR",
    "team2": "SRH",
    "winner_id": 12,
    "super_over_batting_team": 664,
    "super_over_score": 2
  },
  {
    "note": "... and 25 more rows"
  }
]
```

---

## Question 16
### User Query
Find venues where more than 30 matches have been played.

### Explanation
Identifies venues that have hosted over 30 IPL matches, including venue names and locations.

### SQL Query
```sql
SELECT v.id as venue_id, v.name as venue_name, v.city, COUNT(m.id) as total_matches FROM ipl.venues v JOIN ipl.matches m ON v.id = m.venue_id GROUP BY v.id, v.name, v.city HAVING COUNT(m.id) > 30 ORDER BY total_matches DESC
```

### Result
```json
[
  {
    "venue_id": 8,
    "venue_name": "Eden Gardens",
    "city": "Kolkata",
    "total_matches": 77
  },
  {
    "venue_id": 4,
    "venue_name": "Wankhede Stadium",
    "city": "Mumbai",
    "total_matches": 73
  },
  {
    "venue_id": 3,
    "venue_name": "M Chinnaswamy Stadium",
    "city": "Bangalore",
    "total_matches": 65
  },
  {
    "venue_id": 1,
    "venue_name": "Feroz Shah Kotla",
    "city": "Delhi",
    "total_matches": 60
  },
  {
    "venue_id": 5,
    "venue_name": "Rajiv Gandhi International Stadium, Uppal",
    "city": "Hyderabad",
    "total_matches": 49
  },
  {
    "note": "... and 5 more rows"
  }
]
```

---

## Question 17
### User Query
Identify the top 3 highest individual scores in IPL finals.

### Explanation
Lists the top three highest individual scores made in IPL final matches, including player and match details.

### SQL Query
```sql
SELECT dbs.batter_id, p.name as batter_name, m.id as match_id, m.date, dbs.runs_scored, dbs.balls_faced FROM ipl.detailed_batting_scorecard dbs JOIN ipl.matches m ON dbs.match_id = m.id JOIN ipl.players p ON dbs.batter_id = p.id WHERE m.stage = 'Final' ORDER BY dbs.runs_scored DESC, dbs.balls_faced ASC LIMIT 3
```

### Result
```json
[
  {
    "batter_id": "4329fbb5",
    "batter_name": "SR Watson",
    "match_id": 670,
    "date": "2018-05-27",
    "runs_scored": 117,
    "balls_faced": 57
  },
  {
    "batter_id": "fe11caa6",
    "batter_name": "WP Saha",
    "match_id": 434,
    "date": "2014-06-01",
    "runs_scored": 115,
    "balls_faced": 55
  },
  {
    "batter_id": "d5130a30",
    "batter_name": "B Sai Sudharsan",
    "match_id": 955,
    "date": "2023-05-29",
    "runs_scored": 96,
    "balls_faced": 47
  }
]
```

---

## Question 18
### User Query
Average first innings powerplay score in IPL.

### Explanation
Calculates the average score made during the powerplay phase of the first innings across all IPL matches.

### SQL Query
```sql
SELECT AVG(p.runs) as avg_powerplay_score FROM ipl.phases p JOIN ipl.innings i ON p.innings_id = i.id JOIN ipl.matches m ON i.match_id = m.id WHERE p.phase_type = 'powerplay' AND i.innings_number = 1
```

### Result
```json
[
  {
    "avg_powerplay_score": 46.19269406392694
  }
]
```

---

