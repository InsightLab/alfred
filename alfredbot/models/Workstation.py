import pandas as pd
from math import isnan
from .AbstractPandas import AbstractPandas
from alfredbot.exceptions.WorkstationNotFoundException import WorkstationNotFoundException

#user model
class Workstation(AbstractPandas):
	
	def __init__(self,d={}):
		super()
		self.update(d)
		file = "data/workstations.csv"
		super().load_dataframe(file)

	properties = ["id","description"]

	def reload(self):
		super().reload()
		if "description" not in self:
			raise WorkstationNotFoundException("Workstation {} not found".format(self["id"]))

	def remove(self):
		super().remove()

	def get_schedules(self,day,free=False):
		if not self.id:
			return None

		locations = pd.read_csv("data/{}-locations.csv".format(day))
		row = locations[locations.workstation==self.id]

		schedules = row.to_dict(orient="records")[0]
		del schedules["workstation"]

		def get(number):
			return (isnan(number) and free) or (not isnan(number) and not free)

		return {time:schedules[time] for time in schedules\
		 if get(schedules[time])}

	def add_schedule(self,user_id,day,time):
		if not self.id:
			return None

		locations = pd.read_csv("data/{}-locations.csv".format(day))
		row = locations[locations.workstation==self.id]

		schedules = row.to_dict(orient="records")[0]

		if isnan(schedules[time]):
			locations.loc[locations.workstation==self.id,[time]] = user_id
			locations.to_csv("data/{}-locations.csv".format(day),index=False)
			return True

		return False

	def remove_schedule(self,day,time):
		locations = pd.read_csv("data/{}-locations.csv".format(day))
		locations.loc[locations["workstation"] == self.id,time] = ""
		locations.to_csv("data/{}-locations.csv".format(day),index=False)
