CREATE TABLE IF NOT EXISTS vote_select(
user_id INT NOT NULL,
vote_id INT NOT NULL,
vote_content_id INT NOT NULL,
vote_select_time DATETIME NOT NULL, DEFAULT NOW()
PRIMARY KEY(user_id, vote_id, vote_content_id),
FOREIGN KEY(user_id) REFERENCES user(user_id) ON UPDATE CASCADE,
FOREIGN KEY(vote_id) REFERENCES vote_title(vote_id) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY(vote_content_id) REFERENCES vote_content(vote_content_id) ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;