from .exception.Exceptions import *
from telegram.ext import Filters

class Conversation():

	def __init__(self):
		self.entry_points = []
		self.states = {}
		self.fallbacks = []

	def add_command_entry_point(self,command,command_handler):
		if(callable(command_handler)):
			if isinstance(command, str):
				self.entry_points.append((command,command_handler,None))
			else:
				raise NotAStringException("{} isn't a valid command name. Command names must be string")
		else:
			raise NotCallableException("{} is not a function".format(command_handler))

	def add_message_entry_point(self,message_handler,message_filter=Filters.text):
		if(callable(message_handler)):
			self.entry_points.append((None,message_handler,message_filter))
		else:
			raise NotCallableException("{} is not a function".format(message_handler))

	def get_entry_points(self):
		return self.entry_points

	def add_command_to_state(self,state,command,command_handler):
		if(callable(command_handler)):
			if isinstance(command, str):
				if not state in self.states:
					self.states[state] = []
				self.states[state].append((command,command_handler,None))
			else:
				raise NotAStringException("{} isn't a valid command name. Command names must be string")
		else:
			raise NotCallableException("{} is not a function".format(command_handler))

	def add_message_to_state(self,state,message_handler,message_filter=Filters.text):
		if(callable(message_handler)):
			if not state in self.states:
				self.states[state] = []
			self.states[state].append((None,message_handler,message_filter))
		else:
			raise NotCallableException("{} is not a function".format(message_handler))

	def get_states(self):
		return self.states

	def add_command_to_fallback(self,command,command_handler):
		if(callable(command_handler)):
			if isinstance(command, str):
				self.fallbacks.append((command,command_handler,None))
			else:
				raise NotAStringException("{} isn't a valid command name. Command names must be string")
		else:
			raise NotCallableException("{} is not a function".format(command_handler))

	def add_message_to_fallback(self,message_handler,message_filter=Filters.text):
		if(callable(message_handler)):
			self.fallbacks.append((None,message_handler,message_filter))
		else:
			raise NotCallableException("{} is not a function".format(message_handler))





	def get_fallbacks(self):
		return self.fallbacks