CREATE TABLE IF NOT EXISTS everyday_visitor(
v_date DATETIME NOT NULL DEFAULT NOW(),
visitor_cnt INT NOT NULL,
PRIMARY KEY (v_date)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;