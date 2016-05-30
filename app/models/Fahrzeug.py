import cherrypy
from app.abstracts.model import ModelAbstract
from app.models.Fahrzeugklasse import Fahrzeugklasse

class Fahrzeug(ModelAbstract):
	data_file_name = 'fahrzeuge'
	required_fields = ['id', 'benutzerId', 'marke', 'typ', 'baujahr', 'hubraum', 'leistung', 'kennzeichen', 'fahrerId', 'beifahrerId', 'mechanikerId']
	real_fields = ['id', 'benutzerId', 'marke', 'typ', 'baujahr', 'hubraum', 'leistung', 'kennzeichen', 'fahrerId', 'beifahrerId', 'mechanikerId', 'beschreibung']

	def after_find(self):
		fahrzeugklasse = Fahrzeugklasse.find({"id": self.data["typ"]})

		if fahrzeugklasse is not None:
			self.data["fahrzeugklasse"] = fahrzeugklasse.data
# EOF
