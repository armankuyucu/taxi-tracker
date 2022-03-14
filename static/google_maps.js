let map;

let distanceMatrix = [];
let routeOrder = [];
let routeOrderInt = [];
//To get numbers in a string
let regularExpression = /\d+/g;

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


    let currentDate = new Date();
    console.log(currentDate);
    const currentTime =
        padTo2Digits(currentDate.getHours()) + ':' + padTo2Digits(currentDate.getMinutes());
    console.log(currentTime);

    let car34indexes = [];
    let car386indexes = [];
    let car34index;
    let car386index;

    for (let i = 0; i < mydataJson.length; i++) {
        mydataJson[i].date_time = mydataJson[i].date_time.split(" ").slice(-1);
        if (mydataJson[i].user_id == user_id) {
            if (mydataJson[i].car_id == 34) {
                if (mydataJson[i].date_time == currentTime) {
                    car34index = i;
                } else {
                    // console.log("currentTime " + currentTime)
                    // console.log("date_time " + mydataJson[i].date_time)
                }
                car34indexes.push(i);
            } else if (mydataJson[i].car_id == 386) {
                if (mydataJson[i].date_time == currentTime) {
                    // console.log("GİRDİ")

                    car386index = i;
                    console.log("car386index " + car386index)
                } else {
                    // console.log("currentTime " + currentTime)
                    // console.log("date_time " + mydataJson[i].date_time)
                }
                car386indexes.push(i);
            }
        } else {
            // console.log("mydata.user_id " + mydataJson[i].user_id)
            // console.log("user_id " + user_id)

        }
    }

    for (let i = car386index; (car386index-30) < i; i--) {
        console.log("GİRDİ")
        let coords = {lat: mydataJson[i].latitude, lng: mydataJson[i].longitude}
        let marker = addMarker(coords)
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

    // for (let i = 0; i < 30; i++) {
    //     // markers.push((mydataJson[i].latitude, mydataJson[i].longitude))
    //     let coords = {lat: mydataJson[i].latitude, lng: mydataJson[i].longitude}
    //     addMarker(coords)
    //     // console.log(typeof (mydataJson[0].latitude));
    //     // let infowindow = new google.maps.InfoWindow({
    //     //     content: `lat:${coords.lat}, lng:${coords.lng},
    //     //               date:${mydataJson[i].date_time},
    //     //               car_id:${mydataJson[i].car_id}`
    //     // });
    //
    //     // marker.addListener("click", () => {
    //     //     infowindow.open({
    //     //         anchor: marker,
    //     //         map,
    //     //         shouldFocus: false,
    //     //     });
    //     // });
    // }

}


//Add marker function
function addMarker(coords) {
    let marker = new google.maps.Marker({
        position: coords,
        map: map
    });
    return marker;
}

function padTo2Digits(num) {
    return String(num).padStart(2, '0');
}