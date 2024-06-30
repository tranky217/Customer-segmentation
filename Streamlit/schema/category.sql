CREATE TABLE if not exists public.category (
  category_id INT PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL
);

create table if not exists segment_category(
	segment_id INT not null references segment(segment_id),
	category_id INT not null references category(category_id),
	primary key (segment_id, category_id)
);

INSERT INTO category (category_id, name)
VALUES
  (1000, 'shoes'),
  (2000, 'slippers'),
  (3000, 'heels'),
  (4000, 't-shirts'),
  (5000, 'jackets'),
  (6000, 'caps'),
  (7000, 'shorts'),
  (8000, 'sweaters'),
  (9000, 'sneakers'),
  (10000, 'shirts'),
  (11000, 'boots'),
  (12000, 'overshirts'),
  (13000, 'pants'),
  (14000, 'jeans'),
  (15000, 'socks'),
  (16000, 'belts'),
  (17000, 'trainers');