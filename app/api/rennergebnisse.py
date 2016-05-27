import json
from app.abstracts.rest import RestAbstract
from app.models.Rennergebnis import Rennergebnis
from app.models.Fahrzeug import Fahrzeug
from app.models.Rennen import Rennen
from app.models.Station import Station
from app.models.Anmeldung import Anmeldung
from app.models.Fahrzeugklasse import Fahrzeugklasse


class Registrieren(RestAbstract):

	def POST(
			self,
			ergebnisse,
			rennId
	):
		super(Registrieren, self).check_login()
		if self.user_allowed:
			rennen = Rennen.find({"id": rennId})

			if rennen is None:
				return json.dumps({
					"success": False,
					"message": "Rennen nicht vorhanden!"
				})

			stationen = Station.find({"rennId": rennId}, 100000)
			anmeldungen = Anmeldung.find({"rennId": rennId}, 100000)
			ergebnisse_json = json.loads(ergebnisse)

			real_erg = []
			renn_erg_asso = {}
			renn_erg = []
			renn_erg_not_correct = []
			disquali_erg = []

			for anmeldung in anmeldungen:
				if anmeldung.data["fahrzeugId"] not in ergebnisse_json:
					return json.dumps({
						"success": False,
						"message": "Jedes Fahrzeug muss Zeiten erhalten oder disqualifiziert werden!"
					})

				fahrzeug = Fahrzeug.find({"id": anmeldung.data["fahrzeugId"]})

				fahrzeugklasse = Fahrzeugklasse.find({"id": fahrzeug.data["typ"]})
				if fahrzeugklasse is None:
					return json.dumps({
						"success": False,
						"message": "Eines der Fahrzeuge ist keiner Klasse angehörig und kann somit nicht am Rennen teilnehmen!"
					})

				for station in stationen:
					if int(ergebnisse_json[anmeldung.data["fahrzeugId"]]["disquali"]) == 0:
						if station.data["id"] not in ergebnisse_json[anmeldung.data["fahrzeugId"]]["stationsErgebnisse"]:
							return json.dumps({
								"success": False,
								"message": "Jedes Fahrzeug muss Zeiten erhalten oder disqualifiziert werden!"
							})

						real_erg.append({
							"fahrzeugId": anmeldung.data["fahrzeugId"],
							"zeit_in_string": ergebnisse_json[anmeldung.data["fahrzeugId"]]["zeit_in_string"],
							"zeit_in_millisekunden": ergebnisse_json[anmeldung.data["fahrzeugId"]]["zeit_in_millisekunden"],
							"stationId": station.data["id"]
						})

						if anmeldung.data["fahrzeugId"] not in renn_erg_asso:
							renn_erg_asso[anmeldung.data["fahrzeugId"]] = {
								"zeit_in_millisekunden": ergebnisse_json[anmeldung.data["fahrzeugId"]]["zeit_in_millisekunden"]
							}
						else:
							renn_erg_asso[anmeldung.data["fahrzeugId"]]["zeit_in_millisekunden"] += ergebnisse_json[anmeldung.data["fahrzeugId"]]["zeit_in_millisekunden"]
					else:
						disquali_erg.append({
							"fahrzeugId": anmeldung.data["fahrzeugId"]
						})
						break

			for fId in renn_erg_asso:
				if int(ergebnisse_json[anmeldung.data["fahrzeugId"]]["stationen_ok"]) is 0:
					renn_erg_not_correct.append({
						"fahrzeugId": fId
					})
				else:
					minuten = renn_erg_asso[fId]["zeit_in_millisekunden"] / 60
					rest = renn_erg_asso[fId]["zeit_in_millisekunden"] - minuten
					if rest > 9999:
						sekunden = rest[:2]
					else:
						sekunden = rest[:1]

					millisekunden = rest[-3:]
					renn_erg.append({
						"fahrzeugId": fId,
						"zeit_in_string": minuten + ":" + sekunden + ":" + millisekunden,
						"zeit_in_millisekunden": renn_erg_asso[fId]["zeit_in_millisekunden"]
					})

			sorted_erg = sorted(renn_erg, key=self.sort_ergebnisse)
			platz = 1
			for ergebnis in sorted_erg:
				rennergebnis = Rennergebnis()
				rennergebnis.data["zeit"] = ergebnis["zeit_in_string"]
				rennergebnis.data["fahrzeugId"] = ergebnis["fahrzeugId"]
				rennergebnis.data["rennId"] = rennId
				rennergebnis.data["status"] = 1
				rennergebnis.data["platzierung"] = platz
				rennergebnis.data["stationen_ok"] = 1
				rennergebnis.save()
				platz += 1

			for ergebnis in disquali_erg:
				rennergebnis = Rennergebnis()
				rennergebnis.data["zeit"] = "60:60:999"
				rennergebnis.data["fahrzeugId"] = ergebnis["fahrzeugId"]
				rennergebnis.data["rennId"] = rennId
				rennergebnis.data["status"] = 0
				rennergebnis.data["platzierung"] = 999
				rennergebnis.data["stationen_ok"] = 1
				rennergebnis.save()

			for ergebnis in renn_erg_not_correct:
				rennergebnis = Rennergebnis()
				rennergebnis.data["zeit"] = "60:60:999"
				rennergebnis.data["fahrzeugId"] = ergebnis["fahrzeugId"]
				rennergebnis.data["rennId"] = rennId
				rennergebnis.data["status"] = 1
				rennergebnis.data["platzierung"] = 999
				rennergebnis.data["stationen_ok"] = 0
				rennergebnis.save()

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
