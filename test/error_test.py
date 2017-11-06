from os import sys,environ

sys.path.append("..")

from alfredbot.BotConstructor import BotConstructor
from alfredbot.Blueprint import Blueprint

#first, we must define the token of the bot
token = environ.get("BOT_ALFRED_TOKEN")

#then, we can create the BotConstructor object
bot = BotConstructor(token)

#every time that this function execute, it will result on a "division by zero" exception
def start(bot,update):
	update.message.reply_text("The value of 1/0 is: {}".format(1/0))

def error(bot,update,error):
	print("Error: {}".format(error))

bot.add_command_handler("start",start)

bot.start()