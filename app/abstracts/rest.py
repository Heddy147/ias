import cherrypy
import inspect
from app.models.User import User


class RestAbstract:
	exposed = True
	data_file_name = 'index'

	executed_class = None
	executed_method = None

	allowed_actions_gast = [
		'Login.PUT',
		'Registrieren.POST'
	]

	allowed_actions_besitzer = [
		'Fahrzeuge.GET',
		'Fahrzeuge.POST',
		'Fahrzeuge.PUT',
		'Fahrzeuge.DELETE',
		'Rennen.GET',
		'Rennanmeldung.GET',
		'Rennanmeldung.POST',
		'Rennanmeldung.DELETE',
		'Personen.GET'
	]

	user_allowed = True

	def __init__(self):
		pass

	def check_login(self):
		User.user_logged_in()
		RestAbstract.executed_class = self.__class__.__name__
		RestAbstract.executed_method = inspect.stack()[1][3]

		if User.logged_in_user is None:
			allowed_actions = self.allowed_actions_gast
		elif User.logged_in_user.data["rolle"] == "besitzer":
			allowed_actions = self.allowed_actions_besitzer
		else:
			allowed_actions = None

		if allowed_actions is not None:
			called_action = RestAbstract.executed_class + '.' + RestAbstract.executed_method
			if called_action not in allowed_actions:
				self.user_allowed = False

		self.user_allowed = True
# EOF
