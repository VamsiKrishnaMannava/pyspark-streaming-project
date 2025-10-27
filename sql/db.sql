-- Main User Table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    gender VARCHAR(10),
    email VARCHAR(255),
    phone VARCHAR(50),
    cell VARCHAR(50),
    nat VARCHAR(10),
    name_id INT,
    location_id INT,
    login_id INT,
    dob_id INT,
    registered_id INT,
    id_id INT,
    picture_id INT
);

-- Name Table
CREATE TABLE name (
    name_id SERIAL PRIMARY KEY,
    title VARCHAR(20),
    first VARCHAR(100),
    last VARCHAR(100)
);

-- Location Table
CREATE TABLE location (
    location_id SERIAL PRIMARY KEY,
    street_number INT,
    street_name VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postcode VARCHAR(20),
    latitude VARCHAR(20),
    longitude VARCHAR(20),
    timezone_offset VARCHAR(10),
    timezone_description VARCHAR(100)
);

--  Login Table
CREATE TABLE login (
    login_id SERIAL PRIMARY KEY,
    uuid VARCHAR(100),
    username VARCHAR(100),
    password VARCHAR(100),
    salt VARCHAR(100),
    md5 VARCHAR(100),
    sha1 VARCHAR(100),
    sha256 VARCHAR(100)
);

-- Date of Birth Table
CREATE TABLE dob (
    dob_id SERIAL PRIMARY KEY,
    date TIMESTAMP,
    age INT
);

-- Registered Table 
CREATE TABLE registered (
    registered_id SERIAL PRIMARY KEY,
    date TIMESTAMP,
    age INT
);

-- ID Table
CREATE TABLE id (
    id_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    value VARCHAR(100)
);

-- Picture Table
CREATE TABLE picture (
    picture_id SERIAL PRIMARY KEY,
    large VARCHAR(255),
    medium VARCHAR(255),
    thumbnail VARCHAR(255)
);

