var map = L.map('mapid', {editable: true}).setView([60.171318, 24.93639], 13);

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

L.BoundsControl = L.Control.extend({

	options: {
		position: 'topleft',
	},

	onAdd: function (map) {
		var container = L.DomUtil.create('div', 'leaflet-control leaflet-bar'),
			link = L.DomUtil.create('a', '', container);

		link.href = '#';
		link.title = 'Fit to bounds';
		link.innerHTML = '><'
		L.DomEvent.on(link, 'click', function () {
					window.LAYER = mapZoomBounds();
				  }, this);

		L.DomEvent.disableClickPropagation(container);
		return container;
	}

});
map.addControl(new L.BoundsControl());

L.control.scale().addTo(map);

function onMapClick(e) {
	addMarker({latlng: e.latlng});
	readMarkersFromMap()
}

map.on('click', onMapClick);


var group = L.featureGroup()
	.bindPopup("Hello world!<br />Something has gone wrong. The script has not loaded correctly")
	.on("click", markerOnClick)
	.addTo(map);
	
var pathGroup = L.featureGroup()
	.addTo(map);

var baseLayers = {};

var overlayMaps = {
	"Markers": group,
	"Path": pathGroup,
};

L.control.layers(baseLayers, overlayMaps).addTo(map);


function markerMoveEnd(e){
	readMarkersFromMap()
}

function mapZoomBounds() {
	if (group.getLayers().length) {
		map.fitBounds(group.getBounds().pad(0.3));
	}
}

var lastMarkerClickedID = NaN;

function markerOnClick(e){
	lastMarkerClickedID = e.sourceTarget._leaflet_id;
	//console.log(group._popup._content);
	//console.log(group.getLayer(lastMarkerClickedID), lastMarkerClickedID);
	group._popup.setContent(
		"<br /><input type='text' class='marker-title' name='marker-title' value='" + group.getLayer(lastMarkerClickedID).options.title + "'>" +
		"<input type='button' value='Update title' class='marker-update-button'/>" +
		"<br /><input type='button' value='Delete this marker' class='marker-delete-button'/>")
	group._popup.update();
	// To update marker title on click
	$(".marker-update-button:visible").click(function () {
		group.getLayer(lastMarkerClickedID).options.title = $(".marker-title").val()
		readMarkersFromMap()
	});
	// To remove marker on click
	$(".marker-delete-button:visible").click(function () {
		group.removeLayer(lastMarkerClickedID);
		map.closePopup();
		readMarkersFromMap()
	});
}

function addMarker({latlng, title="new", id=""}){
	// Add marker to map;
	var marker = new L.marker(latlng, {
		title: title,
		draggable: true,
		id: id,
	}).addTo(group)
	.on("moveend", markerMoveEnd)
}


function readMarkersFromMap() {
	// For updating html form in page
	console.log(group.getLayers());
	var markerText = ""
	var markers = []
	for (var m in group.getLayers()){
		markerText += group.getLayers()[m]._leaflet_id + " " + group.getLayers()[m]._latlng.toString() + " " + group.getLayers()[m].options.title + "\r\n";
		markers.push({lid: group.getLayers()[m]._leaflet_id, latlng: group.getLayers()[m]._latlng.toString(), title: group.getLayers()[m].options.title});
	}
	$("#markers_list").text(JSON.stringify(markers));
}


var markers = [{"id":"43","lat":"60.171318","lng":"24.93639","title":"test"},{"id":"45","lat":"60.164572","lng":"24.957161","title":"test"},{"id":"57","lat":"60.164999","lng":"24.927979","title":"test title"},{"id":"60","lat":"60.162693","lng":"24.93381)","title":"test title"}];
//var markers = [];

function setMarkersToMap(markers){
	// Set markers to map on startup
	//console.log(markers)
	for (m in markers){
		addMarker({
			latlng: [parseFloat(markers[m].lat), parseFloat(markers[m].lng)],
			title: markers[m].title,
			id: markers[m].id,
		})
	}
	mapZoomBounds()
	//console.log(group.getLayers());
}


var latlngs = [
	[60.162693, 24.93381],
	[60.183184, 24.945831],
	[60.179343, 24.986687],
	[60.163376, 25.017071]
];

var polyline = L.polyline(latlngs, {color: 'red'}).addTo(pathGroup);
polyline.enableEdit();
//polyline.on('dblclick', L.DomEvent.stop).on('dblclick', polyline.toggleEdit);


$(document).ready(function(){
	setMarkersToMap(markers)
	//readMarkersFromFile()
	readMarkersFromMap()
	
	
	$(".map-bounds-button").click(function () {
		mapZoomBounds()
	});
});
