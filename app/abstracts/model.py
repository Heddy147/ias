import cherrypy
import json

class ModelAbstract:
	data_file_name = ''
	data = {"id": 0}

	required_fields = []
	required_fields_empty = []
	real_fields = []

	def __init__(self):
		self.data["id"] = 0
		self.required_fields_empty = []

	@classmethod
	def find(cls, conditions=None, count=1):
		all_data = cls.load_all()
		counted = 0
		found_data = []

		if conditions is None:
			for ad in all_data:
				model = cls()
				model.data = all_data[ad]
				model.after_find()
				if counted < count:
					found_data.append(model)
				else:
					return found_data
			return found_data

		for ad in all_data:
			is_okay = True

			for c in conditions:
				condition = conditions[c]
				value = all_data[ad][c]
				if type(value) is int:
					condition = int(condition)

				if value != condition:
					is_okay = False
					break

			if is_okay:
				model = cls()
				model.data = all_data[ad]
				model.after_find()
				if int(count) is 1:
					return model

				if counted < count:
					found_data.append(model)
				else:
					return found_data

				counted += 1

		if int(count) == 1:
			return None

		return found_data

	def save(self):
		for r in self.required_fields:
			if r not in self.data or self.data[r] == "":
				self.required_fields_empty.append(r)

		if len(self.required_fields_empty) > 0:
			return False

		all_data = self.load_all()

		if self.data["id"] == 0:
			new_id = ModelAbstract.get_last_id(all_data)
			self.data["id"] = str(new_id)

		real_data = {}
		if len(self.real_fields) > 0:
			for field in self.real_fields:
				real_data[field] = self.data[field]
		else:
			real_data = self.data

		all_data[str(self.data["id"])] = real_data

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

		if str(self.data["id"]) in all_data:
			del all_data[str(self.data["id"])]

		self.save_all(all_data)

		return True

	def after_find(self):
		pass

	@staticmethod
	def get_data_of_objects(data):
		if type(data) is list:
			list_data = []
			for d in data:
				list_data.append(d.data)
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
