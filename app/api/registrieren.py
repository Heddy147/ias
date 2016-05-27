import json
from app.abstracts.rest import RestAbstract
from app.models.User import User


class Registrieren(RestAbstract):

	def POST(self, benutzername, passwort):
		super(Registrieren, self).check_login()
		if self.user_allowed:
			user = User.find({"benutzername": benutzername})

			if user is not None:
				return json.dumps({
					"success": False,
					"message": "Benutzer ist schon vorhanden!"
				})
			else:
				user = User()
				user.data["benutzername"] = benutzername
				user.data["passwort"] = passwort
				user.data["rolle"] = "besitzer"
				user.save()

				return json.dumps({
					"success": True
				})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})
# EOF
