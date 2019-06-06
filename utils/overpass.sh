curl -o nagoya_data.osm -g 'https://overpass-api.de/api/interpreter?data=rel["name:en"="Nagoya"];map_to_area->.a;(node(area.a)[amenity="restaurant"];way(area.a)[amenity="restaurant"];);out;'
# cafes and fast food too?
# Nagoya to start
osm2pgsql --slim --username pat --database reservation nagoya_data.osm -S ./utils/restaurant.style

#         'USER': 'pat','PASSWORD': 'password',
# update planet_osm_point set geom=planet_osm_nodes.geom from planet_osm_nodes where planet_osm_point.osm_id = planet_osm_nodes.id;


#ALTER TABLE planet_osm_nodes ADD COLUMN geom geometry(Point,4326);
#update planet_osm_nodes set geom = ST_SetSRID(ST_MakePoint(lon, lat), 4326);


