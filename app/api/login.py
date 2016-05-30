import cherrypy
import json
from app.abstracts.rest import RestAbstract
from app.models.User import User


class Login(RestAbstract):

	exposed = True

	def PUT(self, benutzername, passwort):
		super(Login, self).check_login()
		if self.user_allowed:
			user = User.find({"benutzername": benutzername, "passwort": passwort})
			if user is not None:
				User.login_user(benutzername)
				return json.dumps({'success': True, 'user': User.logged_in_user.data})

			return json.dumps({'success': False, 'message': 'Benutzername oder Passwort falsch!'})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})

	def DELETE(self):
		super(Login, self).check_login()
		if self.user_allowed:
			if User.logged_in_user is not None:
				User.logout()
				return json.dumps({"success": True})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})

# EOF
