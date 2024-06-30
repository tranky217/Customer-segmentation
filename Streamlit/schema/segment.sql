CREATE TABLE if not exists public.brand (
  brand_id INT PRIMARY KEY NOT NULL,
  brand_name VARCHAR(255) NOT NULL
);

CREATE TABLE if not exists public.category (
  category_id INT PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL
);

CREATE TABLE if not exists public.segment (
  segment_id VARCHAR(100) PRIMARY KEY NOT NULL,
  segment_name VARCHAR(255) NOT NULL,
  gender VARCHAR(20),
  min_price DECIMAL(10,2),
  max_price DECIMAL(10,2),
  min_date DATE
);

create table if not exists segment_brand(
	segment_id VARCHAR(100) not null references segment(segment_id) on delete cascade,
	brand_id INTEGER not null references brand(brand_id) on delete cascade,
	primary key (segment_id, brand_id)
);

create table if not exists segment_category(
	segment_id VARCHAR(100) not null references segment(segment_id) on delete cascade,
	category_id INT not null references category(category_id) on delete cascade,
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
 
INSERT INTO brand (brand_id, brand_name)
VALUES
  (1, 'WALK LONDON'),
  (2, 'Reebok'),
  (3, 'Nike'),
  (4, 'Jack & Jones'),
  (5, 'Crocs'),
  (6, 'Vans'),
  (7, 'Puma'),
  (8, 'New Balance'),
  (9, 'Tommy Jeans'),
  (10, 'Tommy Hilfiger'),
  (11, 'Bershka'),
  (12, 'New Look'),
  (13, 'AllSaints'),
  (14, 'Columbia'),
  (15, 'The North Face'),
  (16, 'Collusion'),
  (17, 'ASOS DESIGN'),
  (18, 'Topman'),
  (19, 'Dr Denim'),
  (20, 'Polo Ralph Lauren'),
  (21, 'ASOS Dark Future'),
  (22, 'Levi''s'),
  (23, 'Threadbare'),
  (24, 'Calvin Klein'),
  (25, 'AAPE BY A BATHING APE®'),
  (26, 'Good For Nothing'),
  (27, 'Timberland'),
  (28, 'Pull and Bear'),
  (29, 'Koi Footwear'),
  (30, 'adidas performance'),
  (31, 'Nike Running'),
  (32, 'Dr Martens'),
  (33, 'River Island');
 
--  insert into brand (brand_id, brand_name)
--  values (22, 'Levi''s');

--SELECT * FROM public.brand;
