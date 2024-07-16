-- CREATE SCHEMA nyanner_db

DROP TABLE moves;
DROP TABLE game;
DROP TABLE admin_logs;
DROP TABLE sessions;
DROP TABLE issued_tokens;
DROP TABLE users;
DROP TABLE photos;

CREATE TABLE photos (
    id INT NOT NULL AUTO_INCREMENT,
    filename VARCHAR(100) NOT NULL,
    content LONGBLOB NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE users(
    user_id BIGINT UNSIGNED UNIQUE AUTO_INCREMENT PRIMARY KEY,
	user_type BOOLEAN NOT NULL DEFAULT FALSE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    username VARCHAR(16) UNIQUE NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    birthday DATE,
    phone_number VARCHAR(13) UNIQUE NOT NULL,
    photo_id INT,
    password VARBINARY(256) NOT NULL,
	FOREIGN KEY (photo_id) REFERENCES photos(id)
);

CREATE TABLE sessions(
    session_id BIGINT UNSIGNED UNIQUE AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED,
	FOREIGN KEY (user_id) REFERENCES users(user_id),
    ban_bool BOOLEAN DEFAULT 0,
    ban_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ban_time BIGINT DEFAULT 0
);

CREATE TABLE admin_logs(
	admin_log_id BIGINT UNSIGNED UNIQUE AUTO_INCREMENT PRIMARY KEY,
    description TEXT DEFAULT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE game(
	lobby_name VARCHAR(32) UNIQUE PRIMARY KEY,
    p1_id BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY (p1_id) REFERENCES users(user_id),
    p2_id BIGINT UNSIGNED,
    FOREIGN KEY (p2_id) REFERENCES users(user_id)
);

CREATE TABLE moves(
	moves_id BIGINT UNSIGNED UNIQUE AUTO_INCREMENT PRIMARY KEY,
	lobby_name VARCHAR(32) UNIQUE,
    FOREIGN KEY (lobby_name) REFERENCES game(lobby_name),
    board VARCHAR(256)
);

CREATE TABLE issued_tokens(
	token_id VARCHAR(256) UNIQUE PRIMARY KEY,
    user_id BIGINT UNSIGNED,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    issued_at DATETIME NOT NULL,
    invalidated BOOLEAN NOT NULL DEFAULT FALSE
);
