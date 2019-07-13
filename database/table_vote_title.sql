CREATE TABLE IF NOT EXISTS vote_title(
vote_id INT NOT NULL AUTO_INCREMENT,
user_id INT NOT NULL,
vote_content VARCHAR(1500) NULL,
vote_name VARCHAR(100) NOT NULL,
vote_start DATETIME NOT NULL DEFAULT NOW(),
vote_end DATETIME NOT NULL,
vote_statement INT(1) unsigned NOT NULL DEFAULT 1,
PRIMARY KEY(vote_id),
FOREIGN KEY(user_id) REFERENCES user(user_id) ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;