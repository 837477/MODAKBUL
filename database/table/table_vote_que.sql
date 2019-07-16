CREATE TABLE IF NOT EXISTS vote_que(
vote_que_id INT NOT NULL AUTO_INCREMENT,
vote_id INT NOT NULL,
que_title VARCHAR(100) NOT NULL,
content_type_id TINYINT NOT NULL,
PRIMARY KEY(vote_que_id),
FOREIGN KEY(vote_id) REFERENCES vote(vote_id) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY(content_type_id) REFERENCES vote_content_type(content_type_id) ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;