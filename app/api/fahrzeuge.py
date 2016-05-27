import json
from app.abstracts.rest import RestAbstract
from app.abstracts.model import ModelAbstract
from app.models.Fahrzeug import Fahrzeug
from app.models.Fahrzeugklasse import Fahrzeugklasse
from app.models.User import User


class Fahrzeuge(RestAbstract):
	def GET(self, id=None):
		super(Fahrzeuge, self).check_login()
		if self.user_allowed:
			if id is None:
				if User.logged_in_user.data["rolle"] == "leitung":
					fahrzeuge = Fahrzeug.find(None, 100000)
				else:
					fahrzeuge = Fahrzeug.find({"benutzerId": User.logged_in_user.data["id"]}, 100000)
			else:
				if User.logged_in_user.data["rolle"] == "leitung":
					fahrzeuge = Fahrzeug.find({"id": id})
				else:
					fahrzeuge = Fahrzeug.find({"benutzerId": User.logged_in_user.data["id"], "id": id})

			return json.dumps({
				"success": True,
				"fahrzeuge": ModelAbstract.get_data_of_objects(fahrzeuge)
			})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})

	def POST(
			self,
			marke,
			typ,
			baujahr,
			hubraum,
			leistung,
			beschreibung,
			kennzeichen,
			fahrerId,
			beifahrerId,
			mechanikerId
	):
		super(Fahrzeuge, self).check_login()
		if self.user_allowed:
			fahrzeug = Fahrzeug()
			fahrzeug.data["besitzer"] = User.logged_in_user.data["id"]
			fahrzeug.data["marke"] = marke
			fahrzeug.data["baujahr"] = baujahr
			fahrzeug.data["hubraum"] = hubraum
			fahrzeug.data["leistung"] = leistung
			fahrzeug.data["beschreibung"] = beschreibung
			fahrzeug.data["kennzeichen"] = kennzeichen

			### Müssen noch auf Korrektheit ueberprueft werden
			fahrzeugklasse = Fahrzeugklasse.find({"id": typ})
			if fahrzeugklasse is not None:
				fahrzeug.data["typ"] = 0 # dummy

			fahrzeug.data["fahrerId"] = 0 # dummy
			fahrzeug.data["beifahrerId"] = 0 # dummy
			fahrzeug.data["mechanikerId"] = 0 # dummy

			if fahrzeug.save():
				return json.dumps({
					"success": True,
					"data": fahrzeug.data
				})
			else:
				return json.dumps({
					"success": False,
					"messages": fahrzeug.required_fields_empty
				})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})

# EOF
