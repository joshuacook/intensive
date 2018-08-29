import lib.db_helper as db
import numpy as np

select_count_by_postal_code = """
SELECT postal_code, COUNT(*) FROM business
GROUP BY postal_code
ORDER BY postal_code
"""

select_count_business_non_null_lat_long = """
SELECT COUNT(*) FROM business
WHERE latitude IS NOT NULL
AND longitude IS NOT NULL
"""

select_count_business_invalid_data = """
SELECT COUNT(*) FROM business
WHERE latitude = 0 AND longitude = 0;"""

select_count_business_valid = """
SELECT COUNT(*) FROM business
WHERE 
    (latitude IS NOT NULL
     AND longitude IS NOT NULL)
AND 
    (latitude != 0 
     AND longitude != 0)
"""

select_count_business_invalid = """
SELECT COUNT(*) FROM business
WHERE 
    (latitude IS NULL
     AND longitude IS NULL)
OR 
    (latitude = 0 
     AND longitude = 0)
"""

select_business_valid = """
SELECT * FROM business
WHERE 
    (latitude IS NOT NULL
     AND longitude IS NOT NULL)
AND 
    (latitude != 0 
     AND longitude != 0)
"""

select_business_invalid = """
SELECT * FROM business
WHERE 
    (latitude IS NULL
     AND longitude IS NULL)
OR 
    (latitude = 0 
     AND longitude = 0)
"""

select_postal_code_by_postal_code_less_than_10 = """
SELECT postal_code FROM 
    ({}) q
WHERE count < 10
""".format(select_count_by_postal_code)

select_business_where_bad_postal_code = """
SELECT * FROM business WHERE postal_code IN ({})""".format(select_postal_code_by_postal_code_less_than_10)

select_invalid_business_where_bad_postal_code = """
SELECT * 
FROM ({}) q
WHERE postal_code IN ({})
""".format(select_business_invalid, select_postal_code_by_postal_code_less_than_10)

select_invalid_business_id_where_bad_postal_code = """
SELECT id 
FROM ({}) q
WHERE postal_code IN ({})
""".format(select_business_invalid, select_postal_code_by_postal_code_less_than_10)

delete_invalid_business_bad_postal_code = """
BEGIN;
DELETE 
FROM business
WHERE id IN ({});
COMMIT;
""".format(select_invalid_business_id_where_bad_postal_code)


def get_average_location():
    avg_location_sf = """
    SELECT avg(latitude) as avg_lat, 
           avg(longitude) as avg_lon FROM ({}) q;
    """.format(select_business_valid)

    db.query_to_dataframe(avg_location_sf)

    avg_loc_df = db.query_to_dataframe(avg_location_sf)

    avg_loc = avg_loc_df.values.tolist()[0]
    
    return avg_loc

def select_postal_code(postal_code):
    return """SELECT * FROM business WHERE postal_code = {}""".format(postal_code)

def select_gpnt_for_postal_code(postal_code):
    return """SELECT gpnt_location FROM business WHERE postal_code = {} LIMIT 1""".format(postal_code)

def select_on_gpnt_radius(postal_code, distance):
    return """
            SELECT *
            FROM business
            WHERE ST_Distance_Sphere(gpnt_location, ({})) <= {}
            """.format(select_gpnt_for_postal_code(postal_code), distance)

def select_business_locations_for_postal_code(postal_code):
    query = """SELECT * FROM business WHERE postal_code = {} AND gpnt_location IS NOT NULL""".format(postal_code)
    businesses = db.query_to_dataframe(query)
    return businesses[['latitude', 'longitude','postal_code']]