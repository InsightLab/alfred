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

	def get_schedules(self,day,free=False):
		if not self.id:
			return None

		locations = pd.read_csv("{}-locations.csv".format(day))
		row = locations[locations.workstation==self.id]

		schedules = row.to_dict(orient="records")[0]

		def get(number):
			return (isnan(number) and free) or (not isnan(number) and not free)

		return {time:schedules[time] for time in schedules\
		 if get(schedules[time])}

	def add_schedule(self,user_id,day,time):
		if not self.id:
			return None

		locations = pd.read_csv("{}-locations.csv".format(day))
		row = locations[locations.workstation==self.id]

		schedules = row.to_dict(orient="records")[0]

		if isnan(schedules[time]):
			locations.loc[locations.workstation==self.id,[time]] = user_id
			locations.to_csv("{}-locations.csv".format(day))
			return True

		return False
