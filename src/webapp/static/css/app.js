// document.addEventListener('DOMContentLoaded', function()
// {function initMap() {
//     var mapOptions = {
//         center: { lat: 44.434504431831094, lng: 26.100835858813607 }, // Set initial coordinates
//         zoom: 8, // Set initial zoom level
//     };

//     var map = new google.maps.Map(document.getElementById('map'), mapOptions);

//     // Initialize a marker
//     var marker = new google.maps.Marker({
//         map: map,
//         draggable: true,
//     });

//     // Event listener for when the marker is dragged
//     google.maps.event.addListener(marker, 'dragend', function(event) {
//         document.getElementById('latitude').value = event.latLng.lat();
//         document.getElementById('longitude').value = event.latLng.lng();
//     });

//     // Event listener for when the map is clicked to move the marker
//     google.maps.event.addListener(map, 'click', function(event) {
//         marker.setPosition(event.latLng);
//         document.getElementById('latitude').value = event.latLng.lat();
//         document.getElementById('longitude').value = event.latLng.lng();
//     });
// }

// // Handle form submission
// // document.getElementById('locationForm').addEventListener('submit', function(event) {
// //     event.preventDefault();

// //     // Gather form data including latitude and longitude
// //     var formData = new FormData(this);

// //     // Perform any further processing or data submission here
// //     // For example, you can use JavaScript or send the data to a server via AJAX
// //     console.log('Form Data:', formData);
// // });
// document.getElementById('locationForm').addEventListener('submit', function(event) {
//     event.preventDefault();

//     // Gather form data including latitude and longitude
//     var formData = new FormData(this);

//     // Perform any further processing or data submission here
//     // For example, you can use JavaScript or send the data to a server via AJAX
//     console.log('Form Data:', formData);
// });});


// var map;
//         var marker;
        

//         function initMap() {
//             var mapOptions = {
//                 center: { lat: 44.5, lng: 26 }, // Set initial coordinates
//                 zoom: 8, // Set initial zoom level
//             };

//             map = new google.maps.Map(document.getElementById('map'), mapOptions);

//             marker = new google.maps.Marker({
//                 map: map,
//                 draggable: true,
//             });

//             // Event listener for when the marker is dragged
//             google.maps.event.addListener(marker, 'dragend', function(event) {
//                 document.getElementById('latitude').value = event.latLng.lat();
//                 document.getElementById('longitude').value = event.latLng.lng();
//             });

//             // Event listener for when the map is clicked to move the marker
//             google.maps.event.addListener(map, 'click', function(event) {
//                 marker.setPosition(event.latLng);
//                 document.getElementById('latitude').value = event.latLng.lat();
//                 document.getElementById('longitude').value = event.latLng.lng();
//             });
//         }

//         // Handle form submission
//         document.getElementById('locationForm').addEventListener('submit', function(event) {
//             event.preventDefault();

//             // Gather form data including latitude and longitude
//             var formData = new FormData(this);

//             // Perform any further processing or data submission here
//             // For example, you can use JavaScript or send the data to a server via AJAX
//             console.log('Form Data:', formData);
//         });
var map;
    var marker;

    function initMap() {
        var mapOptions = {
            center: { lat: 0, lng: 0 }, // Set initial coordinates
            zoom: 8, // Set initial zoom level
        };

        map = new google.maps.Map(document.getElementById('map'), mapOptions);

        marker = new google.maps.Marker({
            map: map,
            draggable: true,
        });

        // Event listener for when the marker is dragged
        google.maps.event.addListener(marker, 'dragend', function(event) {
            document.getElementById('latitude').value = event.latLng.lat();
            document.getElementById('longitude').value = event.latLng.lng();
        });

        // Event listener for when the map is clicked to move the marker
        google.maps.event.addListener(map, 'click', function(event) {
            marker.setPosition(event.latLng);
            document.getElementById('latitude').value = event.latLng.lat();
            document.getElementById('longitude').value = event.latLng.lng();
        });
    }

    // Handle form submission
    document.getElementById('locationForm').addEventListener('submit', function(event) {
        event.preventDefault();

        // Gather form data including latitude and longitude
        var formData = new FormData(this);

        // Add "Name" and "Password" fields to the form data
        //var name = document.getElementById('name').value;
        //var password = document.getElementById('password').value;
        //formData.append('name', name);
        //formData.append('password', password);

        // Perform any further processing or data submission here
        // For example, you can use JavaScript or send the data to a server via AJAX
        console.log('Form Data:', formData);
    });