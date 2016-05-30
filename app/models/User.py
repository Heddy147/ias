import cherrypy
import time
from app.abstracts.model import ModelAbstract

class User(ModelAbstract):
	logged_in_user = None
	data_file_name = 'user'

	@staticmethod
	def user_logged_in():
		cookie = cherrypy.request.cookie
		if "user" in cookie:
			username = cherrypy.request.cookie["user"].value
			user = User.find({"benutzername": username})
			if user is not None:
				User.logged_in_user = user
			else:
				User.logged_in_user = None

		else:
			User.logged_in_user = None

	@staticmethod
	def login_user(username):
		cherrypy.response.cookie["user"] = username
		cherrypy.response.cookie['user']['path'] = '/'
		cherrypy.response.cookie['user']['max-age'] = time.time() + 3600
		cherrypy.response.cookie['user']['version'] = 1
		user = User.find({"benutzername": username})
		if user is not None:
			User.logged_in_user = user
		else:
			User.logged_in_user = None

	@staticmethod
	def logout():
		cookie = cherrypy.request.cookie
		if "user" in cookie:
			cherrypy.response.cookie["user"] = ''
			cherrypy.response.cookie["user"]['expires'] = 0
			cherrypy.response.cookie['user']['path'] = '/'
			cherrypy.response.cookie['user']['max-age'] = -1
			cherrypy.response.cookie['user']['version'] = 1

			User.logged_in_user = None

# EOF
