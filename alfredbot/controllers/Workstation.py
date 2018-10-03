
from alfredbot.models.Workstation import Workstation
from alfredbot.models.User import User
from alfredbot.exceptions.ConflitScheduleException import ConflitScheduleException
from alfredbot.exceptions.BadTimeException import BadTimeException

class WorkstationController():

	def get_workstations(self):
		return Workstation().get_all()

	def add_workstation(self,id,description=""):
		workstation = Workstation({
			"id":id,
			"description":description
			})

		workstation.save()
		return workstation

	def remove_workstation(self,id):
		workstation = Workstation({"id":id})
		workstation.remove()

	
	def add_schedule(self,workstation_id,user_id,day,time):
		workstation = Workstation({"id":workstationid})
		workstation.reload()

		return workstation.add_schedule(user_id,day,time)


	def remove_schedule(self,data):
		result = None
		try:
			result = self.__remove_schedule(data)

		except Exception as e:
			print(e)
			result = {"err":str(e)}

		return result



