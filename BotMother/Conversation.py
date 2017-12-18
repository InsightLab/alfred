"""
Module conataining the Conversation class.
This class is used to create a conversation flow to the bot
"""

from .exception.Exceptions import *
from telegram.ext import Filters,ConversationHandler


class Conversation():
	#static value to represent the end of a conversation
	END = ConversationHandler.END
	
	def __init__(self):
		self.entry_points = []
		self.states = {}
		self.fallbacks = []

	def add_command_entry_point(self,command,command_handler,pass_user_data=False):
		"""
		This method adds a command event as a entry point to the conversation.
		Entry poins are events that, when triggered, starts the conversation flow.

		Parameters
		----------

		command : String
			The name of the command that will trigger the event
		command_handler : Callable
			The Callable object that will execute. Must receive 2 parameters:
				bot : the bot object from python-telegram-bot
				update : the update object from python-telegram-bot
			This callable must return the next state of the conversation. Conversation.END
			will represents the end of the conversation
		pass_user_data: Boolean
			This says if an object will be passed over the states of the conversation,
			allowing to store information.
		"""
		if(callable(command_handler)):
			if isinstance(command, str):
				self.entry_points.append((command,command_handler,None,pass_user_data))
			else:
				raise NotAStringException("{} isn't a valid command name. Command names must be string")
		else:
			raise NotCallableException("{} is not a function".format(command_handler))

	def add_message_entry_point(self,message_handler,message_filter=Filters.text,pass_user_data=False):
		"""
		This method adds a message event as a entry point to the conversation.
		Entry poins are events that, when triggered, starts the conversation flow.

		Parameters
		----------

		message_handler : Callable
			The Callable object that will execute. Must receive 2 parameters:
				bot : the bot object from python-telegram-bot
				update : the update object from python-telegram-bot
			This callable must return the next state of the conversation. Conversation.END
			will represents the end of the conversation
		message_filter: Filter from python-telegram-bot
			A filter that will defines wich kind of message will trigger this event.
			The default is text.
		pass_user_data: Boolean
			This says if an object will be passed over the states of the conversation,
			allowing to store information.
		"""
		if(callable(message_handler)):
			self.entry_points.append((None,message_handler,message_filter,pass_user_data))
		else:
			raise NotCallableException("{} is not a function".format(message_handler))

	def get_entry_points(self):
		"""
		Return the list of entry_points as a tuple (command,function,filter), where:
		* If command = None, then is a Command Handler
		* Else, is a Message Handler

		Returns
		-------

		entry_points : List(command,function,filter)
			List of command(if is a command handler), handler function and
			filter(if is message handler)
		"""
		return self.entry_points

	def add_command_to_state(self,state,command,command_handler,pass_user_data=False):
		"""
		This method adds a command event to a state of the conversation.

		Parameters
		----------
		
		state: String
			The state of the conversation that this handler will be designed
		command : String
			The name of the command that will trigger the event
		command_handler : Callable
			The Callable object that will execute. Must receive 2 parameters:
				bot : the bot object from python-telegram-bot
				update : the update object from python-telegram-bot
			This callable must return the next state of the conversation. Conversation.END
			will represents the end of the conversation
		pass_user_data: Boolean
			This says if an object will be passed over the states of the conversation,
			allowing to store information.
		"""
		if(callable(command_handler)):
			if isinstance(command, str):
				if not state in self.states:
					self.states[state] = []
				self.states[state].append((command,command_handler,None,pass_user_data))
			else:
				raise NotAStringException("{} isn't a valid command name. Command names must be string")
		else:
			raise NotCallableException("{} is not a function".format(command_handler))

	def add_message_to_state(self,state,message_handler,message_filter=Filters.text,pass_user_data=False):
		"""
		This method adds a message event to a state of the conversation.

		Parameters
		----------
		
		state: String
			The state of the conversation that this handler will be designed
		message_handler : Callable
			The Callable object that will execute. Must receive 2 parameters:
				bot : the bot object from python-telegram-bot
				update : the update object from python-telegram-bot
			This callable must return the next state of the conversation. Conversation.END
			will represents the end of the conversation
		message_filter: Filter from python-telegram-bot
			A filter that will defines wich kind of message will trigger this event.
			The default is text.
		pass_user_data: Boolean
			This says if an object will be passed over the states of the conversation,
			allowing to store information.
		"""
		if(callable(message_handler)):
			if not state in self.states:
				self.states[state] = []
			self.states[state].append((None,message_handler,message_filter,pass_user_data))
		else:
			raise NotCallableException("{} is not a function".format(message_handler))

	def get_states(self):
		"""
		Return the dict where the key is a state and the value is a list of
		tuple like (command,function,filter), where:
		* If command = None, then is a Command Handler
		* Else, is a Message Handler

		Returns
		-------

		states : dict()
			dict where the key is a state and the value is a list
			of command(if is a command handler), handler function and
			filter(if is message handler)
		"""
		return self.states

	def add_command_to_fallback(self,command,command_handler,pass_user_data=False):
		"""
		This method adds a command event as a fallback to the conversation.
		Fallbacks are events that, when triggered, may cancel the conversation.

		Parameters
		----------

		command : String
			The name of the command that will trigger the event
		command_handler : Callable
			The Callable object that will execute. Must receive 2 parameters:
				bot : the bot object from python-telegram-bot
				update : the update object from python-telegram-bot
			This callable must return the next state of the conversation. Conversation.END
			will represents the end of the conversation.
		pass_user_data: Boolean
			This says if an object will be passed over the states of the conversation,
			allowing to store information.
		"""
		if(callable(command_handler)):
			if isinstance(command, str):
				self.fallbacks.append((command,command_handler,None,pass_user_data))
			else:
				raise NotAStringException("{} isn't a valid command name. Command names must be string")
		else:
			raise NotCallableException("{} is not a function".format(command_handler))

	def add_message_to_fallback(self,message_handler,message_filter=Filters.text,pass_user_data=False):
		"""
		This method adds a message event as a fallback to the conversation.
		Fallbacks are events that, when triggered, may cancel the conversation.

		Parameters
		----------

		message_handler : Callable
				The Callable object that will execute. Must receive 2 parameters:
					bot : the bot object from python-telegram-bot
					update : the update object from python-telegram-bot
				This callable must return the next state of the conversation. Conversation.END
				will represents the end of the conversation
		message_filter: Filter from python-telegram-bot
				A filter that will defines wich kind of message will trigger this event.
				The default is text.
		pass_user_data: Boolean
			This says if an object will be passed over the states of the conversation,
			allowing to store information.
		"""
		if(callable(message_handler)):
			self.fallbacks.append((None,message_handler,message_filter,pass_user_data))
		else:
			raise NotCallableException("{} is not a function".format(message_handler))

	def get_fallbacks(self):
		"""
		Return the list of entry_points as a tuple (command,function,filter), where:
		* If command = None, then is a Command Handler
		* Else, is a Message Handler

		Returns
		-------

		fallbacks : List(command,function,filter)
			List of command(if is a commkand handler), handler function and
			filter(if is message handler)
		"""
		return self.fallbacks