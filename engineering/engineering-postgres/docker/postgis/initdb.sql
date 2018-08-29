CREATE TABLE business (
    id INTEGER,
    name TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    postal_code INTEGER,
    latitude FLOAT,
    longitude FLOAT,
    phone_number TEXT,
    PRIMARY KEY (id));

CREATE TABLE inspection (
    business_id INTEGER,
    score INTEGER,
    date TIMESTAMP,
    type TEXT,
    CONSTRAINT fk_business_id
    FOREIGN KEY (business_id)
    REFERENCES business (id));

CREATE TABLE legend (
    minimum_score INTEGER,
    maximum_score INTEGER,
    description TEXT);

CREATE TABLE violation (
    business_id INTEGER,
    date TIMESTAMP,
    description TEXT,
    CONSTRAINT fk_business_id
    FOREIGN KEY (business_id)
    REFERENCES business (id));

\copy business from '/docker-entrypoint-initdb.d/sf_business_businesses.csv' with DELIMITER ',' CSV HEADER;
\copy inspection from '/docker-entrypoint-initdb.d/sf_business_inspections.csv' with DELIMITER ',' CSV HEADER;
\copy legend from '/docker-entrypoint-initdb.d/sf_business_legend.csv' with DELIMITER ',' CSV HEADER;
\copy violation from '/docker-entrypoint-initdb.d/sf_business_violations.csv' with DELIMITER ',' CSV HEADER;
