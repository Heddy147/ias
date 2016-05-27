import cherrypy
from app.abstracts.model import ModelAbstract

class Stationsergebnis(ModelAbstract):
	data_file_name = 'stattionsergebnisse'
	required_fields = ['id', 'zeit', 'stationsId', 'fahrzeugId']

# EOF
