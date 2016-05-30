import json
from app.abstracts.rest import RestAbstract
from app.abstracts.model import ModelAbstract
from app.models.Anmeldung import Anmeldung
from app.models.Rennen import Rennen
from app.models.Fahrzeug import Fahrzeug
from app.models.User import User

class Anmeldungen(RestAbstract):
	def GET(self, id=None, rennId=None, fahrzeugId=None):
		super(Anmeldungen, self).check_login()
		if self.user_allowed:
			conditions = {}
			if id is not None:
				conditions["id"] = id

			if rennId is not None:
				conditions["rennId"] = rennId

			if fahrzeugId is not None:
				conditions["fahrzeugId"] = fahrzeugId

			if User.logged_in_user.data["rolle"] != "leitung":
				conditions["benutzerId"] = User.logged_in_user.data["id"]

			anmeldung = Anmeldung.find(conditions, 100000)

			return json.dumps({
				"success": True,
				"anmeldungen": ModelAbstract.get_data_of_objects(anmeldung)
			})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})

	def POST(
			self,
			rennId,
			fahrzeugId
	):
		super(Anmeldungen, self).check_login()
		if self.user_allowed:
			rennen = Rennen.find({"id": rennId})
			if rennen is None:
				return json.dumps({
					"success": False,
					"message": "Rennen nicht gefunden!"
				})
			fahrzeug = Fahrzeug.find({"id": fahrzeugId})
			if fahrzeug is None:
				return json.dumps({
					"success": False,
					"message": "Fahrzeug nicht gefunden!"
				})
			existingAnmeldung = Anmeldung.find({"fahrzeugId": fahrzeug.data["id"], "rennId": rennen.data["id"]})
			if existingAnmeldung is not None:
				return json.dumps({
					"success": False,
					"message": "Sie haben sich mit diesem Fahrzeug schon an diesem Rennen angemeldet!"
				})

			anmeldung = Anmeldung()
			anmeldung.data["rennId"] = rennId
			anmeldung.data["fahrzeugId"] = fahrzeugId
			anmeldung.data["benutzerId"] = User.logged_in_user.data["id"]

			if anmeldung.save():
				return json.dumps({
					"success": True,
					"data": anmeldung.data
				})
			else:
				return json.dumps({
					"success": False,
					"messages": anmeldung.required_fields_empty
				})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})

	def PUT(
			self,
			id,
			rennId,
			fahrzeugId
	):
		super(Anmeldungen, self).check_login()
		if self.user_allowed:
			anmeldung = Anmeldung.find({"id": id})

			if anmeldung is None:
				return json.dumps({
					"success": False,
					"messages": "Fahrzeugklasse nicht vorhanden!"
				})

			anmeldung.data["rennId"] = rennId
			anmeldung.data["fahrzeugId"] = fahrzeugId

			if anmeldung.save():
				return json.dumps({
					"success": True,
					"data": anmeldung.data
				})
			else:
				return json.dumps({
					"success": False,
					"messages": anmeldung.required_fields_empty
				})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})

	def DELETE(self, id):
		super(Anmeldungen, self).check_login()
		if self.user_allowed:
			anmeldung = Anmeldung.find({"id": id})

			if anmeldung is None:
				return json.dumps({
					"success": False,
					"messages": "Fahrzeugklasse nicht vorhanden!"
				})

			anmeldung.delete()

			return json.dumps({
				"success": True
			})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})


# EOF
