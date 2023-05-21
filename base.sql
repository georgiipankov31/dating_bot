-- DROP TABLE dating.city;
-- Города
CREATE TABLE dating.city (
	city_name text NULL,
	city_region numeric NULL,
	city_data text NULL,
	city_parent text NULL
);
-- DROP TABLE dating.users;
-- Анкеты
CREATE TABLE dating.users (
	id serial4 NOT NULL,
	user_id int8 NOT NULL,
	user_nick text NOT NULL,
	user_name text NULL DEFAULT 'Человек'::text,
	user_gender text NULL DEFAULT 'trans'::text,
	user_finding_gender text NULL DEFAULT 'trans'::text,
	user_age numeric NULL DEFAULT 18,
	user_text text NULL DEFAULT ''::text,
	user_city text NOT NULL,
	user_rating numeric NULL DEFAULT 0,
	is_actually bool NULL DEFAULT false,
	user_complains_type1 numeric NULL DEFAULT 0,
	user_complains_type2 numeric NULL DEFAULT 0,
	user_photo text NULL,
	CONSTRAINT users_id_key null,
	CONSTRAINT users_pkey null
);
