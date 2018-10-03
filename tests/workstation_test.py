from os import sys,environ
sys.path.append("..")

import unittest
from alfredbot.exceptions.WorkstationNotFoundException import WorkstationNotFoundException
from alfredbot.models.Workstation import Workstation
from alfredbot.controllers.Workstation import WorkstationController

class SimpleTest(unittest.TestCase):
	
	def setUp(self):
		self.controller = WorkstationController()
		self.controller.add_workstation(100,"A simple machine")

	def tearDown(self):
		self.controller.remove_workstation(100)

	def test_load_workstation(self):
		workstation = Workstation({"id":100})
		workstation.reload()
		self.assertEqual(workstation["id"],100)
		self.assertEqual(workstation["description"],"A simple machine")
		

	def test_update_workstation(self):
		workstation = Workstation({"id":100})
		workstation.reload()
		workstation["description"] = "A not so simple machine"
		workstation.save()

		workstation = Workstation({"id":100})
		workstation.reload()

		self.assertEqual(workstation["id"],100)
		self.assertEqual(workstation["description"],"A not so simple machine")
		
	def test_remove_workstation(self):
		self.controller.remove_workstation(100)

		workstation = Workstation({"id":100})
		try:
			workstation.reload()
		except WorkstationNotFoundException:
			workstations = self.controller.get_workstations()
			self.assertEqual(len(workstations),0)


if __name__ == '__main__':
    unittest.main()