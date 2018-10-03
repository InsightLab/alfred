from os import sys,environ

sys.path.append("..")

from telegram.ext import Filters
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from BotMother.BotConstructor import BotConstructor
from BotMother.Blueprint import Blueprint
from BotMother.Conversation import Conversation

"""
This test shows how to construct a conversation with the bot.
Here, we have a conversation where the bots wants to know the user,
askin the genre, a photo, location and some description.
To understand better the wor flow of the conversation, search about the
State design pattern and/or automatons.
"""

#first, we must define the token of the bot
token = environ.get("BOT_ALFRED_TOKEN")

#then, we can create the BotConstructor object
bot = BotConstructor(token)

#we can create a blueprint object, that will contains the organization of the conversation
blueprint = Blueprint()

#this function will start the conversation
def start(bot, update):
	print("Starting conversation")
	#this is a set of possible answers
	reply_keyboard = [['Boy', 'Girl']]

	#the reply_markup hides the keyborad and replace for the set of options defined
	update.message.reply_text(
		'Hi! I will hold a conversation with you. '
		'Send /cancel to stop talking to me.\n\n'
		'Are you a boy or a girl?',
		reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

	#after the message be sent, the bot will change to the "GENDER" state
	return "GENDER"


def gender(bot, update):
	#the message will be one of the options from the start function
	user = update.message.from_user
	print("Gender of {}: {}".format(user.first_name, update.message.text))
	update.message.reply_text('I see! Please send me a photo of yourself, '
							  'so I know what you look like, or send /skip if you don\'t want to.',
							  reply_markup=ReplyKeyboardRemove())

	#now, we change to the "PHOTO" state
	return "PHOTO"


def photo(bot, update):
	#if the user sends a photo, it will be stored on user_photo.jpg
	user = update.message.from_user
	photo_file = bot.get_file(update.message.photo[-1].file_id)
	photo_file.download('user_photo.jpg')
	print("Photo of {}: {}".format(user.first_name, 'user_photo.jpg'))
	update.message.reply_text('Gorgeous! Now, send me your location please, '
							  'or send /skip if you don\'t want to.')

	#now, we change to the "LOCATION" state
	return "LOCATION"


def skip_photo(bot, update):
	#the user may not want to send a photo, so we jump to the next state
	user = update.message.from_user
	print("User {} did not send a photo.".format(user.first_name))
	update.message.reply_text('I bet you look great! Now, send me your location please, '
							  'or send /skip.')

	#now, we change to the "LOCATION" state
	return "LOCATION"


def location(bot, update):
	#if the user sends the location, we print the coordinates
	user = update.message.from_user
	user_location = update.message.location
	print("Location of {}: {} / {}".format(user.first_name, user_location.latitude,
				user_location.longitude))
	update.message.reply_text('Maybe I can visit you sometime! '
							  'At last, tell me something about yourself.')

	#now, we change to the "BIO" state
	return "BIO"


def skip_location(bot, update):
	#the user may not want to send the location, so we jump to the next state
	user = update.message.from_user
	print("User {} did not send a location.".format(user.first_name))
	update.message.reply_text('You seem a bit paranoid! '
							  'At last, tell me something about yourself.')

	#now, we change to the "BIO" state
	return "BIO"


def bio(bot, update):
	#here, the user say some description
	user = update.message.from_user
	print("Bio of {}: {}".format(user.first_name, update.message.text))
	update.message.reply_text('Thank you! I hope we can talk again some day.')

	#and now the conversation ends
	return Conversation.END


def cancel(bot, update):
	#the user can cancel the conversation anytime
	user = update.message.from_user
	print("User {} canceled the conversation.".format(user.first_name))
	update.message.reply_text('Bye! I hope we can talk again some day.',
							  reply_markup=ReplyKeyboardRemove())

	return Conversation.END

#we can create a Conversation object to organize this conversation flow
conversation = Conversation()

#we must add a entry point, that represents the first command/message to start the conversation flow
#OBS: we can have multiple entry points
conversation.add_command_entry_point("start", start)

#for each state, we will define the possible command/messages that can be received
conversation.add_message_to_state("GENDER", gender)

conversation.add_message_to_state("PHOTO", photo, message_filter=Filters.photo)
conversation.add_command_to_state("PHOTO", "skip", skip_photo)

conversation.add_message_to_state("LOCATION", location, message_filter=Filters.location)
conversation.add_command_to_state("LOCATION", "skip", skip_location)

conversation.add_message_to_state("BIO", bio)

#all the functions to stop the conversations are added as a fallback
#OBS: we can have multiple fallbacks
conversation.add_command_to_fallback("cancel", cancel)

#now we add the conversation to the blueprint
blueprint.add_conversation(conversation)

#and add the blueprint to the BotConstructor
bot.add_blueprint(blueprint)

#now, we just need to start the pool
bot.start()