import json


class Ext:

	def __init__(self, ownerComp):
		self.env_in = op("env_in")
		self.env = op("data")
		self.ownerComp = ownerComp
		# initial load of the input file
		Ext.processFile(op("env_in"))

	def Get(self, key):
		"""
		key: name of env variable to get. Should be of type string
		returns: td.Cell for the variable
		"""
		valid = self.Exists(key)
		if not valid:
			raise ValueError("Failed to get value, key '{}' does not exist".format(key))
			return None
		return self.env[str(key), 1]

	def Exists(self, key):
		"""
		return boolean if this key is already present
		"""
		return self.env[str(key), 0] is not None

	def CreateCallbacks(self):
		print(self.ownerComp)
		new_callback_dat = self.ownerComp.parent().copy(op("default_callbacks"), name = f"{self.ownerComp.name}_callbacks")
		new_callback_dat.nodeX = self.ownerComp.nodeX
		new_callback_dat.nodeY = self.ownerComp.nodeY - 150
		new_callback_dat.dock = self.ownerComp
		self.ownerComp.par.Callbackdat = new_callback_dat

	@staticmethod
	def flatten(d, parent_key='', sep='_'):
		"""
		Helper to flatten a json object into a list
		"""
		items = []
		for k, v in d.items():
			new_key = parent_key + sep + k if parent_key else k
			if isinstance(v, collections.MutableMapping):
				items.extend(Ext.flatten(v, new_key, sep=sep).items())
			else:
				items.append((new_key, v))
		return dict(items)

	@staticmethod
	def processFile(dat):
		"""
		Static method to determine if the input file is json or .env and assign the 
		correct field values
		"""
		is_json = str(parent().par.Envfile).endswith(".json")
		is_json_int = int(is_json)
		if is_json:
			print("process as JSON")
			env_out = op("env_json_edit")
			env_out.clear()
			try:
				data = json.loads(dat.text)
				flattened = Ext.flatten(data)
				for key, val in flattened.items():
					env_out.appendRow([key.upper(), val])
			except json.decoder.JSONDecodeError as err:
				print("Invalid Json")
				raise err
		else:
			print("process as .env file")
			env_out = op("env_env_edit")
			env_out.clear()
			lines = dat.text.split('\n')
			for line in lines:
				parts = line.split(str(parent().par.Delimiter), 1)
				if parts != ['']:
					env_out.appendRow(parts)

		
		op("switch1").par.index = is_json_int
		print("reloaded environment file")