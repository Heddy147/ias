function Rest(app) {
	this.app = app;
	var self = this;

	this.doLogin = function(values) {
		self.ajax(values, "PUT", "/api/login", function(data) {
			location.reload();
		})
	};

	this.doRegister = function(values) {
		self.ajax(values, "POST", "/api/registrieren", function(data) {
			location.reload();
		})
	};

	this.getIndexData = function() {
		self.getFahrzeugKlassen(function(data) {
			self.app.render_px("rennleiter_index", data);
		});
	};

	this.getFahrzeugKlassen = function(callback) {
		self.ajax({}, "GET", "/api/fahrzeugklassen", function(data) {
			self.getRennen(data, callback);
		});
	};

	this.getRennen = function(old_data, callback) {
		self.ajax({}, "GET", "/api/rennen", function(data) {
			if(typeof old_data != "undefined") {
				for(var key in old_data) {
					data[key] = old_data[key];
				}
			}

			if(typeof callback != "undefined") {
				callback(data);
			}
		});
	};

	this.insertVehicle = function(values) {
		self.ajax(values, "POST", "/api/fahrzeugklassen", function(data) {
			self.getIndexData();
		});
	};

	this.editVehicleCategory = function(id) {
		self.ajax({id:id}, "GET", "/api/fahrzeugklassen", function(data) {
			self.app.render_px("rennleiter_editVehicleCategory", data);
		});
	};

	this.updateVehicle = function(values) {
		console.log(values);
		self.ajax(values, "PUT", "/api/fahrzeugklassen", function(data) {
			self.getIndexData();
		});
	};

	this.deleteVehicleCategory = function(id) {
		self.ajax({id:id}, "DELETE", "/api/fahrzeugklassen?id=" + id, function(data) {
			self.getIndexData();
		});
	};

	this.createRace = function(values) {
		rennDaten = {
			bezeichnung: values.race_bezeichnung,
			beschreibung: values.race_beschreibung,
			datum: values.race_datum
		};
		stationsDaten = {
			bezeichnung: values.station_bezeichnung,
			lage: values.station_lage,
			beschreibung: values.station_beschreibung
		};

		self.ajax(rennDaten, "POST", "/api/rennen", function(data) {
			stationsDaten.rennId = data.data.id;

			self.insertStation(stationsDaten);
		});
	};

	this.editRace = function(id) {
		self.ajax({id:id}, "GET", "/api/rennen", function(data) {
			self.app.render_px("rennleiter_editRace", data);
		});
	};

	this.updateRace = function(values) {
		console.log(values);
		self.ajax(values, "PUT", "/api/rennen", function(data) {
			self.getIndexData();
		});
	};

	this.insertStation = function(values) {
		self.ajax(values, "POST", "/api/stationen", function(data) {
			self.getIndexData();
		});
	};

	this.ajax = function(values, method, url, successCallback, failureCallback) {
		$.ajax({
			dataType: "json",
			url: url,
			type: method,
			data: values
		}).done(function(data) {
			if(data.success && typeof successCallback != "undefined") {
				successCallback(data);
			}

			if(!data.success && typeof failureCallback != "undefined") {
				failureCallback(data);
			} else if(!data.success && typeof data.message != "undefined") {
				alert(data.message);
			}
		});
	};
}