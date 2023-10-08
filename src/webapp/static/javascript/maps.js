// daterange

$(function() {
  $('input[name="date-range"]').daterangepicker({
    opens: 'left'
  }, function(start, end, label) {
    console.log("A new date selection was made: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));
  });
});

/*
$(document).ready(function () {
  $('#dateRangePicker').daterangepicker();

  $('#dateRangePicker').on('apply.daterangepicker', function (ev, picker) {
      var dateRange = picker.startDate.format('YYYY-MM-DD') + ' to ' + picker.endDate.format('YYYY-MM-DD');

      // Send a POST request using fetch API
      fetch('/process_date_range', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ date_range: dateRange })
      })
      .then(response => response.json())
      .then(data => {
          // Handle the response from the server
          console.log('POST request successful:', data);
      })
      .catch(error => {
          // Handle any errors that occur during the request
          console.error('POST request failed:', error);
      });
  });
});
*/

// Initialize and add the map

const position = [25,46]

maptilersdk.config.apiKey = 'aq7LeCSjPMw8qSBWn3U9';
const map = new maptilersdk.Map({
container: 'map', // container's id or the HTML element to render the map
style: "2120e825-c27b-4424-bbc8-b0b1d3afeceb",
center: position, // starting position [lng, lat]
zoom: 6, // starting zoom

});

const marker = new maptilersdk.Marker({
    color: "#FF0000",
    scale: 0.5
})
.setLngLat(position)
.addTo(map);

