import cherrypy
from app.abstracts.model import ModelAbstract

class Person(ModelAbstract):
	data_file_name = 'personen'
	required_fields = ['id', 'vorname', 'nachname', 'besitzerId']

# EOF
