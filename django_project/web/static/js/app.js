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
        // create a map in the "map" div, set the view to a given place and zoom
        this.map = L.map(this.options.map_id).setView([0, 0], 3);

        // add an OpenStreetMap tile layer
        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(this.map);
    },

    initCropFields: function() {
        var self = this;

        $.each(this.options.cropFields, function() {
            var lealfetPolygon = self.wicketWkt.read(this.area).toObject();
            var color;

            if (this.number_of_incidents === 0) {
                color = '#89E189';
            } else {
                color = '#FF3333';
            }

            lealfetPolygon
                .bindPopup(this.crop_name)
                .addTo(self.map)
                .setStyle({
                    color: color,
                    fillcolor: color,
                    weight: 1
                });
        });
    },

    initIndividualEntries: function() {
        var self = this;

        $.each(this.options.individualEntries, function() {
            var lealfetPoint = self.wicketWkt.read(this.location).toObject();

            lealfetPoint
                .bindPopup('test')
                .addTo(self.map);
        });
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
