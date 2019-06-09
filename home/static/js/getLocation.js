
var createCookie = (name, value, days) => {
  let expires;
  if (days) {
    let date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    expires = '; expires=' + date.toGMTString();
  } else {
    expires = '';
  }
  document.cookie = name + '=' + value + expires + '; path=/';
};


var options = {
  enableHighAccuracy: true,
  timeout: 10000,
  maximumAge: 0
};

function success(pos) {
  let crd = pos.coords;
  var search = document.getElementById('search').value;
  createCookie('location', crd, 2);
  window.location = '?search='+search;
}

function error(err) {
  console.warn(`ERROR(${err.code}): ${err.message}`);
}

function fetchLocation(){
  var promise = new Promise((resolve,reject) => {
    resolve(navigator.geolocation.getCurrentPosition(success,error,options));
  });
  return promise
}
