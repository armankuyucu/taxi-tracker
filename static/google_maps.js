let map;

const blueMarker = "https://maps.google.com/mapfiles/kml/paddle/blu-circle.png";
let markers = [];

function initMap() {

    map = new google.maps.Map(document.getElementById("map"), {
            center: {lat: 59.329326902597735, lng: 18.068576534807608},
            zoom: 6,
        }
    );

    const mydata = JSON.parse(document.getElementById('mydata').textContent);
    // const new_data = mydata.replace("[","'")
    let mydataJson = JSON.parse(mydata);
    mydataJson = JSON.parse(mydataJson);
    // console.log(mydataJson)

    const userId = JSON.parse(document.getElementById('user_id').textContent);
    // const new_data = mydata.replace("[","'")
    let user_id = JSON.parse(userId);
    user_id = JSON.parse(user_id);
    console.log("user_id " + user_id);

    let currentDate = new Date();
    console.log(currentDate);
    document.getElementById("startHour").value = currentDate.getHours() - 1;
    const currentTime =
        padTo2Digits(currentDate.getHours()) + ':' + padTo2Digits(currentDate.getMinutes());
    console.log(currentTime);

    let car34indexes = [];
    let car386indexes = [];
    let car292indexes = [];
    let car246indexes = [];
    let car34index;
    let car386index;
    let car292index;
    let car246index;

    for (let i = 0; i < mydataJson.length; i++) {
        mydataJson[i].date_time = mydataJson[i].date_time.split(" ").slice(-1);
        if (mydataJson[i].user_id == user_id) {

            if (mydataJson[i].car_id == 34) {
                if (mydataJson[i].date_time == currentTime) {
                    car34index = i;
                }
                car34indexes.push(i);
            } else if (mydataJson[i].car_id == 386) {
                if (mydataJson[i].date_time == currentTime) {
                    // console.log("GİRDİ")
                    car386index = i;
                    // console.log("car386index " + car386index)
                }
                car386indexes.push(i);
            } else if (mydataJson[i].car_id == 292) {
                if (mydataJson[i].date_time == currentTime) {
                    // console.log("GİRDİ")
                    car292index = i;
                    // console.log("car386index " + car386index)
                }
                car292indexes.push(i);
            } else if (mydataJson[i].car_id == 246) {
                if (mydataJson[i].date_time == currentTime) {
                    // console.log("GİRDİ")
                    car246index = i;
                    // console.log("car386index " + car386index)
                }
                car246indexes.push(i);
            }

        }
    }

    if (user_id == 2) {
        last30Minutes(user_id, car34index, mydataJson, 0);
        last30Minutes(user_id, car386index, mydataJson, 1);
    } else if (user_id == 3) {
        last30Minutes(user_id, car292index, mydataJson, 0);
        last30Minutes(user_id, car246index, mydataJson, 1);
    }

    document.getElementById("submit").onclick = function () {
        let startHour = document.getElementById("startHour").value;
        let endHour = document.getElementById("endHour").value;
        let carSelect = document.querySelector('#car-select');
        let car_id = carSelect.value;
        if (car_id == "Please select a car") {
            alert("The \"Select a car\" field can't be empty.");
        } else {
            if (enforceMinMax(startHour, endHour)) {
                deleteMarkers();

                if (user_id == 2) {

                    if (car_id == 34)
                        showRoute(user_id, car_id, car34indexes[0], car34indexes[-1], mydataJson, 0, startHour, endHour);
                    else if (car_id == 386)
                        showRoute(user_id, car_id, car386indexes[0], car386indexes[-1], mydataJson, 1, startHour, endHour)
                } else if (user_id == 3) {

                    if (car_id == 292)
                        showRoute(user_id, car_id, car292indexes[0], car292indexes[-1], mydataJson, 0, startHour, endHour);
                    else if (car_id == 246)
                        showRoute(user_id, car_id, car246indexes[0], car246indexes[-1], mydataJson, 1, startHour, endHour);
                    else
                        console.log(car_id)
                }
            }
        }
    }

}


function enforceMinMax(startHour, endHour) {

    if (-1 < parseInt(startHour) && parseInt(startHour) < 25
        && -1 < parseInt(endHour) && parseInt(endHour) < 25) {
        return true;
    } else {
        alert("Please enter a number between 0 and 24")
        return false;
    }
}


// shows the route for the last 30 minutes
function last30Minutes(user_id, carIndex, mydataJson, marker_id) {
    for (let i = carIndex; (carIndex - 30) < i; i--) {
        let coords = {lat: mydataJson[i].latitude, lng: mydataJson[i].longitude}
        let marker;
        if (marker_id === 0) {
            marker = addMarker(coords);
        } else if (marker_id === 1) {
            marker = addBlueMarker(coords);
        }

        // console.log(typeof (mydataJson[0].latitude));
        let infowindow = new google.maps.InfoWindow({
            content: `lat:${coords.lat}, lng:${coords.lng},
                      date:${mydataJson[i].date_time},
                      car_id:${mydataJson[i].car_id}`
        });
        marker.addListener("click", () => {
            infowindow.open({
                anchor: marker,
                map,
                shouldFocus: false,
            });
        });
    }

}


function showRoute(user_id, car_id, carFirstIndex, carLastIndex, mydataJson, marker_id, startHour, endHour) {
    let counter = 0;
    for (let i = (carFirstIndex + startHour * 60); i < (carFirstIndex + endHour * 60); i++) {
        if (car_id == mydataJson[i].car_id) {
            let coords = {lat: mydataJson[i].latitude, lng: mydataJson[i].longitude};
            let marker;
            if (marker_id === 0) {
                marker = addMarker(coords);
            } else if (marker_id === 1) {
                marker = addBlueMarker(coords);
            }

            // console.log(typeof (mydataJson[0].latitude));
            let infowindow = new google.maps.InfoWindow({
                content: `lat:${coords.lat}, lng:${coords.lng},
                      date:${mydataJson[i].date_time},
                      car_id:${mydataJson[i].car_id}`
            });
            marker.addListener("click", () => {
                infowindow.open({
                    anchor: marker,
                    map,
                    shouldFocus: false,
                });
            });
        }
    }
}


//Add marker function
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
        icon: blueMarker,
        map: map
    });
    markers.push(marker);
    return marker;
}

// Sets the map on all markers in the array.
function setMapOnAll(map) {
    for (let i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }
}


// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
    setMapOnAll(null);
    markers = [];
}

function padTo2Digits(num) {
    return String(num).padStart(2, '0');
}
