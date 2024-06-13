-- DROP TABLE moves;
-- DROP TABLE games;
-- DROP TABLE admin_logs;
-- DROP TABLE sessions;
-- DROP TABLE players;

CREATE TABLE players(
    player_id BIGINT UNSIGNED UNIQUE AUTO_INCREMENT PRIMARY KEY,
    player_type VARCHAR(5) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    phone_number VARCHAR(13) UNIQUE NOT NULL,
    photo LONGBLOB NOT NULL,
    pass VARBINARY(32) NOT NULL
);

CREATE TABLE sessions(
	session_id BIGINT UNSIGNED UNIQUE AUTO_INCREMENT PRIMARY KEY,
    player_id BIGINT UNSIGNED,
	FOREIGN KEY (player_id) REFERENCES players(player_id),
    ban_bool TINYINT DEFAULT 0,
    ban_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ban_time BIGINT DEFAULT 0
);

CREATE TABLE admin_logs(
	admin_log_id BIGINT UNSIGNED UNIQUE AUTO_INCREMENT PRIMARY KEY
);

CREATE TABLE games(
	game_id BIGINT UNSIGNED UNIQUE AUTO_INCREMENT PRIMARY KEY,
    p1_id BIGINT UNSIGNED,
    FOREIGN KEY (p1_id) REFERENCES players(player_id),
    p2_id BIGINT UNSIGNED,
    FOREIGN KEY (p2_id) REFERENCES players(player_id),
    p3_id BIGINT UNSIGNED,
    FOREIGN KEY (p3_id) REFERENCES players(player_id),
    p4_id BIGINT UNSIGNED,
    FOREIGN KEY (p4_id) REFERENCES players(player_id)
);

CREATE TABLE moves(
	moves_id BIGINT UNSIGNED UNIQUE AUTO_INCREMENT PRIMARY KEY,
	game_id BIGINT UNSIGNED,
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    p1_board VARCHAR(32),
    p2_board VARCHAR(32),
    p3_board VARCHAR(32),
    p4_board VARCHAR(32)
);