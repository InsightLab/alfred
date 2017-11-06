from .Blueprint import Blueprint
from .Conversation import Conversation
from .exception.Exceptions import *
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters

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

	def add_conversation(self,conversation):
		if isinstance(conversation,Conversation):
			entry_points = []
			for entry_point in conversation.get_entry_points():
				handler = None
				if entry_point[0]:
					handler = CommandHandler(entry_point[0],entry_point[1])
				else:
					handler = MessageHandler(entry_point[2],entry_point[1])
				entry_points.append(handler)

			states = {}
			states_commands = conversation.get_states()

			for state in states_commands:
				states[state] = []

				for command in states_commands[state]:
					if command[0]:
						states[state].append(CommandHandler(command[0],command[1]))
					else:
						states[state].append(MessageHandler(command[2],command[1]))

			fallbacks = []
			for fallback in conversation.get_fallbacks():
				handler = None
				if fallback[0]:
					handler = CommandHandler(fallback[0],fallback[1])
				else:
					handler = MessageHandler(fallback[2],fallback[1])
				fallbacks.append(handler)

			self.dp.add_handler(ConversationHandler(
				entry_points=entry_points,
				states=states,
				fallbacks=fallbacks
			))

		else:
			raise NotAConversation("Must pass Conversation object, not {}".format(type(conversation)))

	def set_error_handler(self,error_handler):
		if(callable(error_handler)):
			self.dp.add_error_handler(error_handler)
		else:
			raise NotCallableException("{} is not a function".format(error_handler))

	def set_message_handler(self,message_handler,message_filter=Filters.text):
		if(callable(message_handler)):
			self.dp.add_handler(MessageHandler(message_filter,message_handler))
		else:
			raise NotCallableException("{} is not a function".format(message_handler))

	def add_blueprint(self,blueprint):
		if isinstance(blueprint,Blueprint):
			for command in blueprint.get_commands():
				self.add_command_handler(command,blueprint.get_command(command))
			
			for conversation in blueprint.get_conversations():
				self.add_conversation(conversation)

			if(blueprint.get_error_handler()!=None):
				self.set_error_handler(blueprint.get_error_handler())	
			
			if(blueprint.get_message_handler()!=None):
				self.set_message_handler(blueprint.get_message_handler(),blueprint.get_message_filter())
		else:
			raise NotABlueprint("Must pass Blueprint object, not {}".format(type(blueprint)))

	def start(self):
		print("Starting bot updater...")
		self.updater.start_polling()
		self.updater.idle()
