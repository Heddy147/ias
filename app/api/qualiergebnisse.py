import json
from app.abstracts.rest import RestAbstract
from app.models.Qualiergebnis import Qualiergebnis
from app.models.Fahrzeug import Fahrzeug
from app.models.Rennen import Rennen
from app.models.Anmeldung import Anmeldung
from app.models.Fahrzeugklasse import Fahrzeugklasse


class Qualiergebnisse(RestAbstract):

	def POST(
			self,
			**kw
	):
		super(Qualiergebnisse, self).check_login()
		if self.user_allowed:
			if "rennId" not in kw:
				return json.dumps({
					"success": False,
					"message": "Rennen nicht vorhanden!"
				})

			rennId = kw["rennId"]

			rennen = Rennen.find({"id": rennId})

			if rennen is None:
				return json.dumps({
					"success": False,
					"message": "Rennen nicht vorhanden!"
				})

			real_erg = []
			not_qualified_erg = []

			anmeldungen = Anmeldung.find({"rennId": rennId}, 100000)

			for anmeldung in anmeldungen:
				status_key = "ergebnisse[" + anmeldung.data["id"] + "][status]"
				zeit_in_string_key = "ergebnisse[" + anmeldung.data["id"] + "][zeit_in_string]"
				zeit_in_millisekunden_key = "ergebnisse[" + anmeldung.data["id"] + "][zeit_in_millisekunden]"

				if status_key not in kw or zeit_in_string_key not in kw or zeit_in_millisekunden_key not in kw:
					return json.dumps({
						"success": False,
						"message": "Jedes Fahrzeug muss eine Zeit erhalten oder disqualifiziert werden!"
					})

				fahrzeug = Fahrzeug.find({"id": anmeldung.data["fahrzeugId"]})

				fahrzeugklasse = Fahrzeugklasse.find({"id": fahrzeug.data["typ"]})
				if fahrzeugklasse is None:
					return json.dumps({
						"success": False,
						"message": "Eines der Fahrzeuge ist keiner Klasse angehörig und kann somit nicht am Rennen teilnehmen!"
					})

				status = kw[status_key]
				if int(status) is not 2:
					if int(kw[zeit_in_millisekunden_key]) <= int(fahrzeugklasse.data["zeit_in_millisekunden"]):
						status = 1
					else:
						status = 0

				if int(status) is not 1:
					not_qualified_erg.append({
						"fahrzeugId": anmeldung.data["fahrzeugId"],
						"status": status
					})
				else:
					real_erg.append({
						"fahrzeugId": anmeldung.data["fahrzeugId"],
						"zeit_in_string": kw[zeit_in_string_key],
						"zeit_in_millisekunden": kw[zeit_in_millisekunden_key],
						"status": status,
						"anmeldeId": anmeldung.data["id"]
					})

			sorted_erg = sorted(real_erg, key=self.sort_ergebnisse)
			platz = 1
			for ergebnis in sorted_erg:
				anmeldung = Anmeldung.find({"id": ergebnis["anmeldeId"]})
				anmeldung.data["quali_platzierung"] = platz
				anmeldung.save()

				qualiergebnis = Qualiergebnis()
				qualiergebnis.data["zeit"] = ergebnis["zeit_in_string"]
				qualiergebnis.data["status"] = 1
				qualiergebnis.data["rennId"] = rennId
				qualiergebnis.data["fahrzeugId"] = ergebnis["fahrzeugId"]
				qualiergebnis.data["platzierung"] = platz
				qualiergebnis.save()
				platz += 1

			for nq_ergebnis in not_qualified_erg:
				qualiergebnis = Qualiergebnis()
				qualiergebnis.data["zeit"] = "60:60:999"
				qualiergebnis.data["status"] = nq_ergebnis["status"]
				qualiergebnis.data["rennId"] = rennId
				qualiergebnis.data["fahrzeugId"] = nq_ergebnis["fahrzeugId"]
				qualiergebnis.data["platzierung"] = 999
				qualiergebnis.save()

			return json.dumps({
				"success": True
			})

		return json.dumps({
			"success": False,
			"message": "Aktion nicht erlaubt!"
		})

	def sort_ergebnisse(self, item):
		return item["zeit_in_millisekunden"]
# EOF
