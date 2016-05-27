import json

def sort_erg(item):
	return item["zeit"]


ergebnisse = [
	{
		"id": 1,
		"zeit": "561087"
	}, {
		"id": 2,
		"zeit": "531874"
	}, {
		"id": 3,
		"zeit": "561187"
	}, {
		"id": 4,
		"zeit": "547954"
	}
]

sorted_erg = sorted(ergebnisse, key=sort_erg)

print(sorted_erg)