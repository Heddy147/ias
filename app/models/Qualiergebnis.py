import cherrypy
from app.abstracts.model import ModelAbstract

class Qualiergebnis(ModelAbstract):
	data_file_name = 'qualiergebnisse'
	required_fields = ['id', 'zeit', 'status', 'rennId', 'fahrzeugId', 'platzierung']

# EOF
