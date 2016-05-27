import json
from app.abstracts.rest import RestAbstract
from app.abstracts.model import ModelAbstract
from app.models.Person import Person
from app.models.User import User

class Personen(RestAbstract):
	def GET(self, id=None):
		super(Personen, self).check_login()
		if self.user_allowed:
			if id is None:
				if User.logged_in_user.data["rolle"] == "leitung":
					person = Person.find(None, 100000)
				else:
					person = Person.find({"besitzerId": User.logged_in_user.data["id"]}, 100000)
			else:
				if User.logged_in_user.data["rolle"] == "leitung":
					person = Person.find({"id": id})
				else:
					person = Person.find({"id": id, "besitzerId": User.logged_in_user.data["id"]})

			return json.dumps({
				"success": True,
				"personen": ModelAbstract.get_data_of_objects(person)
			})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})

	def POST(
			self,
			vorname,
			nachname,
			fuehrerschein
	):
		super(Personen, self).check_login()
		if self.user_allowed:
			person = Person()
			person.data["besitzerId"] = User.logged_in_user.data["id"]
			person.data["vorname"] = vorname
			person.data["nachname"] = nachname
			person.data["fuehrerschein"] = fuehrerschein

			if person.save():
				return json.dumps({
					"success": True,
					"data": person.data
				})
			else:
				return json.dumps({
					"success": False,
					"messages": person.required_fields_empty
				})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})

	def PUT(
			self,
			id,
			vorname,
			nachname,
			fuehrerschein
	):
		super(Personen, self).check_login()
		if self.user_allowed:
			person = Person.find({"id": id})

			if person is None:
				return json.dumps({
					"success": False,
					"messages": "Fahrzeugklasse nicht vorhanden!"
				})

			person.data["vorname"] = vorname
			person.data["nachname"] = nachname
			person.data["fuehrerschein"] = fuehrerschein

			if person.save():
				return json.dumps({
					"success": True,
					"data": person.data
				})
			else:
				return json.dumps({
					"success": False,
					"messages": person.required_fields_empty
				})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})

	def DELETE(self, id):
		super(Personen, self).check_login()
		if self.user_allowed:
			person = Person.find({"id": id})

			if person is None:
				return json.dumps({
					"success": False,
					"messages": "Fahrzeugklasse nicht vorhanden!"
				})

			person.delete()

			return json.dumps({
				"success": True
			})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})


# EOF
