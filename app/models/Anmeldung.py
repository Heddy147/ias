import cherrypy
from app.abstracts.model import ModelAbstract
from app.models.Person import Person
from app.models.Fahrzeug import Fahrzeug
from app.models.Fahrzeugklasse import Fahrzeugklasse

class Anmeldung(ModelAbstract):
	data_file_name = 'anmeldungen'
	required_fields = ['id', 'fahrzeugId', 'rennId', 'benutzerId']
	real_fields = ['id', 'fahrzeugId', 'rennId', 'benutzerId']

	def __init__(self):
		super(Anmeldung, self).__init__()
		self.data["quali_platzierung"] = 999

	def after_find(self):
		fahrzeug = Fahrzeug.find({"id": self.data["fahrzeugId"]})

		if fahrzeug is not None:
			self.data["fahrzeug"] = fahrzeug.data

			fahrer = Person.find({"id": self.data["fahrzeug"]["fahrerId"]})
			beifahrer = Person.find({"id": self.data["fahrzeug"]["beifahrerId"]})
			mechaniker = Person.find({"id": self.data["fahrzeug"]["mechanikerId"]})

			if fahrer is not None:
				self.data["fahrer"] = fahrer.data

			if beifahrer is not None:
				self.data["beifahrer"] = beifahrer.data

			if mechaniker is not None:
				self.data["mechaniker"] = mechaniker.data

# EOF
