CREATE TABLE if not exists public.brand (
  brand_id INT PRIMARY KEY NOT NULL,
  brand_name VARCHAR(255) NOT NULL
);

create table if not exists segment_brand(
	segment_id INT not null references segment(segment_id),
	brand_id INTEGER not null references brand(brand_id),
	primary key (segment_id, brand_id)
);


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
--  (22, "Levi\'s"),
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