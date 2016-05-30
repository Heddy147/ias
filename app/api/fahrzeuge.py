import json
from app.abstracts.rest import RestAbstract
from app.abstracts.model import ModelAbstract
from app.models.Fahrzeug import Fahrzeug
from app.models.Fahrzeugklasse import Fahrzeugklasse
from app.models.User import User
from app.models.Person import Person
from app.models.Anmeldung import Anmeldung


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
			fahrzeug.data["benutzerId"] = User.logged_in_user.data["id"]
			fahrzeug.data["marke"] = marke
			fahrzeug.data["baujahr"] = baujahr
			fahrzeug.data["hubraum"] = hubraum
			fahrzeug.data["leistung"] = leistung
			fahrzeug.data["beschreibung"] = beschreibung
			fahrzeug.data["kennzeichen"] = kennzeichen

			### Müssen noch auf Korrektheit ueberprueft werden
			fahrzeugklasse = Fahrzeugklasse.find({"id": typ})
			if fahrzeugklasse is None and len(typ) > 0:
				return json.dumps({
					"success": False,
					"message": "Fahrzeugklasse existiert nicht!"
				})
			fahrzeug.data["typ"] = typ

			fahrer = Person.find({"id": fahrerId})
			if fahrer is None and len(fahrerId) > 0:
				return json.dumps({
					"success": False,
					"message": "Fahrer existiert nicht!"
				})
			fahrzeug.data["fahrerId"] = fahrerId

			beifahrer = Person.find({"id": beifahrerId})
			if beifahrer is None and len(beifahrerId) > 0:
				return json.dumps({
					"success": False,
					"message": "Beifahrer existiert nicht!"
				})
			fahrzeug.data["beifahrerId"] = beifahrerId

			mechaniker = Person.find({"id": mechanikerId})
			if mechaniker is None and len(mechanikerId) > 0:
				return json.dumps({
					"success": False,
					"message": "Mechaniker existiert nicht!"
				})
			fahrzeug.data["mechanikerId"] = mechanikerId

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

	def PUT(
			self,
			id,
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
			fahrzeug = Fahrzeug.find({"id": id})

			if fahrzeug is None:
				return json.dumps({
					"success": False,
					"messages": "Fahrzeugklasse nicht vorhanden!"
				})

			fahrzeug.data["besitzer"] = User.logged_in_user.data["id"]
			fahrzeug.data["marke"] = marke
			fahrzeug.data["baujahr"] = baujahr
			fahrzeug.data["hubraum"] = hubraum
			fahrzeug.data["leistung"] = leistung
			fahrzeug.data["beschreibung"] = beschreibung
			fahrzeug.data["kennzeichen"] = kennzeichen

			### Müssen noch auf Korrektheit ueberprueft werden
			fahrzeugklasse = Fahrzeugklasse.find({"id": typ})
			if fahrzeugklasse is None:
				return json.dumps({
					"success": False,
					"message": "Fahrzeugklasse existiert nicht!"
				})
			fahrzeug.data["typ"] = typ

			fahrer = Person.find({"id": fahrerId})
			if fahrer is None:
				return json.dumps({
					"success": False,
					"message": "Fahrer existiert nicht!"
				})
			fahrzeug.data["fahrerId"] = fahrerId

			beifahrer = Person.find({"id": beifahrerId})
			if beifahrer is None:
				return json.dumps({
					"success": False,
					"message": "Beifahrer existiert nicht!"
				})
			fahrzeug.data["beifahrerId"] = beifahrerId

			mechaniker = Person.find({"id": mechanikerId})
			if mechaniker is None:
				return json.dumps({
					"success": False,
					"message": "Mechaniker existiert nicht!"
				})
			fahrzeug.data["mechanikerId"] = mechanikerId

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

	def DELETE(self, id):
		super(Fahrzeuge, self).check_login()
		if self.user_allowed:
			fahrzeug = Fahrzeug.find({"id": id})

			if fahrzeug is None:
				return json.dumps({
					"success": False,
					"messages": "Fahrzeug nicht vorhanden!"
				})

			anmeldungen = Anmeldung.find({"fahrzeugId": fahrzeug.data["id"]}, 10000)
			for a in anmeldungen:
				a.delete()

			fahrzeug.delete()

			return json.dumps({
				"success": True
			})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})

# EOF
