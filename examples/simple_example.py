from os import sys,environ
sys.path.append("..")

from BotMother.BotConstructor import BotConstructor
from BotMother.Blueprint import Blueprint

#first, we must define the token of the bot
token = environ.get("BOT_ALFRED_TOKEN")

#then, we can create the BotConstructor object
bot = BotConstructor(token)

#we can define a function to handle updates on the bot
def start(bot,update):
	#the bot paramether represents an object from python-telegram-bot Bot class
	#update paramether represents an object from python-telegram-bot Update class
	update.message.reply_text("Bot started")

#then, we can add this function as a handler to the command "start"
bot.add_command_handler("start", start)

#we can also create a blueprint object, that will contains the organization of the handlers
blueprint = Blueprint()

#now we can define another function to handler a command
def ping(bot,update):
	update.message.reply_text("Pong!")

#here we define a command that will handler filters (the default is text, but can't be changed yet)
def msg(bot,update):
	update.message.reply_text(update.message.text)

#here we have the error handler, that will catch ONLY ERRORS FROM THE BOT. Python error will not be caught.
def error(bot,update,error):
	print(error)

#now, we set this handlers on the blueprint
blueprint.add_command_handler("ping", ping)
blueprint.add_message_handler(msg)
blueprint.set_error_handler(error)

#and add the blueprint to the BotConstructor
bot.add_blueprint(blueprint)

#now, we just need to start the pool
bot.start()