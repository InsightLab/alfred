from .exception.Exceptions import *
from .Conversation import Conversation
from telegram.ext import Filters
class Blueprint():
	def __init__(self):
		self.command_handlers = {}
		self.error_handler = None
		self.message_handler = None
		self.message_filter = None
		self.conversations = []
	
	def add_command_handler(self,command,command_handler):
		if(callable(command_handler)):
			if isinstance(command, str):
				self.command_handlers[command] = command_handler
			else:
				raise NotAStringException("{} isn't a valid command name. Command names must be string")
		else:
			raise NotCallableException("{} is not a function".format(command_handler))

	def get_command_handlers(self):
		return self.command_handlers

	def get_commands(self):
		return list(self.command_handlers.keys())

	def get_command(self,command):
		return self.command_handlers[command]

	def set_error_handler(self,error_handler):
		if(callable(error_handler)):
			self.error_handler = error_handler
		else:
			raise NotCallableException("{} object is not callable".format(type(error_handler)))

	def get_error_handler(self):
		return self.error_handler

	def set_message_handler(self,message_handler,message_filter=Filters.text):
		if(callable(message_handler)):
			self.message_handler = message_handler
			self.message_filter = message_filter
		else:
			raise NotCallableException("{} is not callable".format(type(message_handler)))

	def get_message_handler(self):
		return self.message_handler

	def get_message_filter(self):
		return self.message_filter

	def add_conversation(self,conversation):
		if isinstance(conversation,Conversation):
			self.conversations.append(conversation)
		else:
			raise NotAConversation("Must pass Conversation object, not {}".format(type(conversation)))

	def get_conversations(self):
		return self.conversations