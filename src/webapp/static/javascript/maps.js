// daterange

$(function() {
  $('input[name="daterange"]').daterangepicker({
    opens: 'left'
  }, function(start, end, label) {
    console.log("A new date selection was made: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));
  });
});


// Initialize and add the map

const position = [25,46]

maptilersdk.config.apiKey = 'aq7LeCSjPMw8qSBWn3U9';
const map = new maptilersdk.Map({
container: 'map', // container's id or the HTML element to render the map
style: "dataviz",
center: position, // starting position [lng, lat]
zoom: 6, // starting zoom

});

const marker = new maptilersdk.Marker({
    color: "#FF0000",
    scale: 0.5
})
.setLngLat(position)
.addTo(map);

