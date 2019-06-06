var baselayers, ways, nodes, controls_layers, mymap, overlays, mapbox;

var mapbox = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    minZoom: 8,
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoicG5vbGwiLCJhIjoiY2pkNDNyNmtzMHRtOTMzcWZ0Y2szdzh3eCJ9.g8tszbsYH0bVCcj7v8RAEQ'
});
var baselayers = {
    "Mapbox": mapbox
}
var lat = JSON.parse(document.getElementById('location_dump').textContent);
  console.log(lat);
//console.log(JSON.stringify(location));
var mymap = L.map('map', {
    center: [location[0], location[1]],
    zoom: 9,
    layers: [mapbox]
});
/*
var nodes = L.geoJSON(data,{
style: function (feature) {
    return {stroke:false,fill:false};
}
});

nodes.addTo(mymap);
*/
/*
var overlays = {
"markers": markers,
"ways": ways,
};
var controls_layers = L.control.layers(baselayers, overlays);
controls_layers.addTo(mymap);
legend.addTo(mymap);
counter.addTo(mymap);
});

var legend = L.control({position: 'bottomright'});
legend.onAdd = function (mymap) {
    var div = L.DomUtil.create('div', 'legend');
    //div.innerHTML = 'OSM Last Touched Edits';
    return div;
};
*/
