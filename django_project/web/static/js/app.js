window.VP = {};

VP.map = function(options) {
    // Create a new Wicket instance. Used for converting wkt to leaflet object.
    this.wicketWkt = new Wkt.Wkt();
    this.init(options);
};

VP.map.prototype = {
    init: function(options) {
        this.options = options;

        this.initMap();
        this.initCropFields();
        this.initIndividualEntries();

        // Create layer control.
        L.control.layers(
            this.map.vp_options.baseLayers,
            this.map.vp_options.overlayLayers,
            {
                position: 'topleft'
            }
        ).addTo(this.map);

        if (options.draw === true) {
            // If draw is set to true (i.e. when adding or editing feature)
            // Initialise draw control.
            this.drawControl = this.initDrawControl();
            this.map.addControl(this.drawControl);

            // If feature exists (i.e. we are editing previously saved feature).
            if ($('form #' + this.options.geom_field_id).val() != '') {
                // Load feature we want to edit to layers and geometry input field.
                this.loadFeature();
            }
        }
    },

    initMap: function() {
        var self = this;

        // create a map in the "map" div, set the view to a given place and zoom
        this.map = L.map(this.options.map_id);

        this.map.vp_options = {};
        this.map.vp_options.baseLayers = {};
        this.map.vp_options.overlayLayers = {};

        this.setMapHeight();
        this.map.setView([0, 0], 3);

        // add an OpenStreetMap tile layer
        var osmTileLayer = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        });

        var openTopoMap = L.tileLayer.provider('OpenTopoMap');
        var googleLayer = new L.Google('SATELLITE');

        // Add layer for use in layer control.
        this.map.vp_options.baseLayers['Google Satellite'] = googleLayer;
        this.map.vp_options.baseLayers['OpenTopoMap'] = openTopoMap;
        // Add layer to make it initially active on map.
        this.map.addLayer(googleLayer);

        // On resize set new map height
        $(window).on('resize', function() {
            self.setMapHeight();
        });

    },

    setMapHeight: function() {
        var window_height = $(window).height();
        var topmenu_height = $('#topmenu').height();

        // Set map height. Map extends to the bottom of the window.
        $('#' + this.options.map_id).css('height', window_height - topmenu_height - 40);
    },

    initCropFields: function() {
        var self = this;
        var myCropFields = [];
        var otherCropFields = [];

        $.each(this.options.cropFields, function() {
            var leafletPolygon = self.wicketWkt.read(this.area).toObject();
            var color;

            self.setCropFieldStyle(leafletPolygon, this);
            self.setCropFieldPopup(leafletPolygon, this);

            if (this.creator_object.id === self.options.currentUserId) {
                myCropFields.push(leafletPolygon);
            } else {
                otherCropFields.push(leafletPolygon);
            }
        });

        // If user is logged in we can show layer with his features.
        if (this.options.currentUserId) {
            var myCropFieldsLayer = L.layerGroup(myCropFields);
            // Add layer for use in layer control.
            this.map.vp_options.overlayLayers['My Crop Fields'] = myCropFieldsLayer;
            // Add layer to make it initially active on map.
            this.map.addLayer(myCropFieldsLayer);

            var otherCropFieldsLayer = L.layerGroup(otherCropFields);
            // Add layer for use in layer control.
            this.map.vp_options.overlayLayers['Other Crop Fields'] = otherCropFieldsLayer;
            this.map.addLayer(otherCropFieldsLayer);
        } else {
            var otherCropFieldsLayer = L.layerGroup(otherCropFields);
            // Add layer for use in layer control.
            this.map.vp_options.overlayLayers['Crop Fields'] = otherCropFieldsLayer;
            this.map.addLayer(otherCropFieldsLayer);
        }
    },

    setCropFieldStyle: function(polygon, cropField) {
        if (cropField.number_of_incidents === 0) {
            color = '#009900';
        } else {
            color = '#FF3333';
        }

        polygon.setStyle({
            color: color,
            fillcolor: color,
            fillOpacity: 0.6,
            weight: 1
        });
    },

    setCropFieldPopup: function(polygon, cropField) {
        if (cropField.number_of_incidents) {
            var number_of_incidents = cropField.number_of_incidents;
        } else {
            var number_of_incidents = 0;
        }

        var html = '<div class="popup-content-wrapper">' +
            '<a href="' + cropField.url_detail + '"class="popup-heading">' +
                '<i class="fi-arrow-right"></i> ' +
                cropField.crop_name + '</a>' +
                '<p><span class="popup-prop">REPORTED PESTS AND DISEASES:</span> ' +
                number_of_incidents + '</p>' +
                '<p><span class="popup-prop">CREATED BY:</span> ' +
                cropField.creator_object.name + '</p>';

        if (this.options.currentUserId === cropField.creator_object.id) {
            html += '<a href="' + cropField.url_edit + '">edit...</a>'
        }

        html += '</div>';

        polygon.bindPopup(html);
    },

    initIndividualEntries: function() {
        var self = this;
        var myEntries = [];
        var otherEntries = [];

        $.each(this.options.individualEntries, function() {
            var leafletPoint = self.wicketWkt.read(this.location).toObject();

            var leafletPoint = L.circleMarker(
                [leafletPoint._latlng.lat, leafletPoint._latlng.lng]
            );

            self.setIndividualEntryStyle(leafletPoint, this);
            self.setIndividualEntryPopup(leafletPoint, this);


            if (this.creator_object.id === self.options.currentUserId) {
                myEntries.push(leafletPoint);
            } else {
                otherEntries.push(leafletPoint);
            }
        });

        // If user is logged in we can show layer with his features.
        if (this.options.currentUserId) {
            var myEntriesLayer = L.layerGroup(myEntries);
            // Add layer for use in layer control.
            this.map.vp_options.overlayLayers['My Pests and Diseases'] = myEntriesLayer;
            // Add layer to make it initially active on map.
            this.map.addLayer(myEntriesLayer);

            var otherEntriesLayer = L.layerGroup(otherEntries);
            // Add layer for use in layer control.
            this.map.vp_options.overlayLayers["Other Pests and Diseases"] = otherEntriesLayer;
            this.map.addLayer(otherEntriesLayer);
        } else {
            var otherEntriesLayer = L.layerGroup(otherEntries);
            // Add layer for use in layer control.
            this.map.vp_options.overlayLayers['Pests and Diseases'] = otherEntriesLayer;
            this.map.addLayer(otherEntriesLayer);
        }
    },

    setIndividualEntryStyle: function(point, entry) {
        point.setStyle({
            stroke: true,
            color: '#FFFFFF',
            weight: 2,
            opacity: 1,
            fill: true,
            fillColor: '#FF1919',
            fillOpacity: 0.8
        });
    },

    setIndividualEntryPopup: function(point, entry) {
        if (entry.type_object.typeId === '3') {
            var type = 'Unknown Pest or Disease';
        } else {
            var type = entry.type_object.name;
        }

        var html = '<div class="popup-content-wrapper">';

        if (entry.pest_disease_name != "") {
            html += '<a href="' + entry.url_detail + '"class="popup-heading">' +
                '<i class="fi-arrow-right"></i> ' +
                entry.pest_disease_name + '</a>' +
                '<p><span class="popup-prop">TYPE:</span> ' + type + '</p>';
        } else {
            html += '<a href="' + entry.url_detail + '" class="popup-heading">' +
                '<i class="fi-arrow-right"></i> ' + type + '</a>';
        }

        html += '<p><span class="popup-prop">OCCURENCE DATE:</span> ' + entry.occurence_date + '</p>' +
            '<p><span class="popup-prop">CREATED BY:</span> ' + entry.creator_object.name + '</p>';

        if (this.options.currentUserId === entry.creator_object.id) {
            html += '<a href="' + entry.url_edit + '">edit...</a>'
        }

        html += '</div>';

        point.bindPopup(html);
    },

    initDrawControl: function() {
        var self = this;
        // Create feature group that will hold all editable layers
        // (leaflet.draw requirement).
        this.editableFeatureGroup = new L.FeatureGroup();
        this.editableFeatureGroup.addTo(this.map);

        var drawControl = new L.Control.Draw({
            draw: {
                polyline: this.options.polyline,
                polygon: this.options.polygon,
                rectangle: this.options.rectangle,
                circle: this.options.circle,
                marker: this.options.marker,
            },
            edit: {
                featureGroup: this.editableFeatureGroup
            }
        });

        this.map.on('draw:created', function (e) {
            var feature = e.layer;

            // Add feature to editable layer.
            feature.addTo(self.editableFeatureGroup);

            // Dump feature to geometry input.
            $('form #' + self.options.geom_field_id)
            .val(JSON.stringify(feature.toGeoJSON()['geometry']));
        });

        this.map.on('draw:edited', function (e) {
            // Dump feature to geometry input.
            self.editableFeatureGroup.eachLayer(function(layer) {
                $('form #' + self.options.geom_field_id)
                .val(JSON.stringify(layer.toGeoJSON()['geometry']));
            });
        });

        this.map.on('draw:deleted', function (e) {
            $('form #' + self.options.geom_field_id).val('');
        });

        return drawControl
    },

    loadFeature: function() {
        var feature_geom = $('form #' + this.options.geom_field_id).val();

        // If feature is in geojson.
        if (feature_geom[0] == '{') {
            var geojson_feature = $.parseJSON(feature_geom);
            var layer = L.geoJson(geojson_feature);
            var feature = this.getFeatureFromLayer(layer);
        }
        else {
            // If feature is in WKT.
            var feature = this.wicketWkt.read(feature_geom).toObject();
        }

        // Add feature to editable layer.
        feature.addTo(this.editableFeatureGroup);
    },

    getFeatureFromLayer: function(layer) {
        // There is only one feature in layer, so loop will always go once.
        layer.eachLayer(function(layer) {
            editing_feature = layer
        });

        return editing_feature
    }
};
