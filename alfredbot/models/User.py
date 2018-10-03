import pandas as pd

from .AbstractPandas import AbstractPandas
from alfredbot.exceptions.UserNotFoundException import UserNotFoundException

#user model
class User(AbstractPandas):

	def __init__(self,d={}):
		super()
		self.update(d)
		file = "data/users.csv"
		super().load_dataframe(file)

	def reload(self):
		super().reload()
		if "first_name" not in self:
			raise UserNotFoundException("User {} not found".format(self.id))

	def remove(self):
		id = self["id"]
		super().remove()
		for day in ["sunday","monday","tuesday","wednesday","thursday","friday","saturday"]:
			locations = pd.read_csv("data/{}-locations.csv".format(day))
			locations = locations.replace(to_replace=id,value="")
			locations.to_csv("data/{}-locations.csv".format(day),index=False)