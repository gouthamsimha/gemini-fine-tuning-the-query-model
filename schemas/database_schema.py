CRICKET_SCHEMA = """
Database Schema:
-- current schema is ipl
-- Consider adding a schema version and metadata header
/*
Schema Name: IPL Cricket Database
Version: 1.0
Last Updated: 2024-11-17
Description: Database schema for storing Indian Premier League cricket match data
*/

-- Leagues Table which contains the specific league details
CREATE TABLE ipl.leagues (
    id INTEGER PRIMARY KEY, -- This is the league ID
    name VARCHAR(100),    -- The full name of the league
    short_name VARCHAR(10), -- The short name of the league
    country VARCHAR(50),   -- The country where the league is played
    governing_body VARCHAR(100), -- The governing body of the league
    year_founded INTEGER, -- The year the league was founded
    valuation DECIMAL(10, 2), -- The valuation of the league
    number_of_teams INTEGER, -- The number of teams in the league
    current_champion VARCHAR(100), -- The current champion of the league
    most_successful_team VARCHAR(100), -- The most successful team in the league
    title_sponsor VARCHAR(100), -- The title sponsor of the league
    format VARCHAR(20), -- The format of the league
    gender VARCHAR(10), -- The gender of the league
    inaugural_season INTEGER, -- The inaugural season of the league
    logo VARCHAR(255), -- The logo of the league
    match_type VARCHAR(20), -- The type of match played in the league
    overs INTEGER, -- The number of overs in the league
    tournament VARCHAR(100),
    website VARCHAR(255)
);

-- Seasons Table which contains the specific season details
CREATE TABLE ipl.seasons (
    id SERIAL PRIMARY KEY, -- This is the season ID
    year INT, -- The year of the season
    league_id INT REFERENCES ipl.leagues(id) -- The league ID that the season belongs to
);

CREATE TABLE ipl.teams (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) UNIQUE, -- The full name of the team
    short_name VARCHAR(10), -- The short name of the team
    home_venue VARCHAR(100), -- The home venue of the team
    city VARCHAR(50), -- The city where the team is based
    state VARCHAR(50), -- The state where the team is based
    country VARCHAR(50), -- The country where the team is based
    founded_year INTEGER, -- The year the team was founded
    team_colors VARCHAR(100), -- The colors of the team
    logo_url VARCHAR(255), -- The URL of the team's logo
    website_url VARCHAR(255), -- The URL of the team's website
    owner VARCHAR(100), -- The owner of the team
    twitter_handle VARCHAR(50), -- The Twitter handle of the team
    instagram_handle VARCHAR(50), -- The Instagram handle of the team
    facebook_url VARCHAR(255), -- The Facebook URL of the team
    first_participation_year INTEGER, -- The year the team first participated in the league
    status VARCHAR(20), -- The status of the team
    titles_won INTEGER -- The number of titles the team has won
);

-- Players Table which contains the player details
CREATE TABLE ipl.players (
    id VARCHAR(16) PRIMARY KEY,
    name VARCHAR(100), -- The name of the player
    full_name VARCHAR(150), -- The full name of the player
    dob DATE, -- The date of birth of the player
    country VARCHAR(50), -- The country where the player was born
    batting_style VARCHAR(20), -- The batting style of the player
    bowling_style VARCHAR(50), -- The bowling style of the player
    player_type VARCHAR(30), -- The type of player
    birth_place VARCHAR(100), -- The place where the player was born
    age TEXT GENERATED ALWAYS AS (calculate_age(dob)) STORED -- The age of the player
);

-- Venues Table which contains the venue details
CREATE TABLE ipl.venues (
    id SERIAL PRIMARY KEY, -- This is the venue ID
    name VARCHAR(100), -- The name of the venue
    city VARCHAR(50), -- The city where the venue is located
    country VARCHAR(50) -- The country where the venue is located
);

-- Match Officials Table which contains the match official details
CREATE TABLE ipl.match_officials (
    id SERIAL PRIMARY KEY, -- This is the match official ID
    match_referee VARCHAR(50), -- The match referee
    reserve_umpire VARCHAR(50), -- The reserve umpire
    tv_umpire VARCHAR(50), -- The TV umpire
    umpire1 VARCHAR(50), -- The first umpire
    umpire2 VARCHAR(50) -- The second umpire
);

-- Matches Table which contains the match details
CREATE TABLE ipl.matches (
    id SERIAL PRIMARY KEY, -- This is the match ID
    season_id INT REFERENCES ipl.seasons(id), -- The season ID that the match belongs to
    venue_id INT REFERENCES ipl.venues(id), -- The venue ID that the match is played at
    date DATE, -- The date of the match
    match_number INT, -- The match number
    stage VARCHAR(50), -- The stage of the match. Possible values are 'group', 'playoff'
    is_playoff BOOLEAN, -- Whether the match is a playoff match. Possible values are TRUE, FALSE
    team1_id INT REFERENCES ipl.teams(id), -- The ID of the first team 
    team2_id INT REFERENCES ipl.teams(id), -- The ID of the second team
    toss_winner_id INT REFERENCES ipl.teams(id), -- The ID of the team that won the toss
    toss_decision VARCHAR(5), -- The decision of the toss
    result_type VARCHAR(20), -- The type of result of the match. Possible values are 'normal', 'tie', 'no result'
    win_margin INT, -- The margin of the match. This is only applicable if the result type is 'normal'
    win_margin_type VARCHAR(20), -- The type of margin of the match
    super_over BOOLEAN, -- Whether the match had a super over. Possible values are TRUE, FALSE
    winner_id INT REFERENCES ipl.teams(id), -- The ID of the winning team       
    player_of_match_id VARCHAR(16) REFERENCES ipl.players(id), -- The ID of the player of the match
    dls_applied BOOLEAN DEFAULT FALSE, -- Whether the match had a DLS applied. Possible values are TRUE, FALSE
    no_result_reason VARCHAR(50), -- The reason for no result. This is only applicable if the result type is 'no result'    
    match_officials_id INT REFERENCES ipl.match_officials(id) -- The ID of the match officials
);

-- Innings Table which contains the innings details. first innings or second innings and sometimes third, fourthinnings in case of super over
CREATE TABLE ipl.innings (
    id SERIAL PRIMARY KEY, -- This is the innings ID
    match_id INT REFERENCES ipl.matches(id), -- The match ID that the innings belongs to
    innings_number INT, -- The innings number. Possible values are 1, 2, 3, 4
    batting_team_id INT REFERENCES ipl.teams(id), -- The ID of the batting team
    bowling_team_id INT REFERENCES ipl.teams(id), -- The ID of the bowling team
    is_super_over BOOLEAN, -- Whether the innings is a super over. Possible values are TRUE, FALSE
    total_score INT DEFAULT 0, -- The total score of the innings
    wickets INT DEFAULT 0, -- The number of wickets fallen
    overs INT DEFAULT 0, -- The number of overs bowled
    balls INT DEFAULT 0, -- The number of balls bowled
    total_extras INT DEFAULT 0, -- The total number of extras conceded
    wides INT DEFAULT 0, -- The number of wides conceded
    noballs INT DEFAULT 0, -- The number of no balls conceded
    byes INT DEFAULT 0, -- The number of byes conceded
    legbyes INT DEFAULT 0 -- The number of leg byes conceded
);

-- Phases Table which contains the phase details. powerplay, middle, death
CREATE TABLE ipl.phases (
    innings_id INT REFERENCES ipl.innings(id), -- The innings ID that the phase belongs to. Phases = middle_overs, powerplay, death_overs
    phase_type VARCHAR(20), -- The type of phase
    runs INT, -- The number of runs scored in the phase
    balls INT, -- The number of balls faced in the phase
    wickets INT, -- The number of wickets fallen in the phase
    PRIMARY KEY (innings_id, phase_type) -- The primary key is a composite key of the innings ID and the phase type
);

-- Overs Table which contains the over details
CREATE TABLE ipl.overs (
    id SERIAL PRIMARY KEY, -- This is the over ID
    innings_id INT REFERENCES ipl.innings(id), -- The innings ID that the over belongs to
    over_number INT, -- The over number
    bowler_id VARCHAR(16) REFERENCES ipl.players(id), -- The ID of the bowler
    balls_bowled INT DEFAULT 0 -- The number of balls bowled in the over
);

-- Deliveries Table which contains the delivery details
CREATE TABLE ipl.deliveries (
    id SERIAL PRIMARY KEY, -- This is the delivery ID
    over_id INT REFERENCES ipl.overs(id), -- The over ID that the delivery belongs to
    ball_number INT, -- The ball number. Possible values are 1, 2, 3, 4, 5, 6
    batter_id VARCHAR(16) REFERENCES ipl.players(id), -- The ID of the batter
    bowler_id VARCHAR(16) REFERENCES ipl.players(id), -- The ID of the bowler
    non_striker_id VARCHAR(16) REFERENCES ipl.players(id), -- The ID of the non striker
    runs_batter INT, -- The number of runs scored by the batter.
    runs_extras INT, -- The number of runs scored by extras. 
    runs_total INT, -- The total number of runs scored in the delivery
    is_wicket BOOLEAN, -- Whether the delivery resulted in a wicket
    phase VARCHAR(20), -- The phase of the delivery. Possible values are 'powerplay', 'middle', 'death'
    is_wide BOOLEAN DEFAULT FALSE, -- Whether the delivery was a wide. Possible values are TRUE, FALSE
    is_no_ball BOOLEAN DEFAULT FALSE, -- Whether the delivery was a no ball. Possible values are TRUE, FALSE
    byes INT DEFAULT 0, -- The number of byes conceded
    legbyes INT DEFAULT 0, -- The number of leg byes conceded
    is_legal_ball BOOLEAN DEFAULT TRUE, -- Whether the delivery was a legal ball. Possible values are TRUE, FALSE
    dismissed_player_id VARCHAR(16) REFERENCES ipl.players(id) -- The ID of the player dismissed
);

-- Extra Runs Table which contains the extra runs details
CREATE TABLE ipl.extra_runs (
    id SERIAL PRIMARY KEY, -- This is the extra runs ID
    delivery_id INT REFERENCES ipl.deliveries(id), -- The delivery ID that the extra runs belongs to
    type VARCHAR(10), -- The type of extra runs. Possible values are 'byes', 'legbyes'
    runs INT -- The number of extra runs
);

-- Wickets Table which contains the wicket details
CREATE TABLE ipl.wickets (
    id SERIAL PRIMARY KEY, -- This is the wicket ID
    delivery_id INT REFERENCES ipl.deliveries(id), -- The delivery ID that the wicket belongs to
    player_out_id VARCHAR(16) REFERENCES ipl.players(id), -- The ID of the player dismissed
    kind VARCHAR(50), -- The kind of dismissal. Possible values are 'caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wicket', 'obstructing the field', 'run out', 'hit ball twice', 'handled ball', 'timed out', 'retired hurt', 'obstructing the field', 'hit by ball', 'retired out', 'hit the ball twice', 'hit the wicket', 'stumped', 'caught', 'bowled', 'lbw', 'caught and bowled'
    fielder1_id VARCHAR(16) REFERENCES ipl.players(id), -- The ID of the first fielder
    fielder2_id VARCHAR(16) REFERENCES ipl.players(id) -- The ID of the second fielder
);      

-- Player Match Performance Table which contains the player match performance details
CREATE TABLE ipl.player_match_performance (
    id SERIAL PRIMARY KEY, -- This is the player match performance ID
    match_id INT REFERENCES ipl.matches(id), -- The match ID that the player match performance belongs to
    player_id VARCHAR(16) REFERENCES ipl.players(id), -- The ID of the player
    team_id INT REFERENCES ipl.teams(id), -- The ID of the team
    batting_position INT, -- The batting position of the player
    batting_position_category VARCHAR(20), -- The batting position category of the player. Possible values are 'not out', 'out', 'retired'
    is_impact_player BOOLEAN DEFAULT FALSE, -- Whether the player is an impact player. Possible values are TRUE, FALSE  
    impact_sub_time VARCHAR(10), -- The time of the impact substitution
    did_bat BOOLEAN DEFAULT FALSE, -- Whether the player batted in the match. Possible values are TRUE, FALSE
    did_bowl BOOLEAN DEFAULT FALSE, -- Whether the player bowled in the match. Possible values are TRUE, FALSE
    CONSTRAINT unique_player_match UNIQUE (match_id, player_id) -- The primary key is a composite key of the match ID and the player ID
);

-- DRS Reviews Table which contains the DRS review details
CREATE TABLE ipl.drs_reviews (
    id SERIAL PRIMARY KEY, -- This is the DRS review ID
    delivery_id INT REFERENCES ipl.deliveries(id), -- The delivery ID that the DRS review belongs to
    reviewing_team_id INT REFERENCES ipl.teams(id), -- The ID of the team that reviewed the delivery
    umpire VARCHAR(100), -- The umpire who reviewed the delivery
    batter_reviewed_id VARCHAR(16) REFERENCES ipl.players(id), -- The ID of the player who was reviewed
    decision VARCHAR(50), -- The decision of the DRS review. Possible values are 'hit wicket', 'caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'not out', 'no ball', 'wide', 'no delivery'
    review_type VARCHAR(50), -- The type of DRS review. Possible values are 'batter', 'bowler'
    umpires_call BOOLEAN
);

-- Batting Aggregate Table which contains the batting aggregate details for the whole individual season. 
CREATE TABLE IF NOT EXISTS ipl.batting_aggregate (
    player_id VARCHAR(16) NOT NULL, -- The ID of the player
    player_name VARCHAR(100) NOT NULL, -- The name of the player
    team_id INT NOT NULL, -- The ID of the team
    team_full_name VARCHAR(100) NOT NULL, -- The full name of the team
    season_id INT NOT NULL, -- The ID of the season
    season_year INT NOT NULL, -- The year of the season
    matches_played INT DEFAULT 0, -- The number of matches played
    innings_played INT DEFAULT 0, -- The number of innings played
    total_runs INT DEFAULT 0, -- The total number of runs scored
    balls_faced INT DEFAULT 0, -- The total number of balls faced
    strike_rate DECIMAL(5,2) DEFAULT 0.00, -- The strike rate of the player
    avg DECIMAL(5,2) DEFAULT 0.00, -- The average of the player
    highest_score INT DEFAULT 0, -- The highest score of the player
    thirties INT DEFAULT 0, -- The number of thirties scored
    fifties INT DEFAULT 0, -- The number of fifties scored
    hundreds INT DEFAULT 0, -- The number of hundreds scored
    fours INT DEFAULT 0, -- The number of fours scored
    sixes INT DEFAULT 0, -- The number of sixes scored
    duck_outs INT DEFAULT 0, -- The number of duck outs
    not_outs INT DEFAULT 0, -- The number of not outs
    dot_balls INT DEFAULT 0, -- The number of dot balls faced   
    dot_ball_pct DECIMAL(5,2) DEFAULT 0.00, -- The dot ball percentage
    powerplay_strike_rate DECIMAL(5,2) DEFAULT 0.00, -- The strike rate in the powerplay
    middle_over_strike_rate DECIMAL(5,2) DEFAULT 0.00, -- The strike rate in the middle overs
    death_over_strike_rate DECIMAL(5,2) DEFAULT 0.00, -- The strike rate in the death overs
    PRIMARY KEY (player_id, season_id, team_id), -- The primary key is a composite key of the player ID, season ID, and team ID
    FOREIGN KEY (player_id) REFERENCES ipl.players(id), -- The foreign key constraint for the player ID
    FOREIGN KEY (team_id) REFERENCES ipl.teams(id), -- The foreign key constraint for the team ID
    FOREIGN KEY (season_id) REFERENCES ipl.seasons(id) -- The foreign key constraint for the season ID
);


-- Bowling Aggregate Table which contains the bowling aggregate details for the whole individual season. 
CREATE TABLE IF NOT EXISTS ipl.bowling_aggregate (
    player_id VARCHAR(16) NOT NULL, -- The ID of the player
    player_name VARCHAR(100) NOT NULL, -- The name of the player
    team_id INT NOT NULL, -- The ID of the team
    team_full_name VARCHAR(100) NOT NULL, -- The full name of the team
    season_id INT NOT NULL, -- The ID of the season
    season_year INT NOT NULL, -- The year of the season
    matches_played INT DEFAULT 0, -- The number of matches played
    innings_bowled INT DEFAULT 0, -- The number of innings bowled
    overs_bowled DECIMAL(5,1) DEFAULT 0.0, -- The number of overs bowled
    balls_bowled INT DEFAULT 0, -- The number of balls bowled
    maidens INT DEFAULT 0, -- The number of maidens bowled
    runs_conceded INT DEFAULT 0, -- The total number of runs conceded
    wickets INT DEFAULT 0, -- The number of wickets taken
    economy DECIMAL(5,2) DEFAULT 0.00, -- The economy rate of the player
    average DECIMAL(5,2) DEFAULT 0.00, -- The average of the player
    strike_rate DECIMAL(5,2) DEFAULT 0.00, -- The strike rate of the player
    dot_balls INT DEFAULT 0, -- The number of dot balls faced
    dot_ball_percentage DECIMAL(5,2) DEFAULT 0.00, -- The dot ball percentage
    boundaries_conceded INT DEFAULT 0, -- The number of boundaries conceded
    sixes_conceded INT DEFAULT 0, -- The number of sixes conceded
    wides INT DEFAULT 0, -- The number of wides conceded
    no_balls INT DEFAULT 0, -- The number of no balls conceded
    powerplay_wickets INT DEFAULT 0, -- The number of wickets taken in the powerplay
    powerplay_economy DECIMAL(5,2) DEFAULT 0.00, -- The economy rate in the powerplay
    middle_overs_wickets INT DEFAULT 0, -- The number of wickets taken in the middle overs
    middle_overs_economy DECIMAL(5,2) DEFAULT 0.00, -- The economy rate in the middle overs
    death_overs_wickets INT DEFAULT 0, -- The number of wickets taken in the death overs
    death_overs_economy DECIMAL(5,2) DEFAULT 0.00, -- The economy rate in the death overs
    three_wicket_hauls INT DEFAULT 0, -- The number of three wicket hauls
    four_wicket_hauls INT DEFAULT 0, -- The number of four wicket hauls 
    five_wicket_hauls INT DEFAULT 0, -- The number of five wicket hauls
    best_bowling VARCHAR(10) DEFAULT '0/0', -- The best bowling figures of the player
    PRIMARY KEY (player_id, season_id, team_id), -- The primary key is a composite key of the player ID, season ID, and team ID
    FOREIGN KEY (player_id) REFERENCES ipl.players(id), -- The foreign key constraint for the player ID
    FOREIGN KEY (team_id) REFERENCES ipl.teams(id), -- The foreign key constraint for the team ID
    FOREIGN KEY (season_id) REFERENCES ipl.seasons(id) -- The foreign key constraint for the season ID
);

-- Detailed Batting Scorecard materialized view which contains the detailed batting scorecard details for the whole individual match. 
CREATE MATERIALIZED VIEW ipl.detailed_batting_scorecard AS
WITH dismissal_info AS (
    SELECT DISTINCT ON (d.batter_id, m.id, i.id)
        m.id as match_id, -- The ID of the match
        i.id as innings_id, -- The ID of the innings    
        CASE 
            WHEN w.kind = 'run out' THEN w.player_out_id -- The ID of the player dismissed if the dismissal type is run out 
            ELSE d.batter_id -- The ID of the batter otherwise  
        END as batter_id,
        w.kind as dismissal_type, -- The type of dismissal
        f1.name as fielder1_name, -- The name of the first fielder
        f1.id as fielder1_id, -- The ID of the first fielder
        f2.name as fielder2_name, -- The name of the second fielder
        f2.id as fielder2_id, -- The ID of the second fielder
        b.name as bowler_name, -- The name of the bowler
        b.id as bowler_id, -- The ID of the bowler
        CONCAT(o.over_number, '.', d.ball_number) as dismissal_over -- The over and ball number of the dismissal
    FROM ipl.matches m
    JOIN ipl.innings i ON i.match_id = m.id
    JOIN ipl.overs o ON o.innings_id = i.id
    JOIN ipl.deliveries d ON d.over_id = o.id
    LEFT JOIN ipl.wickets w ON w.delivery_id = d.id
    LEFT JOIN ipl.players f1 ON f1.id = w.fielder1_id
    LEFT JOIN ipl.players f2 ON f2.id = w.fielder2_id
    LEFT JOIN ipl.players b ON b.id = o.bowler_id
    WHERE w.kind IS NOT NULL
),
batting_position AS (
    SELECT DISTINCT ON (m.id, i.id, d.batter_id)
        m.id as match_id,
        i.id as innings_id,
        d.batter_id,                
        ROW_NUMBER() OVER (PARTITION BY m.id, i.id, i.batting_team_id ORDER BY MIN(o.over_number), MIN(d.ball_number)) as position
    FROM ipl.matches m
    JOIN ipl.innings i ON i.match_id = m.id
    JOIN ipl.overs o ON o.innings_id = i.id
    JOIN ipl.deliveries d ON d.over_id = o.id
    GROUP BY m.id, i.id, i.batting_team_id, d.batter_id
)
SELECT DISTINCT ON (m.id, i.id, d.batter_id)
    m.id as match_id, -- The ID of the match
    i.id as innings_id, -- The ID of the innings
    i.innings_number, -- The innings number
    i.is_super_over, -- Whether the innings is a super over
    m.super_over as match_had_super_over, -- Whether the match had a super over
    d.batter_id, -- The ID of the batter
    p.name as batter_name, -- The name of the batter
    t.short_name as team, -- The short name of the team
    t.id as team_id, -- The ID of the team
    bp.position as batting_position, -- The batting position of the player
    COUNT(CASE WHEN d.is_legal_ball = true THEN 1 END) as balls_faced, -- The number of balls faced
    SUM(d.runs_batter) as runs_scored, -- The number of runs scored
    COUNT(CASE WHEN d.runs_batter = 0 AND d.is_legal_ball = true THEN 1 END) as dot_balls, -- The number of dot balls faced
    COUNT(CASE WHEN d.runs_batter = 1 THEN 1 END) as singles, -- The number of singles scored
    COUNT(CASE WHEN d.runs_batter = 2 THEN 1 END) as doubles, -- The number of doubles scored
    COUNT(CASE WHEN d.runs_batter = 3 THEN 1 END) as triples, -- The number of triples scored
    COUNT(CASE WHEN d.runs_batter = 4 THEN 1 END) as fours, -- The number of fours scored
    COUNT(CASE WHEN d.runs_batter = 6 THEN 1 END) as sixes, -- The number of sixes scored
    ROUND(SUM(d.runs_batter) * 100.0 / NULLIF(COUNT(CASE WHEN d.is_legal_ball = true THEN 1 END), 0), 2) as strike_rate, -- The strike rate of the player
    COUNT(CASE WHEN d.is_wide = true THEN 1 END) as wides_faced, -- The number of wides faced
    COUNT(CASE WHEN d.is_no_ball = true THEN 1 END) as no_balls_faced, -- The number of no balls faced
    SUM(d.byes) as byes, -- The number of byes conceded
    SUM(d.legbyes) as legbyes, -- The number of leg byes conceded
    SUM(CASE WHEN d.phase = 'powerplay' THEN d.runs_batter ELSE 0 END) as powerplay_runs, -- The number of runs scored in the powerplay
    SUM(CASE WHEN d.phase = 'middle' THEN d.runs_batter ELSE 0 END) as middle_overs_runs,
    SUM(CASE WHEN d.phase = 'death' THEN d.runs_batter ELSE 0 END) as death_overs_runs,
    di.dismissal_type, -- The type of dismissal
    di.fielder1_name, -- The name of the first fielder
    di.fielder1_id, -- The ID of the first fielder
    di.fielder2_name, -- The name of the second fielder
    di.fielder2_id, -- The ID of the second fielder
    di.bowler_name, -- The name of the bowler
    di.bowler_id, -- The ID of the bowler
    di.dismissal_over, -- The over and ball number of the dismissal
    pmr.is_captain, -- Whether the player is the captain of the team
    pmr.is_wicket_keeper, -- Whether the player is the wicket keeper of the team
    pmp.is_impact_player, -- Whether the player is an impact player
    pmp.impact_sub_time, -- The time of the impact substitution
    pmp.batting_position as intended_batting_position, -- The intended batting position of the player
    pmp.batting_position_category -- The batting position category of the player
FROM ipl.matches m
JOIN ipl.innings i ON i.match_id = m.id
JOIN ipl.overs o ON o.innings_id = i.id
JOIN ipl.deliveries d ON d.over_id = o.id
JOIN ipl.players p ON p.id = d.batter_id
JOIN ipl.teams t ON t.id = i.batting_team_id
LEFT JOIN dismissal_info di ON di.match_id = m.id AND di.innings_id = i.id AND di.batter_id = d.batter_id
LEFT JOIN batting_position bp ON bp.match_id = m.id AND bp.innings_id = i.id AND bp.batter_id = d.batter_id
LEFT JOIN ipl.player_match_roles pmr ON pmr.match_id = m.id AND pmr.player_id = d.batter_id
LEFT JOIN ipl.player_match_performance pmp ON pmp.match_id = m.id AND pmp.player_id = d.batter_id
GROUP BY 
    m.id, -- The ID of the match
    i.id, -- The ID of the innings
    i.innings_number, -- The innings number
    i.is_super_over, -- Whether the innings is a super over
    m.super_over, -- Whether the match had a super over
    d.batter_id, -- The ID of the batter
    p.name, -- The name of the batter
    t.short_name, -- The short name of the team
    t.id, -- The ID of the team
    bp.position, -- The batting position of the player
    di.dismissal_type, -- The type of dismissal
    di.fielder1_name, -- The name of the first fielder
    di.fielder1_id, -- The ID of the first fielder
    di.fielder2_name, -- The name of the second fielder
    di.fielder2_id, -- The ID of the second fielder
    di.bowler_name, -- The name of the bowler
    di.bowler_id, -- The ID of the bowler
    di.dismissal_over, -- The over and ball number of the dismissal
    pmr.is_captain, -- Whether the player is the captain of the team
    pmr.is_wicket_keeper, -- Whether the player is the wicket keeper of the team
    pmp.is_impact_player, -- Whether the player is an impact player
    pmp.impact_sub_time, -- The time of the impact substitution
    pmp.batting_position, -- The batting position of the player
    pmp.batting_position_category -- The batting position category of the player
ORDER BY m.id, i.id, d.batter_id, bp.position; -- Order the results by match ID, innings ID, batter ID, and batting position


-- Detailed Bowling Scorecard materialized view which contains the detailed bowling scorecard details for the whole individual match. 
CREATE MATERIALIZED VIEW ipl.detailed_bowling_scorecard AS
WITH bowling_spells AS (
    SELECT 
        m.id as match_id, -- The ID of the match
        i.id as innings_id, -- The ID of the innings
        o.bowler_id, -- The ID of the bowler
        CONCAT(MIN(o.over_number), '.', MIN(d.ball_number)) as spell_start, -- The start of the spell
        CONCAT(MAX(o.over_number), '.', MAX(d.ball_number)) as spell_end -- The end of the spell
    FROM ipl.matches m  
    JOIN ipl.innings i ON i.match_id = m.id
    JOIN ipl.overs o ON o.innings_id = i.id
    JOIN ipl.deliveries d ON d.over_id = o.id
    GROUP BY m.id, i.id, o.bowler_id
)
SELECT DISTINCT ON (m.id, i.id, o.bowler_id)
    m.id as match_id, -- The ID of the match
    i.id as innings_id, -- The ID of the innings
    i.innings_number, -- The innings number
    i.is_super_over, -- Whether the innings is a super over
    m.super_over as match_had_super_over, -- Whether the match had a super over
    o.bowler_id, -- The ID of the bowler
    p.name as bowler_name, -- The name of the bowler
    t.short_name as bowling_team, -- The short name of the bowling team
    t.id as team_id, -- The ID of the bowling team
    -- Basic bowling stats
    COUNT(d.id) as total_deliveries, -- The total number of deliveries bowled
    COUNT(CASE WHEN d.is_legal_ball = true THEN 1 END) as legal_deliveries, -- The number of legal deliveries bowled
    FLOOR(COUNT(CASE WHEN d.is_legal_ball = true THEN 1 END)::decimal / 6) as complete_overs, -- The number of complete overs bowled
    MOD(COUNT(CASE WHEN d.is_legal_ball = true THEN 1 END), 6) as balls_in_incomplete_over, -- The number of balls in the incomplete over
    CONCAT(
        FLOOR(COUNT(CASE WHEN d.is_legal_ball = true THEN 1 END)::decimal / 6)::text, -- The number of complete overs bowled
        '.',
        MOD(COUNT(CASE WHEN d.is_legal_ball = true THEN 1 END), 6)::text
    ) as overs_bowled, -- The number of overs bowled
    -- Corrected runs calculations
    SUM(d.runs_batter) as runs_off_bat, -- The number of runs conceded off the bat
    SUM(CASE 
        WHEN d.is_wide = true THEN 1 -- The number of wides conceded
        WHEN d.is_no_ball = true THEN 1 -- The number of no balls conceded
        ELSE 0 
    END) as extras_runs,
    SUM(d.runs_batter + 
        CASE 
            WHEN d.is_wide = true THEN 1 -- The number of wides conceded
            WHEN d.is_no_ball = true THEN 1 -- The number of no balls conceded
            ELSE 0 
        END
    ) as runs_conceded,
    SUM(d.byes) as byes,           -- Not counted in runs_conceded
    SUM(d.legbyes) as legbyes,     -- Not counted in runs_conceded
    COUNT(CASE WHEN d.is_wicket = true THEN 1 END) as wickets,
    -- Detailed bowling stats
    COUNT(CASE WHEN d.runs_batter = 0 AND d.is_legal_ball = true THEN 1 END) as dot_balls, -- The number of dot balls conceded
    COUNT(CASE WHEN d.runs_batter = 1 THEN 1 END) as singles_conceded, -- The number of singles conceded
    COUNT(CASE WHEN d.runs_batter = 2 THEN 1 END) as doubles_conceded, -- The number of doubles conceded
    COUNT(CASE WHEN d.runs_batter = 3 THEN 1 END) as triples_conceded, -- The number of triples conceded
    COUNT(CASE WHEN d.runs_batter = 4 THEN 1 END) as fours_conceded, -- The number of fours conceded
    COUNT(CASE WHEN d.runs_batter = 6 THEN 1 END) as sixes_conceded, -- The number of sixes conceded
    -- Extras
    COUNT(CASE WHEN d.is_wide = true THEN 1 END) as wides, -- The number of wides conceded
    COUNT(CASE WHEN d.is_no_ball = true THEN 1 END) as no_balls,
    -- Phase-wise analysis (excluding byes and leg byes)
    SUM(CASE WHEN d.phase = 'powerplay' THEN  -- The number of runs conceded in the
        d.runs_batter + 
        CASE 
            WHEN d.is_wide = true THEN 1 -- The number of wides conceded
            WHEN d.is_no_ball = true THEN 1 -- The number of no balls conceded
            ELSE 0 
        END
    ELSE 0 END) as powerplay_runs, -- The number of runs conceded in the powerplay
    COUNT(CASE WHEN d.phase = 'powerplay' AND d.is_wicket = true THEN 1 END) as powerplay_wickets,
    SUM(CASE WHEN d.phase = 'middle' THEN  -- The number of runs conceded in the middle overs
        d.runs_batter + 
        CASE 
            WHEN d.is_wide = true THEN 1 -- The number of wides conceded
            WHEN d.is_no_ball = true THEN 1
            ELSE 0 
        END
    ELSE 0 END) as middle_overs_runs,
    COUNT(CASE WHEN d.phase = 'middle' AND d.is_wicket = true THEN 1 END) as middle_overs_wickets,
    SUM(CASE WHEN d.phase = 'death' THEN 
        d.runs_batter + 
        CASE 
            WHEN d.is_wide = true THEN 1 -- The number of wides conceded
            WHEN d.is_no_ball = true THEN 1 -- The number of no balls conceded
            ELSE 0 
        END
    ELSE 0 END) as death_overs_runs, -- The number of runs conceded in the death overs
    COUNT(CASE WHEN d.phase = 'death' AND d.is_wicket = true THEN 1 END) as death_overs_wickets, -- The number of wickets taken in the death overs
    -- Economy and strike rate calculations (excluding byes and leg byes)
    ROUND(
        (SUM(d.runs_batter + 
            CASE 
                WHEN d.is_wide = true THEN 1 -- The number of wides conceded
                WHEN d.is_no_ball = true THEN 1 -- The number of no balls conceded
                ELSE 0 
            END
        ) * 6.0) / 
        NULLIF(COUNT(CASE WHEN d.is_legal_ball = true THEN 1 END), 0), 
    2) as economy_rate, -- The economy rate of the bowler
    ROUND(COUNT(CASE WHEN d.is_legal_ball = true THEN 1 END) * 1.0 / NULLIF(COUNT(CASE WHEN d.is_wicket = true THEN 1 END), 0), 2) as strike_rate,
    ROUND(
        (SUM(d.runs_batter + 
            CASE 
                WHEN d.is_wide = true THEN 1 -- The number of wides conceded
                WHEN d.is_no_ball = true THEN 1 -- The number of no balls conceded
                ELSE 0 
            END
        ) * 1.0) / 
        NULLIF(COUNT(CASE WHEN d.is_wicket = true THEN 1 END), 0),  
    2) as average, -- The average of the bowler
    -- Spell information
    bs.spell_start, -- The start of the spell   
    bs.spell_end, -- The end of the spell
    -- Match role information
    pmr.is_captain, -- Whether the bowler is the captain of the team
    pmp.is_impact_player, -- Whether the bowler is an impact player
    pmp.impact_sub_time, -- The time of the impact substitution
    -- Wicket types summary
    COUNT(CASE WHEN w.kind = 'bowled' THEN 1 END) as bowled, -- The number of wickets taken by the bowler
    COUNT(CASE WHEN w.kind = 'caught' THEN 1 END) as caught, -- The number of wickets taken by the bowler   
    COUNT(CASE WHEN w.kind = 'lbw' THEN 1 END) as lbw, -- The number of wickets taken by the bowler
    COUNT(CASE WHEN w.kind = 'stumped' THEN 1 END) as stumped, -- The number of wickets taken by the bowler
    COUNT(CASE WHEN w.kind = 'caught and bowled' THEN 1 END) as caught_and_bowled, -- The number of wickets taken by the bowler
    COUNT(CASE WHEN w.kind = 'hit wicket' THEN 1 END) as hit_wicket -- The number of wickets taken by the bowler
FROM ipl.matches m
JOIN ipl.innings i ON i.match_id = m.id -- The innings bowled by the bowler
JOIN ipl.overs o ON o.innings_id = i.id -- The overs bowled by the bowler
JOIN ipl.deliveries d ON d.over_id = o.id -- The deliveries bowled by the bowler
JOIN ipl.players p ON p.id = o.bowler_id -- The bowler
JOIN ipl.teams t ON t.id = i.bowling_team_id -- The team bowling the overs
LEFT JOIN ipl.wickets w ON w.delivery_id = d.id
LEFT JOIN bowling_spells bs ON bs.match_id = m.id AND bs.innings_id = i.id AND bs.bowler_id = o.bowler_id -- The spells bowled by the bowler
LEFT JOIN ipl.player_match_roles pmr ON pmr.match_id = m.id AND pmr.player_id = o.bowler_id -- The role of the bowler in the match
LEFT JOIN ipl.player_match_performance pmp ON pmp.match_id = m.id AND pmp.player_id = o.bowler_id -- The performance of the bowler in the match
GROUP BY 
    m.id, -- The ID of the match
    i.id, -- The ID of the innings
    i.innings_number, -- The innings number
    i.is_super_over, -- Whether the innings is a super over
    m.super_over, -- Whether the match had a super over
    o.bowler_id, -- The ID of the bowler
    p.name, -- The name of the bowler
    t.short_name, -- The short name of the bowling team
    t.id, -- The ID of the bowling team
    bs.spell_start, -- The start of the spell
    bs.spell_end, -- The end of the spell
    pmr.is_captain, -- Whether the bowler is the captain of the team
    pmp.is_impact_player, -- Whether the bowler is an impact player
    pmp.impact_sub_time -- The time of the impact substitution
ORDER BY m.id, i.id, o.bowler_id;  -- Order the results by match ID, innings ID, and bowler ID

-- Points Table which contains the points table details for the whole individual season. 
CREATE TABLE ipl.points_table (
    id SERIAL PRIMARY KEY, -- The ID of the points table
    season_id INT REFERENCES ipl.seasons(id), -- The ID of the season
    year INT, -- The year of the season
    team_id INT REFERENCES ipl.teams(id), -- The ID of the team
    team_name VARCHAR(100), -- The name of the team
    matches_played INT DEFAULT 0, -- The number of matches played
    matches_won INT DEFAULT 0, -- The number of matches won
    no_results INT DEFAULT 0, -- The number of matches with no result
    points INT DEFAULT 0, -- The number of points
    net_run_rate DECIMAL(6,3) DEFAULT 0.000, -- The net run rate
    win_percentage DECIMAL(5,2) DEFAULT 0.00, -- The win percentage
    position INT, -- The position of the team in the points table
    winner BOOLEAN DEFAULT FALSE, -- Whether the team is the winner of the season
    runner_up BOOLEAN DEFAULT FALSE, -- Whether the team is the runner up of the season
    eliminator_participant BOOLEAN DEFAULT FALSE, -- Whether the team is a participant in the eliminator
    eliminator_winner BOOLEAN DEFAULT FALSE, -- Whether the team is the winner of the eliminator
    qualifier2_participant BOOLEAN DEFAULT FALSE, -- Whether the team is a participant in the qualifier 2
    qualifier2_winner BOOLEAN DEFAULT FALSE, -- Whether the team is the winner of the qualifier 2
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- The last updated timestamp
    UNIQUE(season_id, team_id) -- The unique constraint on the season ID and team ID
);
""" 