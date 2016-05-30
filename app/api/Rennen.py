import json
from app.abstracts.rest import RestAbstract
from app.abstracts.model import ModelAbstract
from app.models.Rennen import Rennen as RennenModel
from app.models.User import User
from app.models.Anmeldung import Anmeldung
from app.models.Station import Station

class Rennen(RestAbstract):
	def GET(self, id=None):
		super(Rennen, self).check_login()
		if self.user_allowed:
			if User.logged_in_user.data["rolle"] == "leiter":
				if id is None:
					rennen = RennenModel.find({"leitungId": User.logged_in_user.data["id"], "beendet": 0})
				else:
					rennen = RennenModel.find({"id": id, "leitungId": User.logged_in_user.data["id"], "beendet": 0})
			else:
				if id is None:
					rennen = RennenModel.find({"beendet": 0}, 100000)
				else:
					rennen = RennenModel.find({"id": id, "beendet": 0})

			return json.dumps({
				"success": True,
				"rennen": ModelAbstract.get_data_of_objects(rennen)
			})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})

	def POST(
			self,
			bezeichnung,
			beschreibung,
			datum
	):
		super(Rennen, self).check_login()
		if self.user_allowed:
			rennen = RennenModel()
			rennen.data["leitungId"] = User.logged_in_user.data["id"]
			rennen.data["bezeichnung"] = bezeichnung
			rennen.data["beschreibung"] = beschreibung
			rennen.data["datum"] = datum
			rennen.data["beendet"] = False

			if rennen.save():
				return json.dumps({
					"success": True,
					"data": rennen.data
				})
			else:
				return json.dumps({
					"success": False,
					"messages": rennen.required_fields_empty
				})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})

	def PUT(
			self,
			id,
			bezeichnung,
			beschreibung,
			datum
	):
		super(Rennen, self).check_login()
		if self.user_allowed:
			rennen = RennenModel.find({"id": id})

			if rennen is None:
				return json.dumps({
					"success": False,
					"messages": "Fahrzeugklasse nicht vorhanden!"
				})

			rennen.data["bezeichnung"] = bezeichnung
			rennen.data["beschreibung"] = beschreibung
			rennen.data["datum"] = datum

			if rennen.save():
				return json.dumps({
					"success": True,
					"data": rennen.data
				})
			else:
				return json.dumps({
					"success": False,
					"messages": rennen.required_fields_empty
				})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})

	def DELETE(self, id):
		super(Rennen, self).check_login()
		if self.user_allowed:
			rennen = RennenModel.find({"id": id})

			if rennen is None:
				return json.dumps({
					"success": False,
					"messages": "Fahrzeugklasse nicht vorhanden!"
				})

			anmeldungen = Anmeldung.find({"rennId": rennen.data["id"]}, 10000)
			for a in anmeldungen:
				a.delete()

			stationen = Station.find({"rennId": rennen.data["id"]}, 10000)
			for s in stationen:
				s.delete()

			rennen.delete()

			return json.dumps({
				"success": True
			})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})


# EOF
