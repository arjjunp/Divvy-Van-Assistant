function initMap() {
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();
    var chicago = new google.maps.LatLng(41.85, -87.65);
    var map = new google.maps.Map(document.getElementById('map'),{
        zoom: 7,
        center: chicago
    });
    directionsRenderer.setMap(map);

    calculate_route(directionsService)
}


function calculate_route(ds) {
    request = {}
    fetch('./request_map.json')
        .then((response) => response.json())
        .then(data => Object.assign(request, data));

    ds.route(request)
        .then((result) => {
        directionsRenderer.setDirections(result);
        })
}