let map;
const BLUE_MARKER_URL = "https://maps.google.com/mapfiles/kml/paddle/blu-circle.png";
let markers = [];


function initMap() {
    // Create a map centered in Stockholm
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 59.329326902597735, lng: 18.068576534807608 },
        zoom: 7,
    });

    const taxiLocations = JSON.parse(JSON.parse(JSON.parse(document.getElementById('taxi_locations').textContent)));
    const user_id = JSON.parse(document.getElementById('user_id').textContent);
    const car_ids = JSON.parse(document.getElementById('car_ids').textContent);
    let currentDate = new Date();
    current_hour = currentDate.getHours()
    document.getElementById("startHour").value = (current_hour != 0) ? current_hour - 1 : 0;
    const currentTime = `${padTo2Digits(current_hour)}:${padTo2Digits(currentDate.getMinutes())}`;

    let carLocationIndexes = {};  // Store the indexes of each car's location data
    // use a for each loop to initialize the carLocationIndexes object
    car_ids.forEach((car_id) => {
        carLocationIndexes[car_id] = [];
    });

    let currentCarIndexes = {};

    // Populate location indexes for each car
    for (let i = 0; i < taxiLocations.length; i++) {
        taxiLocations[i].date_time = taxiLocations[i].date_time.split(" ").slice(-1);
        if (taxiLocations[i].date_time == currentTime) {
            currentCarIndexes[taxiLocations[i].car_id] = i;
        }
        carLocationIndexes[taxiLocations[i].car_id].push(i);
    }

    // Display last 30 minutes of data for each user's cars
    if (car_ids) {
        car_ids.forEach((car_id, index) => {
            showRouteForLast30Minutes(user_id, currentCarIndexes[car_id], taxiLocations, index);
        });
    }

    document.getElementById("submit").onclick = function () {
        let startHour = document.getElementById("startHour").value;
        let endHour = document.getElementById("endHour").value;
        let car_id = document.querySelector('#car-select').value;

        if (car_id === "Please select a car") {
            alert("The 'Select a car' field can't be empty.");
        } else if (enforceMinMax(startHour, endHour)) {
            // Clear the map of previous markers
            deleteMarkers();

            let index = car_ids.indexOf(parseInt(car_id));
            showRoute(car_id, carLocationIndexes[car_id][0], taxiLocations, index, startHour, endHour);
        }
    };
}

function enforceMinMax(startHour, endHour) {
    if (isValidHour(startHour) && isValidHour(endHour)) {
        return true;
    } else {
        alert("Please enter a number between 0 and 24");
        return false;
    }
}

function isValidHour(hour) {
    return -1 < parseInt(hour) && parseInt(hour) < 25;
}

// Shows the route for the last 30 minutes
function showRouteForLast30Minutes(user_id, carIndex, taxiLocations, index) {
    for (let i = carIndex; (carIndex - 30) < i; i--) {
        let coords = { lat: taxiLocations[i].latitude, lng: taxiLocations[i].longitude };
        // If the index is even, add a red marker, otherwise add a blue marker
        let marker = index % 2 === 0 ? addMarker(coords) : addMarker(coords, "blue");
        addInfoWindow(marker, coords, taxiLocations[i]);
    }
}

function showRoute(car_id, carFirstIndex, taxiLocations, index, startHour, endHour) {
    for (let i = (carFirstIndex + startHour * 60); i < (carFirstIndex + endHour * 60); i++) {
        if (car_id == taxiLocations[i].car_id) {
            let coords = { lat: taxiLocations[i].latitude, lng: taxiLocations[i].longitude };
            let marker = index % 2 === 0 ? addMarker(coords) : addMarker(coords, "blue");
            addInfoWindow(marker, coords, taxiLocations[i]);
        }
    }
}

function addMarker(coords, color=null) {
    let marker;
    if (color === "blue") {
        marker = new google.maps.Marker({
            position: coords,
            icon: BLUE_MARKER_URL,
            map: map
        }); 
    } else {
        marker = new google.maps.Marker({
            position: coords,
            map: map
        });    
    }
    markers.push(marker);
    return marker;
}

function addInfoWindow(marker, coords, data) {
    let infowindow = new google.maps.InfoWindow({
        content: `lat:${coords.lat}, lng:${coords.lng}, date:${data.date_time}, car_id:${data.car_id}`
    });
    marker.addListener("click", () => {
        infowindow.open({ anchor: marker, map, shouldFocus: false });
    });
}

function setMapOnAll(map) {
    markers.forEach(marker => marker.setMap(map));
}

function deleteMarkers() {
    setMapOnAll(null);
    markers = [];
}

function padTo2Digits(num) {
    return String(num).padStart(2, '0');
}
