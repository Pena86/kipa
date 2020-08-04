
var map = L.map('mapid').setView([60.171318, 24.93639], 13);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
	maxZoom: 17,
	minZoom: 4,
	attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
		'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
		'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
	id: 'mapbox/streets-v11',
	tileSize: 512,
	zoomOffset: -1
}).addTo(map);

L.control.scale().addTo(map);


var group = L.featureGroup()
	.bindPopup("Hello world!<br /><input type='button' value='Delete this marker' class='marker-delete-button'/>")
	//.on('click', function() { alert('Clicked on a member of the group!'); })
	.on("popupopen", onPopupOpen)
	.on("click", markerOnClick)
	.addTo(map);
	
var baseLayers = {};

var overlayMaps = {
	"Cities": group
};

L.control.layers(baseLayers, overlayMaps).addTo(map);


function markerMoveEnd(e){
	readMarkersFromMap()
}

function onMapClick(e) {
	addMarker(e);
	readMarkersFromMap()
}

map.on('click', onMapClick);

var lastMarkerClickedID = NaN;

function markerOnClick(e){
	lastMarkerClickedID = e.sourceTarget._leaflet_id;
}

function addMarker(e){
	// Add marker to map at click location;
	var newMarker = new L.marker(e.latlng, {
		title: "test title",
		alt: "test title",
		draggable: true,
		autoPan: true,
	}).addTo(group)
	.on("moveend", markerMoveEnd)
}

function onPopupOpen(e) {
	// To remove marker on click of delete
	$(".marker-delete-button:visible").click(function () {
		group.removeLayer(lastMarkerClickedID);
		map.closePopup();
		readMarkersFromMap()
	});
}


function mapZoomBounds() {
	for (var m in map._layers){
		if (map._layers[m].hasOwnProperty('_icon')) { 
			map.fitBounds(group.getBounds().pad(0.3));
			break;
		}
	}
}

function readMarkersFromMap() {
	var markerText = ""
	var markers = []
	for (var m in map._layers){
		if (map._layers[m].hasOwnProperty('_icon')) { 
			markerText += m + " " + map._layers[m]._latlng.toString() + " " + map._layers[m].options.title + "\r\n";
			markers.push({lid: m, latlng: map._layers[m]._latlng.toString(), title: map._layers[m].options.title});
		}
	}
	$("#markers_list").text(JSON.stringify(markers));
	console.log(markers);
}


markers = [{"id":"43","lat":"60.171318","lng":"24.93639","title":"test"},{"id":"45","lat":"60.164572","lng":"24.957161","title":"test"},{"id":"57","lat":"60.164999","lng":"24.927979","title":"test title"},{"id":"60","lat":"60.162693","lng":"24.93381)","title":"test title"}];

function setMarkersToMap(markers){
	console.log(markers)
	for (m in markers){
		new L.marker([parseFloat(markers[m].lat), parseFloat(markers[m].lng)], {
			title: markers[m].title,
			alt: markers[m].title,
			draggable: true,
			autoPan: true,
		}).addTo(group)
		.on("moveend", markerMoveEnd)
	}
	mapZoomBounds()
}


$(document).ready(function(){
	setMarkersToMap(markers)
	//readMarkersFromFile()
	readMarkersFromMap()
	
	
	$(".map-bounds-button").click(function () {
		mapZoomBounds()
	});
});
