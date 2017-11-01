from .Blueprint import Blueprint
from .exception.Exceptions import *
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

class BotConstructor():

	def __init__(self,token):
		self.updater = Updater(token)
		self.dp = self.updater.dispatcher

	def add_command_handler(self,command,command_handler):
		if(callable(command_handler)):
			if isinstance(command, str):
				self.dp.add_handler(CommandHandler(command,command_handler))
			else:
				raise NotAString("{} isn't a valid command name. Command names must be string")
		else:
			raise NotCallableException("{} is not a function".format(command_handler))

	def set_error_handler(self,error_handler):
		if(callable(error_handler)):
			self.dp.add_error_handler(error_handler)
		else:
			raise NotCallableException("{} is not a function".format(error_handler))

	def set_message_handler(self,message_handler):
		if(callable(message_handler)):
			self.dp.add_handler(MessageHandler(Filters.text,message_handler))
		else:
			raise NotCallableException("{} is not a function".format(message_handler))

	def add_blueprint(self,blueprint):
		if isinstance(blueprint,Blueprint):
			for command in blueprint.get_commands():
				self.add_command_handler(command,blueprint.get_command(command))
			
			if(blueprint.get_error_handler()!=None):
				self.set_error_handler(blueprint.get_error_handler())	
			
			if(blueprint.get_message_handler()!=None):
				self.set_message_handler(blueprint.get_message_handler())
		else:
			raise NotABlueprint("Must pass Blueprint object, not {}".format(type(blueprint)))

	def start(self):
		print("Starting bot updater...")
		self.updater.start_polling()
		self.updater.idle()
