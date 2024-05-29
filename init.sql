CREATE TABLE users (
  user_id serial PRIMARY KEY,
  chat_id VARCHAR(100) UNIQUE
);

CREATE TABLE partners (
  partner_id serial PRIMARY KEY,
  partner_name VARCHAR(100)
);

CREATE TABLE user_visited_partner (
  user_id INT,
  partner_id INT,
  PRIMARY KEY (user_id, partner_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (partner_id) REFERENCES partners(partner_id)
);

INSERT INTO partners (partner_name) VALUES 
('Level group'),
('BC questions'),
('Технологии доверия'),
('BC photobooth'),
('hse inc'),
('BC networking'),
('Малый бизнес Москвы'),
('Альфа банк'),
('SuperJob'),
('Beyond Taylor'),
('Kept'),
('Фонд содействия инновациям'),
('аэропорт Домодедово'),
('Сибур'),
('ВТБ');