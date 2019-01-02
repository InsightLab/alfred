from BotMother.BotConstructor import BotConstructor

from alfredbot.models.User import User
from alfredbot.exceptions.UserNotFoundException import UserNotFoundException

from alfredbot.blueprints.users_blueprint import users_blueprint
from alfredbot.blueprints.workstations_blueprint import workstations_blueprint

from telegram.ext import CallbackQueryHandler

from os import environ
from datetime import datetime as dt

token = environ.get("BOT_ALFRED_TOKEN")

bot = BotConstructor(token=token)

def help(bot, update):
	user = update.message.from_user
	user = User({"id":user.id})
	textFile = "texts/not_user_help_text.txt"
	try:
		user.reload()

		if user["type"] == -1:
			update.message.reply_text("Your request was not reviewed yet. Please wait.")
			return
		elif user["type"] == 0:
			textFile = "texts/user_help_text.txt"
		else:
			textFile = "texts/admin_help_text.txt"

		with open(textFile) as f:
			update.message.reply_text(f.read())

	except UserNotFoundException:
		with open(textFile) as f:
			update.message.reply_text(f.read())

	
def start(bot,update):
	with open("texts/start_text.txt") as f:
			update.message.reply_text(f.read())

def clean_button(bot,update):
	query = update.callback_query

	obj = query.data

	user = query.from_user

	text = "Obrigado {}.\nManutenção registrada!\n".format(user.username, obj)

	bot.edit_message_text(text=query.message.text+"\nUPDATE: limpo por "+user.username,
						  chat_id=query.message.chat_id,
						  message_id=query.message.message_id
						  )
	
	with open("{}_cleaning_history.txt".format(obj), 'a') as f:
		f.write("{},{}\n".format(dt.now(),user.username))

	bot.sendMessage(chat_id=query.message.chat_id, text=text)

bot.add_command_handler("start",start)
bot.add_command_handler("help",help)

bot.dp.add_handler(CallbackQueryHandler(clean_button))

bot.add_blueprint(users_blueprint)
bot.add_blueprint(workstations_blueprint)

bot.start()

bot.idle()