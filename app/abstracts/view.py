import cherrypy
from app.models.User import User


class ViewAbstract:
	data_file_name = 'index'

	executed_class = None

	def __init__(self):
		User.user_logged_in()
		ViewAbstract.executed_class = self.__class__.__name__

	@cherrypy.expose
	def index(self):
		with open('content/' + self.data_file_name + '.html', 'r') as f:
			return f.read()

# EOF
