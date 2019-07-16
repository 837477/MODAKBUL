CREATE TABLE IF NOT EXISTS account_attach(
account_id INT NOT NULL,
account_file_path VARCHAR(500) NOT NULL,
PRIMARY KEY(account_id, account_file_path),
FOREIGN KEY(account_id) REFERENCES account(account_id) ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;