import cherrypy
from app.abstracts.model import ModelAbstract

class Rennergebnis(ModelAbstract):
	data_file_name = 'rennergebnisse'
	required_fields = ['id', 'zeit', 'fahrzeugId', 'rennId', 'status', 'platzierung', 'stationen_ok']

# EOF
