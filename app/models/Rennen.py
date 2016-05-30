import cherrypy
from app.abstracts.model import ModelAbstract
from app.models.User import User
from app.models.Qualiergebnis import Qualiergebnis
from app.models.Rennergebnis import Rennergebnis

class Rennen(ModelAbstract):
	data_file_name = 'rennen'
	required_fields = ['id', 'bezeichnung', 'beschreibung', 'datum', 'leitungId', 'beendet']
	real_fields = ['id', 'bezeichnung', 'beschreibung', 'datum', 'leitungId', 'beendet']

	def __init__(self):
		super(Rennen, self).__init__()
		self.data["beendet"] = 0

	def after_find(self):
		leiter = User.find({"id": self.data["leitungId"]})

		if leiter is not None:
			self.data["leiter"] = leiter.data

		qualiergebnisse = Qualiergebnis.find({"rennId": self.data["id"]})
		if qualiergebnisse is not None:
			self.data["quali_eingetragen"] = True
		else:
			self.data["quali_eingetragen"] = False

		rennergebnisse = Rennergebnis.find({"rennId": self.data["id"]})
		if rennergebnisse is not None:
			self.data["rennen_eingetragen"] = True
		else:
			self.data["rennen_eingetragen"] = False

# EOF
