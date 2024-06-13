-- DROP TABLE moves;
-- DROP TABLE games;
-- DROP TABLE admin_logs;
-- DROP TABLE sessions;
-- DROP TABLE users;

CREATE TABLE users(
    user_id BIGINT UNSIGNED UNIQUE AUTO_INCREMENT PRIMARY KEY,
    user_type BOOL DEFAULT 0,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    username VARCHAR(16) UNIQUE NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    phone_number VARCHAR(13) UNIQUE NOT NULL,
    photo LONGBLOB,
    password VARBINARY(32) NOT NULL
);

CREATE TABLE sessions(
    session_token VARCHAR(256) UNIQUE PRIMARY KEY,
    user_id BIGINT UNSIGNED,
	FOREIGN KEY (user_id) REFERENCES users(user_id),
    ban_bool BOOL DEFAULT 0,
    ban_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ban_time BIGINT DEFAULT 0
);

CREATE TABLE admin_logs(
	admin_log_id BIGINT UNSIGNED UNIQUE AUTO_INCREMENT PRIMARY KEY
);

CREATE TABLE games(
	game_id BIGINT UNSIGNED UNIQUE AUTO_INCREMENT PRIMARY KEY,
    p1_id BIGINT UNSIGNED,
    FOREIGN KEY (p1_id) REFERENCES users(user_id),
    p2_id BIGINT UNSIGNED,
    FOREIGN KEY (p2_id) REFERENCES users(user_id),
    p3_id BIGINT UNSIGNED,
    FOREIGN KEY (p3_id) REFERENCES users(user_id),
    p4_id BIGINT UNSIGNED,
    FOREIGN KEY (p4_id) REFERENCES users(user_id)
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