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
