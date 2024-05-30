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
('Технологии доверия'),
('hse inc'),
('Малый бизнес Москвы'),
('Альфа банк'),
('SuperJob'),
('Kept'),
('Фонд содействия инновациям'),
('аэропорт Домодедово'),
('Развитие человеческого капитала'),
('Сбер'),
('Skillbox'),
('Сколково'),
('МАРС'),
('Тинькофф банк'),
('Открой глаза - ВШЭ'),
('Юнилевер Русь'),
('Агенство инноваций Москвы');
