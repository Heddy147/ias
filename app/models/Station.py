import cherrypy
from app.abstracts.model import ModelAbstract

class Station(ModelAbstract):
	data_file_name = 'stationen'
	required_fields = ['id', 'bezeichnung', 'lage', 'rennId']

# EOF
