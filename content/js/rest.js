var feldToName = {
	fahrzeugeId: "Fahrzeug",
	rennId: "Rennen",
	marke: "Marke",
	typ: "Fahrzeugklasse",
	baujahr: "Baujahr",
	hubraum: "Hubraum",
	leistung: "Leistung",
	kennzeichen: "Kennzeichen",
	fahrerId: "Fahrer",
	beifahrerId: "Beifahrer",
	mechanikerId: "Mechaniker",
	zeit_in_string: "Qualifikationszeit",
	vorname: "Vorname",
	nachname: "Nachname",
	bezeichnung: "Bezeichnung",
	beschreibung: "Beschreibung",
	datum: "Datum",
	lage: "Lage"
};

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

	this.getBesitzerIndexData = function() {
		var data = {};

		self.ajax({}, "GET", "/api/fahrzeuge", function(ajaxData) {
			data.fahrzeuge = ajaxData.fahrzeuge;
			self.app.render_px("besitzer_index", data);
		});

		self.ajax({}, "GET", "/api/anmeldungen", function(ajaxData) {
			data.anmeldungen = ajaxData.anmeldungen;
			self.app.render_px("besitzer_index", data);
		});

		self.ajax({}, "GET", "/api/personen", function(ajaxData) {
			data.personen = ajaxData.personen;
			self.app.render_px("besitzer_index", data);
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

	this.getStations = function(rennId) {
		self.ajax({rennId: rennId}, "GET", "/api/stationen", function(data) {
			data.rennId = rennId;
			self.app.render_px("rennleiter_viewStations", data);
		});
	};

	this.getAnmeldungenOfRace = function(rennId, callback) {
		self.ajax({rennId: rennId}, "GET", "/api/anmeldungen", callback);
	};

	this.insertVehicleCategory = function(values) {
		self.ajax(values, "POST", "/api/fahrzeugklassen", function(data) {
			self.getIndexData();
		});
	};

	this.editVehicleCategory = function(id) {
		self.ajax({id:id}, "GET", "/api/fahrzeugklassen", function(data) {
			self.app.render_px("rennleiter_editVehicleCategory", data);
		});
	};

	this.updateVehicleCategory = function(values) {
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

	this.editUserCar = function(id) {
		data = {};
		self.ajax({id:id}, "GET", "/api/fahrzeuge", function(ajaxData) {
			data.fahrzeuge = ajaxData.fahrzeuge;
			self.app.render_px("rennleiter_editUserCar", data);
		});
		self.ajax({}, "GET", "/api/personen", function(ajaxData) {
			data.personen = ajaxData.personen;
			self.app.render_px("rennleiter_editUserCar", data);
		});
		self.ajax({}, "GET", "/api/fahrzeugklassen", function(ajaxData) {
			data.fahrzeugklassen = ajaxData.fahrzeugklassen;
			self.app.render_px("rennleiter_editUserCar", data);
		});
	};

	this.updateUserCar = function(values) {
		self.ajax(values, "PUT", "/api/fahrzeuge", function(data) {
			self.ajax({}, "GET", "/api/rennen", function(data2) {
				self.app.editAnmeldungen(undefined, data2.rennen[0].id);
			});
		});
	};

	this.insertVehicle = function(values) {
		self.ajax(values, "POST", "/api/fahrzeuge", function(data) {
			self.getBesitzerIndexData();
		});
	};

	this.editVehicle = function(id) {
		data = {};
		self.ajax({id:id}, "GET", "/api/fahrzeuge", function(ajaxData) {
			data.fahrzeuge = ajaxData.fahrzeuge;
			self.app.render_px("besitzer_editCar", data);
		});
		self.ajax({}, "GET", "/api/personen", function(ajaxData) {
			data.personen = ajaxData.personen;
			self.app.render_px("besitzer_editCar", data);
		});
		self.ajax({}, "GET", "/api/fahrzeugklassen", function(ajaxData) {
			data.fahrzeugklassen = ajaxData.fahrzeugklassen;
			self.app.render_px("besitzer_editCar", data);
		});
	};

	this.updateVehicle = function(values) {
		self.ajax(values, "PUT", "/api/fahrzeuge", function(data) {
			self.getBesitzerIndexData();
		});
	};

	this.deleteVehicle = function(id) {
		self.ajax({id:id}, "DELETE", "/api/fahrzeuge?id=" + id, function(data) {
			self.getBesitzerIndexData();
		});
	};

	this.insertPerson = function(values) {
		self.ajax(values, "POST", "/api/personen", function(data) {
			self.getBesitzerIndexData();
		});
	};

	this.editPerson = function(id) {
		self.ajax({id:id}, "GET", "/api/personen", function(data) {
			self.app.render_px("besitzer_editPerson", data);
		});
	};

	this.updatePerson = function(values) {
		console.log(values);
		self.ajax(values, "PUT", "/api/personen", function(data) {
			self.getBesitzerIndexData();
		});
	};

	this.deletePerson = function(id) {
		self.ajax({id:id}, "DELETE", "/api/personen?id=" + id, function(data) {
			self.getBesitzerIndexData();
		});
	};

	this.editUserPerson = function(id) {
		self.ajax({id:id}, "GET", "/api/personen", function(data) {
			self.app.render_px("rennleiter_editPerson", data);
		});
	};

	this.updateUserPerson = function(values) {
		console.log(values);
		self.ajax(values, "PUT", "/api/personen", function(data) {
			self.ajax({}, "GET", "/api/rennen", function(data2) {
				self.app.editAnmeldungen(undefined, data2.rennen[0].id);
			});
		});
	};

	this.editRennAuswertung = function(rId) {
		this.getAnmeldungenOfRace(rId, function(data) {
			data.rennId = rId;
			self.ajax({rennId: rId}, 'GET', '/api/stationen', function(data2) {
				data.stationen = data2.stationen;
				self.app.render_px("rennleiter_rennauswertung", data);
			});
		});
	};

	this.createRace = function(values, callback) {
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

			self.insertStation(stationsDaten, callback);
		});
	};

	this.insertRaceWithStation = function(values) {
		this.createRace(values, function(data) {
			self.app.addStation(undefined, data.data.rennId);
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

	this.deleteRace = function(rId) {
		self.ajax({id: rId}, "DELETE", "/api/rennen?id=" + rId, function(data) {
			self.getIndexData();
		});
	};

	this.insertStation = function(values, callback) {
		self.ajax(values, "POST", "/api/stationen", callback);
	};

	this.loadDataForVehicle = function() {
		var data = {};
		self.ajax({}, "GET", "/api/fahrzeugklassen", function(ajaxData) {
			data.fahrzeugklassen = ajaxData.fahrzeugklassen;
			self.app.render_px("besitzer_createCar", data);
		});
		self.ajax({}, "GET", "/api/personen", function(ajaxData) {
			data.personen = ajaxData.personen;
			self.app.render_px("besitzer_createCar", data);
		});
	};

	this.createAnmeldung = function() {
		var data = {};

		self.ajax({}, "GET", "/api/rennen", function(ajaxData) {
			data.rennen = ajaxData.rennen;
			self.app.render_px("besitzer_registerForRace", data);
		});

		self.ajax({}, "GET", "/api/fahrzeuge", function(ajaxData) {
			data.fahrzeuge = ajaxData.fahrzeuge;
			self.app.render_px("besitzer_registerForRace", data);
		});
	};

	this.insertAnmeldung = function(values) {
		self.ajax(values, "POST", "/api/anmeldungen", function(data) {
			self.getBesitzerIndexData();
		});
	};

	this.deleteAnmeldung = function(aId) {
		self.ajax({id: aId}, "DELETE", "/api/anmeldungen?id=" + aId, function(data) {
			self.getBesitzerIndexData();
		});
	};

	this.deleteStation = function(aId) {
		self.ajax({id: aId}, "DELETE", "/api/stationen?id=" + aId, function(data) {
			self.app.viewStations(undefined, data.data.rennId);
		});
	};

	this.insertQualifying = function(values) {
		for(var a in values.ergebnisse) {
			if(values.ergebnisse[a].status == 2) {
				var zeit_in_millisekunden = 0;
			} else {
				var zeit_in_string = values.ergebnisse[a].zeit_in_string;

				if(zeit_in_string.length == 0) {
					alert("Jedes Fahrzeug muss eine Zeit erhalten oder disqualifiziert werden!");

					return;
				}

				var splittedZeit = zeit_in_string.split(':');
				if(splittedZeit.length < 3) {
					alert("Eine der eingetragenen Zeiten hat ein falsches Format.\nRichtiges Format: Minuten:Sekunden:Millisekunden");
					return;
				}

				var minuten = splittedZeit[0];
				var sekunden = splittedZeit[1];
				var millisekunden = splittedZeit[2];
				var zeit_in_millisekunden = (Number(minuten) * 60 + Number(sekunden)) * 1000 + Number(millisekunden);
			}

			values.ergebnisse[a].zeit_in_millisekunden = zeit_in_millisekunden;
		}

		self.ajax(values, "POST", "/api/qualiergebnisse", function(data) {
			self.getIndexData();
		});
	};

	this.insertRennErgebnisse = function(values) {
		self.ajax(values, "POST", "/api/rennergebnisse", function(data) {
			location.reload();
		});
	};

	this.logout = function() {
		self.ajax({}, "DELETE", "/api/login", function(data) {
			location.reload();
		});
	};

	this.ajax = function(values, method, url, successCallback, failureCallback) {
		if(typeof processData == "undefined") {
			processData = true;
		}
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
			} else if(!data.success && typeof data.messages != "undefined") {
				var msg = "Sie müssen folgende Felder ausfüllen:\n\n";

				var errors = [];
				for(var e in data.messages) {
					errors.push(feldToName[data.messages[e]]);
				}

				msg = msg + "- " + errors.join("\n- ");
				alert(msg);
			}
		});
	};
}