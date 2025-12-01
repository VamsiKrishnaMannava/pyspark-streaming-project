DROP TABLE IF NOT EXISTS users;

CREATE TABLE users (
    gender              VARCHAR(255),
    title               VARCHAR(255),
    first_name          VARCHAR(255),
    last_name           VARCHAR(255),
    street_number       VARCHAR(255),
    street_name         VARCHAR(255),
    city                VARCHAR(255),
    state               VARCHAR(255),
    country             VARCHAR(255),
    postcode            VARCHAR(255),
    latitude            VARCHAR(255),
    longitude           VARCHAR(255),
    tz_offset           VARCHAR(255),
    tz_description      VARCHAR(255),
    email               VARCHAR(255),
    login_uuid          VARCHAR(255),
    username            VARCHAR(255),
    password            VARCHAR(255),
    dob_date            VARCHAR(255),
    dob_age             VARCHAR(255),
    registered_date     VARCHAR(255),
    registered_age      VARCHAR(255),
    phone               VARCHAR(255),
    cell                VARCHAR(255),
    id_name             VARCHAR(255),
    id_value            VARCHAR(255),
    picture_large       VARCHAR(255),
    picture_medium      VARCHAR(255),
    picture_thumbnail   VARCHAR(255),
    nationality         VARCHAR(255)
);

SELECT COUNT(1) AS USR_CNT FROM USERS;