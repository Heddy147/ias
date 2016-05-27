import cherrypy
import sys
import json
from app.models.User import User


class App:
	def __init__(self):
		User.user_logged_in()

	@cherrypy.expose
	def index(self):
		if User.logged_in_user is not None:
			if User.logged_in_user.data["rolle"] == "leitung":
				file_name = "leitung"
			else:
				file_name = "besitzer"
		else:
			file_name = "login"

		with open('content/' + file_name + '.html', 'r') as f:
			return f.read()

# EOF
