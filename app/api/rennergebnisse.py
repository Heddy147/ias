import json
from app.abstracts.rest import RestAbstract
from app.models.Rennergebnis import Rennergebnis
from app.models.Fahrzeug import Fahrzeug
from app.models.Rennen import Rennen
from app.models.Station import Station
from app.models.Anmeldung import Anmeldung
from app.models.Fahrzeugklasse import Fahrzeugklasse


class Rennergebnisse(RestAbstract):

	def POST(
			self,
			**kw
	):
		super(Rennergebnisse, self).check_login()
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

			if "ergebnisse" not in kw:
				return json.dumps({
					"success": False,
					"message": "Irgendetwas ist schief gelaufen. Versuchen Sie es erneut."
				})

			ergebnisse = kw["ergebnisse"]

			stationen = Station.find({"rennId": rennId}, 100000)
			anmeldungen = Anmeldung.find({"rennId": rennId}, 100000)
			ergebnisse_json = json.loads(ergebnisse)

			real_erg = []
			renn_erg_asso = {}
			renn_erg = []
			renn_erg_not_correct = []
			disquali_erg = []

			for anmeldung in anmeldungen:
				if anmeldung.data["id"] not in ergebnisse_json:
					return json.dumps({
						"success": False,
						"message": "Jedes Fahrzeug muss Zeiten erhalten oder disqualifiziert werden! 1"
					})

				fahrzeug = Fahrzeug.find({"id": anmeldung.data["fahrzeugId"]})

				fahrzeugklasse = Fahrzeugklasse.find({"id": fahrzeug.data["typ"]})
				if fahrzeugklasse is None:
					return json.dumps({
						"success": False,
						"message": "Eines der Fahrzeuge ist keiner Klasse angehörig und kann somit nicht am Rennen teilnehmen!"
					})

				if int(ergebnisse_json[anmeldung.data["id"]]["disquali"]) == 0:
					for station in stationen:
						if station.data["id"] not in ergebnisse_json[anmeldung.data["id"]]["stationsErgebnisse"]:
							return json.dumps({
								"success": False,
								"message": "Jedes Fahrzeug muss Zeiten erhalten oder disqualifiziert werden! 2"
							})

						real_erg.append({
							"fahrzeugId": anmeldung.data["fahrzeugId"],
							"zeit_in_string": ergebnisse_json[anmeldung.data["id"]]["stationsErgebnisse"][station.data["id"]]["zeit_in_string"],
							"zeit_in_millisekunden": ergebnisse_json[anmeldung.data["id"]]["stationsErgebnisse"][station.data["id"]]["zeit_in_millisekunden"],
							"stationId": station.data["id"]
						})

						if anmeldung.data["id"] not in renn_erg_asso:
							renn_erg_asso[anmeldung.data["id"]] = {
								"zeit_in_millisekunden": int(ergebnisse_json[anmeldung.data["id"]]["stationsErgebnisse"][station.data["id"]]["zeit_in_millisekunden"]),
								"fahrzeugId": anmeldung.data["fahrzeugId"]
							}
						else:
							renn_erg_asso[anmeldung.data["id"]]["zeit_in_millisekunden"] += int(ergebnisse_json[anmeldung.data["id"]]["stationsErgebnisse"][station.data["id"]]["zeit_in_millisekunden"])
					renn_erg_asso[anmeldung.data["id"]]["stationen_ok"] = int(ergebnisse_json[anmeldung.data["id"]]["stationen_ok"])
				else:
					disquali_erg.append({
						"fahrzeugId": anmeldung.data["fahrzeugId"]
					})
					break

			for fId in renn_erg_asso:
				if int(renn_erg_asso[fId]["stationen_ok"]) is 0:
					renn_erg_not_correct.append({
						"fahrzeugId": renn_erg_asso[fId]["fahrzeugId"]
					})
				else:
					minuten = int(renn_erg_asso[fId]["zeit_in_millisekunden"] / 60000)
					rest = renn_erg_asso[fId]["zeit_in_millisekunden"] - (minuten * 60000)

					if rest > 9999:
						sekunden = str(rest)[:2]
					else:
						sekunden = str(rest)[:1]

					millisekunden = str(rest)[-3:]
					minuten = str(minuten)

					if len(minuten) < 2:
						minuten = "0" + minuten

					if len(sekunden) < 2:
						sekunden = "0" + sekunden

					renn_erg.append({
						"fahrzeugId": renn_erg_asso[fId]["fahrzeugId"],
						"zeit_in_string": str(minuten) + ":" + str(sekunden) + ":" + str(millisekunden),
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

			rennen.data["beendet"] = 1
			rennen.save()

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
