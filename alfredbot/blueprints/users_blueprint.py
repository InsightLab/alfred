from alfredbot.models.User import User
from alfredbot.exceptions.UserNotFoundException import UserNotFoundException

from BotMother.Blueprint import Blueprint
from BotMother.Conversation import Conversation

from .helper import Helper

import re
import pandas as pd

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Filters

users_blueprint = Blueprint()

mail_regex = re.compile('[^@]+@[^@]+\\.[^@]+')

def map_users_to_keyboard(users,separator="\n",max_per_line=3):
	line = 0
	keyboard = [[]]
	for i,user in enumerate(users):
		name = "{} {}".format(user["first_name"],user["last_name"])
		text = "{}{}{}".format(user["id"],separator,name)
		keyboard[line].append(text)
		
		if (i+1)%max_per_line==0:
			line += 1
			keyboard.append([])
	return keyboard

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
		update.message.reply_text("Thank you. Now, please, give a phone number to contact (only numbers)")
		return "REQUEST_PHONE"
	else:
		update.message.reply_text("Invalid email. Please try again or send /cancel")
		return "REQUEST_EMAIL"

def request_phone(bot,update,user_data):
	number = update.message.text
	try:
		number = int(number)
		new_user = user_data["user"]
		new_user["phone"] = number
		new_user["role"] = ""
		new_user.save()
		Helper.reload_data()
		update.message.reply_text("Request sent to be inspected for one of ours admins.")
		Helper.notify_admins(bot,"{},{} to join us .To aprove, type /check_requests and select the id {}".format(new_user["last_name"],new_user["first_name"],new_user["id"]))
		return Conversation.END
	except Exception as e:
		print(e)
		update.message.reply_text("Invalid number. Please try again or send /cancel")
		return "REQUEST_PHONE"

def cancel_request(bot,update):
	update.message.reply_text("Request aborted. Have a nice day!")

	return Conversation.END

request_access_conversation.add_command_entry_point("request_access",start_request,pass_user_data=True)
request_access_conversation.add_message_to_state("REQUEST_EMAIL",request_email,pass_user_data=True)
request_access_conversation.add_message_to_state("REQUEST_PHONE",request_phone,pass_user_data=True)
request_access_conversation.add_command_to_fallback("cancel",cancel_request)

users_blueprint.add_conversation(request_access_conversation)

#-------------------------------------

manage_users_conversation = Conversation()

def start_get_users(bot,update,user_data):
	user_id = update.message.from_user.id
	if Helper.is_adm(user_id):
		text = "Choose an user to review or /done to end this conversation. The operation can be aborted by typing /cancel ."

		df = pd.read_csv("data/users.csv")
		users = [{p:row.values[i] for i,p in enumerate(df.columns)} for _,row in df.iterrows()]
		# for user in users:
		# 	text += "\t\t/{} {} {} ({})\n".format(user["id"],user["first_name"],user["last_name"],user["mail"])
		keyboard = map_users_to_keyboard(users)
		update.message.reply_text(text,reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))
		user_data["keyboard"] = keyboard
		return "REVIEW_USER"
	else:
		update.message.reply_text("You are not allowed to do this operation")

def start_check_requests(bot,update,user_data):
	user_id = update.message.from_user.id
	if Helper.is_adm(user_id):
		text = "Choose an user to review or /done to end this conversation. The operation can be aborted by typing /cancel ."

		df = pd.read_csv("data/users.csv")
		users = [{p:row.values[i] for i,p in enumerate(df.columns)} for _,row in df[df.type==-1].iterrows()]
		if len(users)==0:
			update.message.reply_text("No request to analyse")
			return Conversation.END

		# for user in users:
		# 	text += "\t\t/{} {} {} ({})\n".format(user["id"],user["first_name"],user["last_name"],user["mail"])

		keyboard = map_users_to_keyboard(users)
		update.message.reply_text(text,reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))
		user_data["keyboard"] = keyboard
		return "REVIEW_USER"
	else:
		update.message.reply_text("You are not allowed to do this operation.")

def review_user(bot,update,user_data):
	global df
	df = pd.read_csv("data/users.csv")

	# if update.message.text == "/done":
	# 	return done(bot,update)
	msg = update.message.text

	if not len(msg.split("\n"))==2:
		update.message.reply_text("You didn't choose a valid option. Try again or send /cancel .",
			reply_markup=ReplyKeyboardMarkup(user_data["keyboard"],one_time_keyboard=True))

	user_id = msg.split("\n")[0]
	user_data["selected"] = msg

	try:
		user_id = int(user_id)
		user = User({"id":user_id})
		user.reload()
		user_type = ["pendent","regular","administrator"][user["type"]+1]
		update.message.reply_text("User chosen:\nName: {} {}\nEmail: {}\nUsername: {}\nType: {}\nRole: {}\nPhone: {}".format(
			user["first_name"],user["last_name"],user["mail"],user["username"],user_type,user["role"],user["phone"]))

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
		return "UPDATE_ROLE"

	except:
		update.message.reply_text("Invalid Id. Try again.")
		return "REVIEW_USER"

def update_role(bot,update,user_data):
	command = update.message.text
	user = user_data["user"]

	if command not in ["ADM","USER"] and \
	(user["type"] == -1 and not command == "DISCARD") and \
	(user["type"] > -1 and not command == "REMOVE"):
		update.message.reply_text("Invalid command. Try again")
		return "UPDATE_ROLE"

	user_data["command"] = command
	roles = [["Researcher"],["Ph.D Candidate"],["Master Student"],["Visitor"],["Undergraduate"],["Professional"]]

	update.message.reply_text("Wich role this user have on the lab?",
		reply_markup=ReplyKeyboardMarkup(roles, one_time_keyboard=True))

	return "UPDATE_USER"

def update_user(bot,update,user_data):
	role = update.message.text
	roles = ["Researcher","Ph.D Candidate","Master Student","Visitor","Undergraduate","Professional"]

	if not role in roles:
		update.message.reply_text("Invalid role. Choose a valid one:",
		reply_markup=ReplyKeyboardMarkup(roles, one_time_keyboard=True))
		return "UPDATE_USER"

	command = user_data["command"]
	user = user_data["user"]
	user["role"] = role
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
		try:
			user_data["keyboard"].remove(user_data["selected"])
		except:
			pass
	else:
		update.message.reply_text("Invalid command. Try again")
		return "UPDATE_USER"

	Helper.reload_data()
	
	update.message.reply_text("Operation {} done! Choose another user or type /done .".format(command),
		reply_markup=ReplyKeyboardMarkup(user_data["keyboard"],one_time_keyboard=True))
	return "REVIEW_USER"

def done(bot,update):
	update.message.reply_text("Have a nice day!",reply_markup=ReplyKeyboardRemove())
	return Conversation.END

def cancel(bot,update):
	update.message.reply_text("Operation aborted.")
	return Conversation.END

manage_users_conversation.add_command_entry_point("users",start_get_users,pass_user_data=True)
manage_users_conversation.add_command_entry_point("check_requests",start_check_requests,pass_user_data=True)
manage_users_conversation.add_message_to_state("REVIEW_USER",review_user,pass_user_data=True)
manage_users_conversation.add_message_to_state("UPDATE_ROLE",update_role,pass_user_data=True)
manage_users_conversation.add_message_to_state("UPDATE_USER",update_user,pass_user_data=True)
manage_users_conversation.add_command_to_fallback("done",done)
manage_users_conversation.add_command_to_fallback("cancel",cancel)

users_blueprint.add_conversation(manage_users_conversation)
