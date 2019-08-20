var baselayers, ways, nodes, controls_layers, mymap, overlays, mapbox, place_loc;

// var mapbox = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
mapbox = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    minZoom: 10,
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoicG5vbGwiLCJhIjoiY2pkNDNyNmtzMHRtOTMzcWZ0Y2szdzh3eCJ9.g8tszbsYH0bVCcj7v8RAEQ'
});
baselayers = {
    "Mapbox": mapbox
};

mymap = L.map('map', {
    center: [loc[1], loc[0]],
    zoom: 15,
    layers: [mapbox]
});

// tries to locate user on page load
mymap.locate({ setView: true, enableHighAccuracy: true });
mymap.on('locationerror', onLocationError);
function onLocationError(e) {
  alert(e.message);
}

var markerGroup = L.layerGroup().addTo(mymap);

mymap.on('click', function(ev) {
    markerGroup.clearLayers();
    // store as long lat as needed for database
    place_loc = [ev.latlng.lng, ev.latlng.lat];
    L.marker([ev.latlng.lat, ev.latlng.lng],).addTo(markerGroup);
    markerGroup.addTo(mymap);
});

function sendToDb() {
  if (place_loc) {
    let queries = '?name=' + String(name) + '&phone=' + String(phone) + '&place_loc=' + String(place_loc);
    fetch('add_place' + queries)
    .then(res => {
      if (res.ok) {
      window.location = 'add_place?success=yes';
      } else if (res.ok == false) {
        window.location = 'add_place' + queries;
      }
    })
    .catch(err => 'add_place?success=no');
  } else {
    let queries = '?name=' + String(name) + '&phone=' + String(phone);
    window.location = 'add_place' + queries + '&success=no';
  }
}
