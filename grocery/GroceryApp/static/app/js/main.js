
<script>
// JavaScript code to detect user's location and update navbar
window.addEventListener('load', function() {
  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var latitude = position.coords.latitude;
      var longitude = position.coords.longitude;
      var userLocation = document.getElementById('userLocation');
      userLocation.textContent = 'Your Location: ' + latitude + ', ' + longitude;
    });
  } else {
    console.log('Geolocation is not supported by this browser.');
  }
});
</script>