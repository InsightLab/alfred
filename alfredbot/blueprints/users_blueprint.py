from alfredbot.controllers.User import UserController
from alfredbot.models.User import User
from alfredbot.exceptions.UserNotFoundException import UserNotFoundException

from BotMother.Blueprint import Blueprint
from BotMother.Conversation import Conversation

import pandas as pd
import re

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Filters

users_blueprint = Blueprint()
df = pd.read_csv("data/users.csv")
admins_id = df[df['type']==1]['id'].values
mail_regex = re.compile('[^@]+@[^@]+\\.[^@]+')

def is_adm(id):
	return id in admins_id

def notify_admins(bot,text):
	for id in admins_id:
		print("Sending to {}".format(id))
		bot.sendMessage(text=text,chat_id=str(id))

#-------------------------------------

request_access_conversation = Conversation()


def start_request(bot,update,user_data):
	user = update.message.from_user
	new_user = User({"id":user.id})

	try:
		new_user.reload()
		if new_user["type"] == -1:
			update.message.reply_text("Your request was not reviewed yet. Please wait.")
		else:
			update.message.reply_text("Looks like you are already a member of our organization.")

		return Conversation.END

	except UserNotFoundException:
		new_user.update({
			"first_name":user.first_name,
			"last_name":user.last_name,
			"username":user.username,
			"type":-1
		})

		user_data["user"] = new_user
		update.message.reply_text("Ok, just send me your email, please. If you don't want it anymore, just send /cancel .")

		return "REQUEST_EMAIL"

def request_email(bot,update,user_data):
	mail = update.message.text
	if mail_regex.match(mail):
		new_user = user_data["user"]
		new_user["mail"] = mail
		new_user.save()
		update.message.reply_text("Request sent to be inspected for one of ours admins.")
		notify_admins(bot,"{},{} to join us".format(new_user["last_name"],new_user["first_name"]))
		return Conversation.END
	else:
		update.message.reply_text("Invalid email. Please try again or send /cancel")
		return "REQUEST_EMAIL"

def cancel_request(bot,update):
	update.message.reply_text("Request aborted. Have a nice day!")

	return Conversation.END

request_access_conversation.add_command_entry_point("request_access",start_request,pass_user_data=True)
request_access_conversation.add_message_to_state("REQUEST_EMAIL",request_email,pass_user_data=True)
request_access_conversation.add_command_to_fallback("cancel",cancel_request)

users_blueprint.add_conversation(request_access_conversation)

#-------------------------------------

manage_users_conversation = Conversation()

def start_get_users(bot,update,user_data):
	user_id = update.message.from_user.id
	if is_adm(user_id):
		text = "Choose an user to review or /done to end this conversation:\n\n"

		users = [{p:row.values[i] for i,p in enumerate(df.columns)} for _,row in df.iterrows()]
		for user in users:
			text += "\t\t/{} {} {} ({})\n".format(user["id"],user["first_name"],user["last_name"],user["mail"])

		update.message.reply_text(text)

		return "REVIEW_USER"
	else:
		update.message.reply_text("You are not allowed to do this operation.")

def start_check_requests(bot,update,user_data):
	user_id = update.message.from_user.id
	if is_adm(user_id):
		text = "Choose an user to review or /done to end this conversation:\n\n"

		users = [{p:row.values[i] for i,p in enumerate(df.columns)} for _,row in df[df.type==-1].iterrows()]
		if len(users)==0:
			update.message.reply_text("No request to analyse")
			return Conversation.END

		for user in users:
			text += "\t\t/{} {} {} ({})\n".format(user["id"],user["first_name"],user["last_name"],user["mail"])

		update.message.reply_text(text)

		return "REVIEW_USER"
	else:
		update.message.reply_text("You are not allowed to do this operation.")

def review_user(bot,update,user_data):
	global df
	df = pd.read_csv("data/users.csv")

	if update.message.text == "/done":
		return done(bot,update)

	user_id = update.message.text.replace("/","")

	try:
		user_id = int(float(user_id))
		user = User({"id":user_id})
		user.reload()
		user_type = ["pendent","regular","administrator"][user["type"]+1]
		update.message.reply_text("User chosen:\nName: {} {}\nEmail: {}\nType: ".format(
			user["first_name"],user["last_name"],user["mail"],user_type))

		reply_keyboard = [["ADM","USER"]]
		text = ""
		
		if user["type"]==-1:
			reply_keyboard[0].append("DISCARD")
			text += "Should I set {} {} as administrator (ADM), as a simple user (USER) or discard this request (DISCARD)?".format(user["first_name"],user["last_name"])
		else:
			reply_keyboard[0].append("REMOVE")
			text += "Should I set {} {} as administrator (ADM), as a simple user (USER) or remove this user (REMOVE)?".format(user["first_name"],user["last_name"])
		
		update.message.reply_text(text,reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
		user_data["user"] = user
		return "UPDATE_USER"

	except:
		update.message.reply_text("Invalid Id. Try again.")
		return "REVIEW_USER"	

def update_user(bot,update,user_data):
	command = update.message.text
	user = user_data["user"]
	if command == "ADM":
		user["type"] = 1
		user.save()
		bot.sendMessage(chat_id=str(user["id"]),text="You are now one of my masters from Insight Data Science Lab. I hope be helpful to you.")
	elif command == "USER":
		user["type"] = 0
		user.save()
		bot.sendMessage(chat_id=str(user["id"]),text="You are now a regular member on Insight Data Science Lab. I hope be helpful to you.")
	elif command == "DISCARD" or command == "REMOVE":
		bot.sendMessage(chat_id=str(user["id"]),text="Your access on Insight Data Science Lab has been denied.")
		user.remove()
	else:
		update.message.reply_text("Invalid command. Try again")
		return "UPDATE_USER"

	update.message.reply_text("Operation {} done! If you want to do something else, just choose another user or type /done .".format(command))
	return "REVIEW_USER"

def done(bot,update):
	update.message.reply_text("Have a nice day!")
	return Conversation.END

manage_users_conversation.add_command_entry_point("users",start_get_users,pass_user_data=True)
manage_users_conversation.add_command_entry_point("check_requests",start_check_requests,pass_user_data=True)
manage_users_conversation.add_message_to_state("REVIEW_USER",review_user,pass_user_data=True,message_filter=Filters.all)
manage_users_conversation.add_message_to_state("UPDATE_USER",update_user,pass_user_data=True)
manage_users_conversation.add_command_to_fallback("done",done)

users_blueprint.add_conversation(manage_users_conversation)
