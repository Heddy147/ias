import cherrypy
from app.abstracts.model import ModelAbstract

class Rennen(ModelAbstract):
	data_file_name = 'rennen'
	required_fields = ['id', 'bezeichnung', 'beschreibung', 'datum', 'leitungId', 'beendet']

# EOF
