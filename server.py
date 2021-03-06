# coding: utf-8
import os
import cherrypy
from app import application, template
from app.api import anmeldungen, fahrzeuge, fahrzeugklassen, login, personen, qualiergebnisse, registrieren, rennen, rennergebnisse, stationen

def validate_password(realm, username, password):
	users = application.db.load_user()
	if username in users and users[username]["password"] == password:
		application.user = username
		return True
	return False


def main():
	# --------------------------------------
	# Get current directory
	try:
		current_dir = os.path.dirname(os.path.abspath(__file__))
	except:
		current_dir = os.path.dirname(os.path.abspath(sys.executable))

	cherrypy.Application.currentDir = current_dir
#
	# disable autoreload and timeout_monitor
	cherrypy.engine.autoreload.unsubscribe()
	cherrypy.engine.timeout_monitor.unsubscribe()

	cherrypy.tree.mount(application.App(), '/', {"/": {}})

	css_handler = cherrypy.tools.staticdir.handler(section="/", dir='/content/css')
	cherrypy.tree.mount(css_handler, '/css', {
		'/': {
			'tools.staticdir.root': current_dir,
			'tools.staticdir.on': True,
			'tools.staticdir.dir': 'content/css'
		}
	})
	js_handler = cherrypy.tools.staticdir.handler(section="/", dir='/content/js')
	cherrypy.tree.mount(js_handler, '/js', {
		'/': {
			'tools.staticdir.root': current_dir,
			'tools.staticdir.on': True,
			'tools.staticdir.dir': 'content/js'
		}
	})

	cherrypy.tree.mount(anmeldungen.Anmeldungen(), '/api/anmeldungen', {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}})
	cherrypy.tree.mount(fahrzeuge.Fahrzeuge(), '/api/fahrzeuge', {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}})
	cherrypy.tree.mount(fahrzeugklassen.Fahrzeugklassen(), '/api/fahrzeugklassen', {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}})
	cherrypy.tree.mount(login.Login(), '/api/login', {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}})
	cherrypy.tree.mount(personen.Personen(), '/api/personen', {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}})
	cherrypy.tree.mount(qualiergebnisse.Qualiergebnisse(), '/api/qualiergebnisse', {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}})
	cherrypy.tree.mount(registrieren.Registrieren(), '/api/registrieren', {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}})
	cherrypy.tree.mount(rennen.Rennen(), '/api/rennen', {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}})
	cherrypy.tree.mount(rennergebnisse.Rennergebnisse(), '/api/rennergebnisse', {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}})
	cherrypy.tree.mount(stationen.Stationen(), '/api/stationen', {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}})

	cherrypy.tree.mount(template.Template(), '/template', {
		'/': {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher()
		}
	})

	# Start server
	cherrypy.engine.start()
	cherrypy.engine.block()

# --------------------------------------
if __name__ == '__main__':
	# --------------------------------------
	main()
# EOF