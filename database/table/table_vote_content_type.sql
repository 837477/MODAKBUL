CREATE TABLE IF NOT EXISTS vote_content_type(
content_type_id TINYINT NOT NULL AUTO_INCREMENT,
content_type_title VARCHAR(10) NOT NULL,
PRIMARY KEY(content_type_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;