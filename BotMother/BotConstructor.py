"""
Module that contains the BotConstructor class, that is used
to help on the construction of services using a telegram Bot
"""

from .Blueprint import Blueprint
from .Conversation import Conversation
from .exception.Exceptions import *
import telegram
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters

class BotConstructor():

	def __init__(self,token=None,bot=None,show_log=True):
		"""
		Constructor of the class

		Parameters
		----------

		token : String
			Token generated from @BotFather on telegram
		bot : python-telegram-bot instance
			If you already have an instance of a bot, you can send it
		show_log : Boolean
			By default, the log of the bot will be displayed
		"""
		if show_log:			
			logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		if not bot:
			if token:
				self.updater = Updater(token)
			else:
				raise BotNotDefined("You must send a token or a bot instance")
		else:
			self.updater = Updater(bot=bot)

		self.dp = self.updater.dispatcher

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
				self.dp.add_handler(CommandHandler(command,command_handler))
			else:
				raise NotAString("{} isn't a valid command name. Command names must be string")
		else:
			raise NotCallableException("{} is not a function".format(command_handler))

	def add_conversation(self,conversation):
		"""
		This method adds a conversation flow

		Parameters
		----------

		conversation : Conversation object
			The conversation that will be added
		"""
		if isinstance(conversation,Conversation):
			entry_points = []
			for entry_point in conversation.get_entry_points():
				handler = None
				if entry_point[0]:
					handler = CommandHandler(entry_point[0],entry_point[1],pass_user_data=entry_point[3])
				else:
					handler = MessageHandler(entry_point[2],entry_point[1],pass_user_data=entry_point[3])
				entry_points.append(handler)

			states = {}
			states_commands = conversation.get_states()

			for state in states_commands:
				states[state] = []

				for command in states_commands[state]:
					if command[0]:
						states[state].append(CommandHandler(command[0],command[1],pass_user_data=command[3]))
					else:
						states[state].append(MessageHandler(command[2],command[1],pass_user_data=command[3]))

			fallbacks = []
			for fallback in conversation.get_fallbacks():
				handler = None
				if fallback[0]:
					handler = CommandHandler(fallback[0],fallback[1],pass_user_data=fallback[3])
				else:
					handler = MessageHandler(fallback[2],fallback[1],pass_user_data=fallback[3])
				fallbacks.append(handler)

			self.dp.add_handler(ConversationHandler(
				entry_points=entry_points,
				states=states,
				fallbacks=fallbacks
			))

		else:
			raise NotAConversation("Must pass Conversation object, not {}".format(type(conversation)))

	def set_error_handler(self,error_handler):
		"""
		This method set the error handler

		Parameters
		----------

		error_handler : Callable
			Function that will handle the error event
		"""
		if(callable(error_handler)):
			self.dp.add_error_handler(error_handler)
		else:
			raise NotCallableException("{} is not a function".format(error_handler))

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
			self.dp.add_handler(MessageHandler(message_filter,message_handler))
		else:
			raise NotCallableException("{} is not a function".format(message_handler))

	def add_blueprint(self,blueprint):
		"""
		This method receives a blueprint and applies to the bot

		Parameters
		----------

		blueprint : Blueprint object
			The blueprint that will be applied
		"""
		if isinstance(blueprint,Blueprint):
			for command in blueprint.get_commands():
				self.add_command_handler(command,blueprint.get_command(command))
			
			for conversation in blueprint.get_conversations():
				self.add_conversation(conversation)

			for message in blueprint.get_message_handlers():
				self.add_message_handler(message[0],message[1])

			if(blueprint.get_error_handler()!=None):
				self.set_error_handler(blueprint.get_error_handler())	
			
		else:
			raise NotABlueprintException("Must pass Blueprint object, not {}".format(type(blueprint)))

	def start(self):
		"""
		Starts the service
		"""
		print("Starting bot updater...")
		return self.updater.start_polling()
		
	def idle(self):
		"""
		Put the program on iddle state
		"""
		self.updater.idle()

	def stop(self):
		"""
		Stops the service
		"""
		print("Stopping bot updater...")
		self.updater.stop()

