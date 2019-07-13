CREATE TABLE IF NOT EXISTS user(
user_id INT NOT NULL,
user_pw VARCHAR(100) NOT NULL,
user_name VARCHAR(20) NOT NULL,
user_major VARCHAR(20) NOT NULL,
user_nickname VARCHAR(20) NULL,
user_access INT(1) unsigned default 1,
PRIMARY KEY(user_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;