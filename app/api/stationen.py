import json
from app.abstracts.rest import RestAbstract
from app.abstracts.model import ModelAbstract
from app.models.Station import Station
from app.models.User import User

class Stationen(RestAbstract):
	def GET(self, id=None, rennId=None):
		super(Stationen, self).check_login()
		if self.user_allowed:
			conditions = {}
			if id is not None:
				conditions["id"] = id

			if rennId is not None:
				conditions["rennId"] = rennId

			station = Station.find(conditions, 100000)

			return json.dumps({
				"success": True,
				"fahrzeugklassen": ModelAbstract.get_data_of_objects(station)
			})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})

	def POST(
			self,
			bezeichnung,
			lage,
			beschreibung,
			rennId
	):
		super(Stationen, self).check_login()
		if self.user_allowed:
			station = Station()
			station.data["bezeichnung"] = bezeichnung
			station.data["lage"] = lage
			station.data["beschreibung"] = beschreibung
			station.data["rennId"] = rennId

			if station.save():
				return json.dumps({
					"success": True,
					"data": station.data
				})
			else:
				return json.dumps({
					"success": False,
					"messages": station.required_fields_empty
				})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})

	def PUT(
			self,
			id,
			bezeichnung,
			lage,
			beschreibung,
			rennId
	):
		super(Stationen, self).check_login()
		if self.user_allowed:
			station = Station.find({"id": id})

			if station is None:
				return json.dumps({
					"success": False,
					"messages": "Fahrzeugklasse nicht vorhanden!"
				})

			station.data["bezeichnung"] = bezeichnung
			station.data["lage"] = lage
			station.data["beschreibung"] = beschreibung
			station.data["rennId"] = rennId

			if station.save():
				return json.dumps({
					"success": True,
					"data": station.data
				})
			else:
				return json.dumps({
					"success": False,
					"messages": station.required_fields_empty
				})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})

	def DELETE(self, id):
		super(Stationen, self).check_login()
		if self.user_allowed:
			station = Station.find({"id": id})

			if station is None:
				return json.dumps({
					"success": False,
					"messages": "Fahrzeugklasse nicht vorhanden!"
				})

			station.delete()

			return json.dumps({
				"success": True
			})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})


# EOF
