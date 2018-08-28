FROM mdillon/postgis

COPY initdb.sql /docker-entrypoint-initdb.d/initdb.sql
COPY data/sf_business_businesses.csv /docker-entrypoint-initdb.d/sf_business_businesses.csv
COPY data/sf_business_inspections.csv /docker-entrypoint-initdb.d/sf_business_inspections.csv
COPY data/sf_business_legend.csv /docker-entrypoint-initdb.d/sf_business_legend.csv
COPY data/sf_business_violations.csv /docker-entrypoint-initdb.d/sf_business_violations.csv
