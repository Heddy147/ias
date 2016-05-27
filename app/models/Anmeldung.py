import cherrypy
from app.abstracts.model import ModelAbstract

class Anmeldung(ModelAbstract):
	data_file_name = 'anmeldungen'
	required_fields = ['id', 'fahrzeugeId', 'rennId']

	def __init__(self):
		super(Anmeldung, self).__init__()
		self.data["quali_platzierung"] = 999

# EOF
