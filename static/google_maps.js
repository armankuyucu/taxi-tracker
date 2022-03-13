
let map;

let distanceMatrix = [];
let routeOrder = [];
let routeOrderInt = [];
//To get numbers in a string
let regularExpression = /\d+/g;

function initMap() {

    map = new google.maps.Map(document.getElementById("map"), {
            center: {lat: 40.767, lng: 29.917},
            zoom: 14,
        }
    );
    const mydata = JSON.parse(document.getElementById('mydata').textContent);
    console.log(mydata)
}
