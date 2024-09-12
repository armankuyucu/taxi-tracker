let map;
const BLUE_MARKER_URL = "https://maps.google.com/mapfiles/kml/paddle/blu-circle.png";
let markers = [];

// Car data for each user
const userCarData = {
    2: [34, 386],
    3: [292, 246]
};

// JavaScript to dynamically populate the select dropdown
function populateCarSelect(user_id, carData) {
    const carSelect = document.getElementById('car-select');
    carSelect.innerHTML = '<option selected>Please select a car</option>';

    if (carData[user_id]) {
        carData[user_id].forEach(carId => {
            const option = document.createElement('option');
            option.value = carId;
            option.textContent = `Car ${carId}`;
            carSelect.appendChild(option);
        });
    }
}

populateCarSelect(user_id, carData);

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 59.329326902597735, lng: 18.068576534807608 },
        zoom: 6,
    });

    const mydataJson = JSON.parse(JSON.parse(JSON.parse(document.getElementById('mydata').textContent)));
    const user_id = JSON.parse(JSON.parse(JSON.parse(document.getElementById('user_id').textContent)));

    let currentDate = new Date();
    document.getElementById("startHour").value = currentDate.getHours() - 1;
    const currentTime = `${padTo2Digits(currentDate.getHours())}:${padTo2Digits(currentDate.getMinutes())}`;

    // Car indexes by car ID
    let carIndexes = {
        34: [],
        386: [],
        292: [],
        246: []
    };

    let carCurrentIndexes = {};

    // Populate car indexes based on user data
    for (let i = 0; i < mydataJson.length; i++) {
        mydataJson[i].date_time = mydataJson[i].date_time.split(" ").slice(-1);
        if (mydataJson[i].user_id == user_id) {
            if (mydataJson[i].date_time == currentTime) {
                carCurrentIndexes[mydataJson[i].car_id] = i;
            }
            carIndexes[mydataJson[i].car_id].push(i);
        }
    }

    // Display last 30 minutes of data for each user's cars
    if (userCarData[user_id]) {
        userCarData[user_id].forEach((car_id, index) => {
            last30Minutes(user_id, carCurrentIndexes[car_id], mydataJson, index);
        });
    }

    document.getElementById("submit").onclick = function () {
        let startHour = document.getElementById("startHour").value;
        let endHour = document.getElementById("endHour").value;
        let car_id = document.querySelector('#car-select').value;

        if (car_id === "Please select a car") {
            alert("The 'Select a car' field can't be empty.");
        } else if (enforceMinMax(startHour, endHour)) {
            deleteMarkers();

            if (userCarData[user_id].includes(parseInt(car_id))) {
                let index = userCarData[user_id].indexOf(parseInt(car_id));
                showRoute(user_id, car_id, carIndexes[car_id][0], carIndexes[car_id][carIndexes[car_id].length - 1], mydataJson, index, startHour, endHour);
            }
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
function last30Minutes(user_id, carIndex, mydataJson, marker_id) {
    for (let i = carIndex; (carIndex - 30) < i; i--) {
        let coords = { lat: mydataJson[i].latitude, lng: mydataJson[i].longitude };
        let marker = marker_id === 0 ? addMarker(coords) : addBlueMarker(coords);
        addInfoWindow(marker, coords, mydataJson[i]);
    }
}

function showRoute(user_id, car_id, carFirstIndex, carLastIndex, mydataJson, marker_id, startHour, endHour) {
    for (let i = (carFirstIndex + startHour * 60); i < (carFirstIndex + endHour * 60); i++) {
        if (car_id == mydataJson[i].car_id) {
            let coords = { lat: mydataJson[i].latitude, lng: mydataJson[i].longitude };
            let marker = marker_id === 0 ? addMarker(coords) : addBlueMarker(coords);
            addInfoWindow(marker, coords, mydataJson[i]);
        }
    }
}

function addMarker(coords) {
    let marker = new google.maps.Marker({
        position: coords,
        map: map
    });
    markers.push(marker);
    return marker;
}

function addBlueMarker(coords) {
    let marker = new google.maps.Marker({
        position: coords,
        icon: BLUE_MARKER_URL,
        map: map
    });
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
