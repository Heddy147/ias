import cherrypy
import json


class ModelAbstract:
	data_file_name = ''
	data = {"id": 0}

	required_fields = []
	required_fields_empty = []

	def __init__(self):
		self.data["id"] = 0

	@classmethod
	def find(cls, conditions=None, count=1):
		all_data = cls.load_all()
		counted = 0
		found_data = []

		if conditions is None:
			for ad in all_data:
				user = cls()
				user.data = all_data[ad]
				if counted < count:
					found_data.append(user)
				else:
					return found_data
			return found_data

		for ad in all_data:
			is_okay = True

			for c in conditions:
				if all_data[ad][c] != conditions[c]:
					is_okay = False
					break

			if is_okay:
				user = cls()
				user.data = all_data[ad]
				if int(count) is 1:
					return user

				if counted < count:
					found_data.append(user)
				else:
					return found_data

				counted += 1

		if int(count) is 1:
			return None

		return found_data

	def save(self):
		for r in self.required_fields:
			if r not in self.data or self.data[r] == "":
				self.required_fields_empty.append(self.required_fields[r])

		if len(self.required_fields_empty) > 0:
			return False

		all_data = self.load_all()

		if self.data["id"] == 0:
			new_id = ModelAbstract.get_last_id(all_data)
			self.data["id"] = new_id

		all_data[self.data["id"]] = self.data

		self.save_all(all_data)

		return True

	@classmethod
	def load_all(cls):
		file = open("data/" + cls.data_file_name + ".json", "r")
		data = json.load(file)
		return data

	def save_all(self, data):
		file = open("data/" + self.data_file_name + ".json", "w")
		json.dump(data, file)

	def delete(self):
		all_data = self.load_all()

		if self.data["id"] in all_data:
			del all_data[self.data["id"]]

		self.save_all(all_data)

		return True

	@staticmethod
	def get_data_of_objects(data):
		if type(data) is list:
			list_data = []
			for d in data:
				list_data.append(data[d].data)
			return list_data

		return data.data

	@staticmethod
	def get_last_id(checking_data):
		last_id = 0

		for id_of_data in checking_data:
			if int(last_id) < int(id_of_data):
				last_id = int(id_of_data)

		return last_id + 1
# EOF
