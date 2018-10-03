from os import sys,environ
sys.path.append("..")

import unittest
from alfredbot.exceptions.UserNotFoundException import UserNotFoundException
from alfredbot.models.User import User
from alfredbot.controllers.User import UserController

class SimpleTest(unittest.TestCase):
	
	def setUp(self):
		self.controller = UserController()
		self.controller.add_user(100,"Alfred","Penyworth","alfred","alfred@insight.com")

	def tearDown(self):
		self.controller.remove_user(100)

	def test_load_user(self):
		user = User({"id":100})
		user.reload()
		self.assertEqual(user["id"],100)
		self.assertEqual(user["first_name"],"Alfred")
		self.assertEqual(user["last_name"],"Penyworth")
		self.assertEqual(user["username"],"alfred")
		self.assertEqual(user["mail"],"alfred@insight.com")

	def test_update_user(self):
		user = User({"id":100})
		user.reload()
		user["mail"] = "alfred@wayne.com"
		user.save()

		user = User({"id":100})
		user.reload()

		self.assertEqual(user["id"],100)
		self.assertEqual(user["first_name"],"Alfred")
		self.assertEqual(user["last_name"],"Penyworth")
		self.assertEqual(user["username"],"alfred")
		self.assertEqual(user["mail"],"alfred@wayne.com")

	def test_remove_user(self):
		self.controller.remove_user(100)

		user = User({"id":100})
		try:
			user.reload()
		except UserNotFoundException:
			users = self.controller.get_users()
			self.assertEqual(len(users),0)


if __name__ == '__main__':
    unittest.main()