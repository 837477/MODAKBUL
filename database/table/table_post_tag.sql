CREATE TABLE IF NOT EXISTS post_tag(
post_id INT NOT NULL,
tag_id VARCHAR(20) NOT NULL,
PRIMARY KEY(post_id, tag_id),
FOREIGN KEY(post_id) REFERENCES post(post_id) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY(tag_id) REFERENCES tag(tag_id) ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;