var baselayers, ways, nodes, controls_layers, mymap, overlays, mapbox;

//var mapbox = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
var mapbox = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    minZoom: 10,
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoicG5vbGwiLCJhIjoiY2pkNDNyNmtzMHRtOTMzcWZ0Y2szdzh3eCJ9.g8tszbsYH0bVCcj7v8RAEQ'
});
var baselayers = {
    "Mapbox": mapbox
}
var mymap = L.map('map', {
    center: [loc[1],loc[0]],
    zoom: 15,
    layers: [mapbox]
});
L.marker([loc[1],loc[0]],).addTo(mymap);
