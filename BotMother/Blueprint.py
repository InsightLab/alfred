"""
Module containing the Blueprint class.
This class allows to store an organization of handlers
to be used in the construction of a bot
"""

from .exception.Exceptions import *
from .Conversation import Conversation
from telegram.ext import Filters
class Blueprint():
	def __init__(self):
		self.command_handlers = {}
		self.error_handler = None
		self.message_handlers = []
		self.conversations = []
	
	def add_command_handler(self,command,command_handler):
		"""
		This method adds a handler to a command

		Parameters
		----------

		command: String
			The command that will trigger the handler
		command_handler: Callable
			The Callable object that will execute. Must receive 2 parameters:
				bot : the bot object from python-telegram-bot
				update : the update object from python-telegram-bot
		"""
		if(callable(command_handler)):
			if isinstance(command, str):
				self.command_handlers[command] = command_handler
			else:
				raise NotAStringException("{} isn't a valid command name. Command names must be string")
		else:
			raise NotCallableException("{} is not a function".format(command_handler))

	def get_command_handlers(self):
		"""
		Returns a dict of command handlers in the structure
		command : handler

		Returns
		-------
		
		message_handlers : dict()
			dict object where the key is the command and the value is the handler function
		"""
		return self.command_handlers

	def get_commands(self):
		"""
		Returns the list of commands defined

		Returns
		-------

		commands : List(String)
			List of commands defined

		"""
		return list(self.command_handlers.keys())

	def get_command(self,command):
		"""
		Returns the command handler from a command

		Parameters
		----------

		command : String
			The command that will be returned

		Returns
		-------

		handler : Callable
			Function that handle the command
		"""
		return self.command_handlers[command]

	def set_error_handler(self,error_handler):
		"""
		This method set the error handler

		Parameters
		----------

		error_handler : Callable
			Function that will handle the error event
		"""
		if(callable(error_handler)):
			self.error_handler = error_handler
		else:
			raise NotCallableException("{} object is not callable".format(type(error_handler)))

	def get_error_handler(self):
		"""
		Returns the function to handle errors

		Returns
		-------

		error_handler : Callable
			Handler of error event
		"""
		return self.error_handler

	def add_message_handler(self,message_handler,message_filter=Filters.text):
		"""
		This method adds a handler to a message type

		Parameters
		----------

		message_handler: Callable
			The Callable object that will execute. Must receive 2 parameters:
				bot : the bot object from python-telegram-bot
				update : the update object from python-telegram-bot
		message_filter: Filter from python-telegram-bot.
			A filter that will defines wich kind of message will trigger this event.
			The default is text.
		"""
		if(callable(message_handler)):
			self.message_handlers.append((message_handler,message_filter))
		else:
			raise NotCallableException("{} is not callable".format(type(message_handler)))

	def get_message_handlers(self):
		"""
		Returns a list of message handlers in the structure 
		(message_handler,messager_filter)

		Returns
		-------

		message_handlers : List((message_handler,messager_filter))
			List of messages handlers and its filters
		"""
		return self.message_handlers

	def add_conversation(self,conversation):
		"""
		Add a conversation flow to the blueprint

		Parameters
		----------

		conversation : Conversation object
			The conversation that will be added in the blueprint
		"""
		if isinstance(conversation,Conversation):
			self.conversations.append(conversation)
		else:
			raise NotAConversation("Must pass Conversation object, not {}".format(type(conversation)))

	def get_conversations(self):
		"""
		Returns the list of conversations on the blueprint

		Returns
		-------

		conversations : List(Conversation)
			List of conversations
		"""
		return self.conversations