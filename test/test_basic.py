from os import sys,environ
sys.path.append("..")

import unittest
from telegram.utils.request import Request
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from ptbtest import ChatGenerator, MessageGenerator, Mockbot, UserGenerator
from BotMother.BotConstructor import BotConstructor
from BotMother.Blueprint import Blueprint

class SimpleTest(unittest.TestCase):
	
	def setUp(self):
		# For use within the tests we nee some stuff. Starting with a Mockbot
		self.bot = Mockbot()
		self.constructor = BotConstructor(bot=self.bot)
		# Some generators for users and chats
		self.ug = UserGenerator()
		self.cg = ChatGenerator()
		# And a Messagegenerator and updater (for use with the bot.)
		self.mg = MessageGenerator()
		# self.updater = Updater(bot=self.bot)

		def start(bot,update):
			self.start_value = True

		self.constructor.add_command_handler("start", start)

		blueprint = Blueprint()

		def ping(bot,update):
			self.ping_value = True

		def msg(bot,update):
			self.message_value = update.message.text

		blueprint.add_command_handler("ping", ping)
		blueprint.add_message_handler(msg)

		self.constructor.add_blueprint(blueprint)


	def test_start(self):
		self.constructor.start()
		update = self.mg.get_message(text="/start")
		self.bot.insertUpdate(update)

		self.assertEqual(self.start_value, True)

		self.constructor.stop()


	def test_ping(self):
		self.constructor.start()
		update = self.mg.get_message(text="/ping")
		self.bot.insertUpdate(update)

		self.assertEqual(self.ping_value, True)

		self.constructor.stop()


	def test_message(self):
		self.constructor.start()
		update = self.mg.get_message(text="alfred is a cool name!")
		self.bot.insertUpdate(update)

		self.assertEqual(self.message_value, "alfred is a cool name!")

		self.constructor.stop()


if __name__ == '__main__':
    unittest.main()