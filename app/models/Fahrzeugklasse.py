import cherrypy
from app.abstracts.model import ModelAbstract

class Fahrzeugklasse(ModelAbstract):
	data_file_name = 'fahrzeugklassen'
	required_fields = ['id', 'beschreibung', 'bezeichnung', 'zeit_in_millisekunden', 'zeit_in_string']

# EOF
