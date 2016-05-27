import cherrypy
from app.abstracts.model import ModelAbstract

class Fahrzeug(ModelAbstract):
	data_file_name = 'fahrzeuge'
	required_fields = ['id', 'marke', 'typ', 'baujahr', 'hubraum', 'leistung', 'kennzeichen', 'fahrerId', 'beifahrerId', 'mechanikerId']

# EOF
