DROP TABLE IF EXISTS scripts;
DROP TABLE IF EXISTS games;

CREATE TABLE scripts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    module_name TEXT NOT NULL UNIQUE,
    script_path TEXT NOT NULL UNIQUE
);

CREATE TABLE games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_player_ip TEXT NOT NULL,
    second_player_ip TEXT,
    first_player_plays_as TEXT NOT NULL CHECK (first_player_plays_as == 'white' OR first_player_plays_as == 'black'),
    move_number INTEGER NOT NULL,
    turn TEXT NOT NULL CHECK (turn == 'white' OR turn == 'black'),
    script_id INTEGER NOT NULL,
    link TEXT NOT NULL UNIQUE,
    additional_data TEXT
);
