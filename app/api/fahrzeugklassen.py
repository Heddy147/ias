import json
from app.abstracts.rest import RestAbstract
from app.abstracts.model import ModelAbstract
from app.models.Fahrzeugklasse import Fahrzeugklasse


class Fahrzeugklassen(RestAbstract):
	def GET(self, id=None):
		super(Fahrzeugklassen, self).check_login()
		if self.user_allowed:
			if id is None:
				fahrzeugklassen = Fahrzeugklasse.find(None, 100000)
			else:
				fahrzeugklassen = Fahrzeugklasse.find({"id": id})

			if fahrzeugklassen is None:
				return json.dumps({
					"success": False,
					"message": "Fahrzeugklasse wurde nicht gefunden!"
				})

			return json.dumps({
				"success": True,
				"fahrzeugklassen": ModelAbstract.get_data_of_objects(fahrzeugklassen)
			})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})

	def POST(
			self,
			bezeichnung,
			beschreibung,
			zeit_in_string
	):
		super(Fahrzeugklassen, self).check_login()
		if self.user_allowed:
			params_zeit = zeit_in_string.split(':')
			if(len(params_zeit) < 3):
				return json.dumps({
					"success": False,
					"message": "Format der Qualifikationszeit ist fehlerhaft"
				})

			zeit_in_millisekunden = (int(params_zeit[0]) * 60 + int(params_zeit[1])) * 1000 + int(params_zeit[2])
			fahrzeugklasse = Fahrzeugklasse()
			fahrzeugklasse.data["bezeichnung"] = bezeichnung
			fahrzeugklasse.data["beschreibung"] = beschreibung
			fahrzeugklasse.data["zeit_in_millisekunden"] = zeit_in_millisekunden
			fahrzeugklasse.data["zeit_in_string"] = zeit_in_string

			if fahrzeugklasse.save():
				return json.dumps({
					"success": True,
					"data": fahrzeugklasse.data
				})
			else:
				return json.dumps({
					"success": False,
					"messages": fahrzeugklasse.required_fields_empty
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
			zeit_in_string
	):
		super(Fahrzeugklassen, self).check_login()
		if self.user_allowed:
			params_zeit = zeit_in_string.split(':')
			if(len(params_zeit) < 3):
				return json.dumps({
					"success": False,
					"message": "Format der Qualifikationszeit ist fehlerhaft"
				})

			zeit_in_millisekunden = (int(params_zeit[0]) * 60 + int(params_zeit[1])) * 1000 + int(params_zeit[2])

			fahrzeugklasse = Fahrzeugklasse.find({"id": id})

			if fahrzeugklasse is None:
				return json.dumps({
					"success": False,
					"messages": "Fahrzeugklasse nicht vorhanden!"
				})

			fahrzeugklasse.data["bezeichnung"] = bezeichnung
			fahrzeugklasse.data["beschreibung"] = beschreibung
			fahrzeugklasse.data["zeit_in_millisekunden"] = zeit_in_millisekunden
			fahrzeugklasse.data["zeit_in_string"] = zeit_in_string

			if fahrzeugklasse.save():
				return json.dumps({
					"success": True,
					"data": fahrzeugklasse.data
				})
			else:
				return json.dumps({
					"success": False,
					"messages": fahrzeugklasse.required_fields_empty
				})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})

	def DELETE(self, id):
		super(Fahrzeugklassen, self).check_login()
		if self.user_allowed:
			fahrzeugklasse = Fahrzeugklasse.find({"id": id})

			if fahrzeugklasse is None:
				return json.dumps({
					"success": False,
					"messages": "Fahrzeugklasse nicht vorhanden!"
				})

			fahrzeugklasse.delete()

			return json.dumps({
				"success": True
			})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})

# EOF
