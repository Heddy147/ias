import cherrypy
from app.abstracts.model import ModelAbstract
from app.models.User import User

class Rennen(ModelAbstract):
	data_file_name = 'rennen'
	required_fields = ['id', 'bezeichnung', 'beschreibung', 'datum', 'leitungId', 'beendet']

	def after_find(self):
		leiter = User.find({"id": self.data["leitungId"]})

		if leiter is not None:
			self.data["leiter"] = leiter.data

# EOF
