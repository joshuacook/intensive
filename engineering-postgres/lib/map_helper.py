from lib.queries import *
import folium

def plot_businesses_for_postal_code(postal_code, shared_map=None, color='blue'):
    business_locations = select_business_locations_for_postal_code(postal_code)
    average_location = business_locations.mean().values[:2].tolist()
    if shared_map:
        this_map = shared_map
    else:
        this_map = folium.Map(location=average_location, zoom_start=14)
    for loc in business_locations[['latitude','longitude']].values.tolist():
        try:
            postal_code = str(int(loc[2]))
        except:
            postal_code = None
        folium.Marker(loc[:2],postal_code, icon=folium.Icon(color=color)).add_to(this_map)
    return this_map