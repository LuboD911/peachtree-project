CREATE DATABASE IF NOT EXISTS peachtree_bank;
USE peachtree_bank;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS refresh_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) NOT NULL,
    token VARCHAR(512) NOT NULL,
    revoked BOOLEAN DEFAULT FALSE,
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transaction_statuses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE,
    color VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS contractors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    image_url VARCHAR(512) DEFAULT 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'
);

CREATE TABLE IF NOT EXISTS system_accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    balance DECIMAL(15, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    contractor_id INT NOT NULL,
    type ENUM('card_payment', 'online_transfer', 'transaction'),
    amount DECIMAL(10, 2),
    status_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (contractor_id) REFERENCES contractors(id),
    FOREIGN KEY (status_id) REFERENCES transaction_statuses(id)
);

CREATE INDEX idx_transactions_date ON transactions(date);
CREATE INDEX idx_transactions_contractor_id ON transactions(contractor_id);
CREATE INDEX idx_transactions_amount ON transactions(amount);

INSERT INTO transaction_statuses (name, color) VALUES
('sent', 'red'),
('received', 'yellow'),
('paid', 'green');

INSERT INTO contractors (name, image_url) VALUES
('H&M Store', 'https://www.hm.com/entrance/assets/bundle/img/HM-Share-Image.jpg'),
('Whole Foods', 'https://banner2.cleanpng.com/20180430/rsw/kisspng-whole-foods-market-organic-food-amazon-com-beer-festival-food-5ae7c1a962a879.7177055715251378334041.jpg'),
('Texaco', 'https://cdn.freebiesupply.com/logos/large/2x/texaco-logo-png-transparent.png'),
('Jerry Hildreth', 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png');

INSERT INTO system_accounts (name, balance) VALUES
('Main Account', 10000.00),
('Secondary Account', 5000.00);

INSERT INTO users (username, password) VALUES
('alice', '$2b$12$w1Q4Q1Q4Q1Q4Q1Q4Q1Q4eIXwl/1aQ9Q6Q9Q6Q9Q6Q9Q6Q9Q6Q9Q6'),
('bob',   '$2b$12$z2A4A2A4A2A4A2A4A2A4eIXwl/1aQ9Q6Q9Q6Q9Q6Q9Q6Q9Q6Q9Q6');

INSERT INTO transactions (user_id, date, contractor_id, type, amount, status_id) VALUES
(1, '2025-05-01 10:30:00', 1, 'card_payment', 120.00, 1),
(1, '2025-05-02 14:15:30', 2, 'online_transfer', 220.00, 2),
(1, '2025-05-03 09:45:12', 3, 'transaction', 320.00, 3),
(2, '2025-06-01 16:20:45', 3, 'card_payment', 150.00, 1),
(2, '2025-06-02 11:05:33', 1, 'online_transfer', 250.00, 2),
(2, '2025-06-03 13:40:18', 4, 'transaction', 350.00, 3);
