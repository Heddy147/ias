var LITAPP = {};

LITAPP.Application_cl = Class.create({
	initialize: function () {
		var self = this;
		this.rest = new Rest(this);

		LITAPP.es_o.subscribe_px(this, 'app');
	},
	notify_px: function (self_opl, message_spl, data_apl) {
		switch (message_spl) {
			case 'app':
				switch (data_apl[0]) {
					case 'init':
						LITAPP.tm_o = new TELIB.TemplateManager_cl();
						break;
					case 'templates.loaded':
						self_opl.rest.getIndexData();
//						self_opl.render_px('rennleiter_index', {});
						break;
					default:
						console.warning('[Application_cl] unbekannte app-Notification: '+data_apl[0]);
						break;
				}
				break;
			default:
				console.warning('[Application_cl] unbekannte Notification: '+message_spl);
				break;
		}
	},
	render_px: function(template_name, data) {
		var self = this;

		$('#content').html(LITAPP.tm_o.execute_px(template_name + '.html', data));

		$('button:not([type="submit"]), .function').click(function() {
			var action = $(this).data('action');
			if($(this).is('.function')) {
				action = 'function';
			}

			switch(action) {
				case 'page.switch.index':
					self.rest.getIndexData();
					break;
				case 'page.switch':
					var templateName = $(this).data('template-name');
					self.render_px(templateName);
					break;
				case 'function':
					var functionName = $(this).data('function');
					eval("self." + functionName + "(this);");
					break;
				default:
					console.log("Action unbekannt: " + action);
					break;
			}
		});

		if ($('form#login').length > 0) {
			$('form#login').submit(function(e) {
				e.preventDefault();
				var values = {};
				$(this).find('input').each(function() {
					values[$(this).attr('name')] = $(this).val();
				});
				self.rest.doLogin(values);
			});
		}

		if ($('form#registrieren').length > 0) {
			$('form#registrieren').submit(function(e) {
				e.preventDefault();
				var values = {};
				$(this).find('input').each(function() {
					values[$(this).attr('name')] = $(this).val();
				});
				self.rest.doRegister(values);
			});
		}

		if ($('form#createVehicleCategory').length > 0) {
			$('form#createVehicleCategory').submit(function(e) {
				e.preventDefault();
				var values = {};
				$(this).find('input').each(function() {
					values[$(this).attr('name')] = $(this).val();
				});
				self.rest.insertVehicleCategory(values);
			});
		}

		if ($('form#editVehicleCategory').length > 0) {
			$('form#editVehicleCategory').submit(function(e) {
				e.preventDefault();
				var values = {};
				$(this).find('input').each(function() {
					values[$(this).attr('name')] = $(this).val();
				});
				self.rest.updateVehicleCategory(values);
			});
		}

		if ($('form#editUserCar').length > 0) {
			$('form#editUserCar').submit(function(e) {
				e.preventDefault();
				var values = {};
				$(this).find('input,select').each(function() {
					values[$(this).attr('name')] = $(this).val();
				});
				self.rest.updateUserCar(values);
			});
		}

		if ($('form#createRace').length > 0) {
			$('form#createRace').submit(function(e) {
				e.preventDefault();
				var values = {};
				$(this).find('input').each(function() {
					values[$(this).attr('name')] = $(this).val();
				});
				self.rest.createRace(values, function(data) {
					self.rest.getIndexData();
				});
			});
		}

		if ($('form#editRace').length > 0) {
			$('form#editRace').submit(function(e) {
				e.preventDefault();
				var values = {};
				$(this).find('input').each(function() {
					values[$(this).attr('name')] = $(this).val();
				});
				self.rest.updateRace(values);
			});
		}

		if ($('form#createStation').length > 0) {
			$('form#createStation').submit(function(e) {
				e.preventDefault();
				var values = {};
				$(this).find('input').each(function() {
					values[$(this).attr('name')] = $(this).val();
				});
				self.rest.insertStation(values, function(data) {
					self.viewStations(data.data.rennId);
				});
			});
		}

		if ($('form#insertQualifying').length > 0) {
			$('form#insertQualifying').submit(function(e) {
				e.preventDefault();
				var values = {
					ergebnisse: {}
				};
				var rennId = $(this).find('[name="rennId"]').val();
				var zeiten = $(this).find('[name^="zeit_in_string"]');
				var stati = $(this).find('[name^="status"]');

				zeiten.each(function() {
					var aId = $(this).data('anmeldung-id');
					var value = $(this).val();

					if(typeof values.ergebnisse[aId] == "undefined") {
						values.ergebnisse[aId] = {};
					}

					values.ergebnisse[aId].zeit_in_string = value;
				});

				stati.each(function() {
					var aId = $(this).data('anmeldung-id');
					var value = $(this).val();

					if(typeof values.ergebnisse[aId] == "undefined") {
						values.ergebnisse[aId] = {};
					}

					values.ergebnisse[aId].status = value;
				});

				values.rennId = rennId;

				self.rest.insertQualifying(values);
			});
		}

		if($('form#insertRennergebnisse').length > 0) {
			$('form#insertRennergebnisse').submit(function(e) {
				e.preventDefault();
				var values = {
					ergebnisse: {}
				};
				var rennId = $(this).find('[name="rennId"]').val();
				var zeiten = $(this).find('[name^="zeit_in_string"]');
				var disqualis = $(this).find('[name^="disquali"]');
				var stationenOk = $(this).find('[name^="stationen_ok"]');

				zeiten.each(function() {
					var aId = $(this).data('anmeldung-id');
					var sId = $(this).data('station-id');
					var value = $(this).val();

					if(typeof values.ergebnisse[aId] == "undefined") {
						values.ergebnisse[aId] = {
							stationsErgebnisse: {}
						};
					}

					if(typeof values.ergebnisse[aId].stationsErgebnisse[sId] == "undefined") {
						values.ergebnisse[aId].stationsErgebnisse[sId] = {};
					}

					values.ergebnisse[aId].stationsErgebnisse[sId].zeit_in_string = value;
				});

				disqualis.each(function() {
					var aId = $(this).data('anmeldung-id');
					var value = $(this).val();

					if(typeof values.ergebnisse[aId] == "undefined") {
						values.ergebnisse[aId] = {};
					}

					values.ergebnisse[aId].disquali = value;
				});

				stationenOk.each(function() {
					var aId = $(this).data('anmeldung-id');
					var value = $(this).val();

					if(typeof values.ergebnisse[aId] == "undefined") {
						values.ergebnisse[aId] = {};
					}

					values.ergebnisse[aId].stationen_ok = value;
				});

				values.rennId = rennId;

				console.log(values);

				for(var a in values.ergebnisse) {
					for(var s in values.ergebnisse[a].stationsErgebnisse) {
						if(values.ergebnisse[a].disquali == 1) {
							var zeit_in_millisekunden = 0;
						} else {
							var zeit_in_string = values.ergebnisse[a].stationsErgebnisse[s].zeit_in_string;

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

						values.ergebnisse[a].stationsErgebnisse[s].zeit_in_millisekunden = zeit_in_millisekunden;
					}
				}

				values.ergebnisse = JSON.stringify(values.ergebnisse);
				self.rest.insertRennErgebnisse(values);
			});
		}

		if ($('form#editUserperson').length > 0) {
			$('form#editUserperson').submit(function(e) {
				e.preventDefault();
				var values = {};
				$(this).find('input').each(function() {
					values[$(this).attr('name')] = $(this).val();
				});
				self.rest.updateUserPerson(values);
			});
		}
	},

	editVehicleCategory: function(element) {
		var fId = $(element).data('id');

		this.rest.editVehicleCategory(fId);
	},

	deleteVehicleCategory: function(element) {
		var fId = $(element).data('id');

		this.rest.deleteVehicleCategory(fId);
	},

	editUserCar: function(element) {
		var uId = $(element).data('id');

		this.rest.editUserCar(uId);
	},

	editRace: function(element) {
		var rId = $(element).data('id');

		this.rest.editRace(rId);
	},

	deleteRace: function(element) {
		var rId = $(element).data('id');

		this.rest.deleteRace(rId);
	},

	addStationAfterRace: function(element) {
		var values = {};
		$('form#createRace').find('input').each(function() {
			values[$(this).attr('name')] = $(this).val();
		});

		this.rest.insertRaceWithStation(values);
	},

	addStation: function(element, rId) {
		if(typeof rId == "undefined") {
			rId = $(element).data('id');
		}

		this.render_px("rennleiter_createStation", {rennId: rId})
	},

	viewStations: function(element, rId) {
		if(typeof rId == "undefined") {
			rId = $(element).data('id');
		}

		this.rest.getStations(rId);
	},

	deleteStation: function(element) {
		var sId = $(element).data('id');

		this.rest.deleteStation(sId);
	},

	insertQualiErgebnisse: function(element) {
		var self = this;
		var rId = $(element).data('id');

		this.rest.getAnmeldungenOfRace(rId, function(data) {
			data.rennId = rId;
			self.render_px("rennleiter_qualifying", data);
		});
	},

	insertRennErgebnisse: function(element) {
		var self = this;
		var rId = $(element).data('id');
		this.rest.editRennAuswertung(rId);
	},

	editAnmeldungen: function(element, rId) {
		var self = this;

		if(typeof rId == "undefined") {
			rId = $(element).data('id');
		}

		this.rest.getAnmeldungenOfRace(rId, function(data) {
			data.rennId = rId;
			self.rest.getRennen(data, function(data2) {
				data.rennen = data2.rennen;
				self.render_px("rennleiter_anmeldungen", data);
			});
		});
	},

	editPerson: function(element) {
		var pId = $(element).data('id');

		this.rest.editUserPerson(pId);
	},

	logout: function(element) {
		this.rest.logout();
	},

	setCookie: function(cname, cvalue) {
		var d = new Date();
		d.setTime(d.getTime() + 60*60*1000);
		var expires = "expires=" + d.toUTCString();

		document.cookie = cname + "=" + cvalue + "; " + expires;
	},
	getCookie: function(cname) {
		var name = cname + "=";
		var ca = document.cookie.split(';');
		for(var i=0; i<ca.length; i++) {
			var c = ca[i];
			while(c.charAt(0) == '' && c != '') {
				c = c.substring(1);
			}
			if(c.indexOf(name) == 0) {
				return c.substring(name.length, c.length);
			}
		}
		return null;
	}
});

$(document).ready(function(){
	LITAPP.es_o  = new EventService_cl();
	LITAPP.app_o = new LITAPP.Application_cl();

	LITAPP.es_o.publish_px('app', ['init', null]);

});

function toggleStationen(el, aId) {
	el = $(el);

	var toggleEl = $('[data-id="' + aId + '"]');

	if(toggleEl.length > 0) {
		if(toggleEl.is(":visible")) {
			el.text("Stationen einblenden");
		} else {
			el.text("Stationen ausblenden");
		}

		toggleEl.slideToggle();
	}
}

// EOF