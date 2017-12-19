from alfredbot.models.Workstation import Workstation
from alfredbot.models.User import User
from alfredbot.controllers.Workstation import WorkstationController
from alfredbot.exceptions.WorkstationNotFoundException import WorkstationNotFoundException

from BotMother.Blueprint import Blueprint
from BotMother.Conversation import Conversation

from .helper import Helper

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)

def map_workstations_to_keyboard(workstations,separator="\n",max_per_line=3):
	line = 0
	keyboard = [[]]

	workstations = sorted(workstations, key=lambda w: w["id"])

	for i,workstation in enumerate(workstations):
		keyboard[line].append(str(workstation["id"]))
		
		if (i+1)%max_per_line==0:
			line += 1
			keyboard.append([])
	return keyboard

def map_times_to_keyboard(times,names=False,separator="\n",max_per_line=3):
	line = 0
	keyboard = [[]]
	for i,time in enumerate(times):
		if names:
			user = User({"id":times[time]})
			user.reload()
			name = "{} {}".format(user["first_name"],user["last_name"])
			text = "{}\n{}".format(time,name)

		else:
			text = time

		keyboard[line].append(text)
		
		if (i+1)%max_per_line==0:
			line += 1
			keyboard.append([])

	return keyboard

controller = WorkstationController()

workstations_blueprint = Blueprint()

manage_workstations_conversation = Conversation()

#/workstations
def start_workstations(bot,update,user_data):
	user_id = update.message.from_user.id
	if not Helper.is_user(user_id):
		update.message.reply_text("You are not a member of Insight Data Science Lab. Access denied")
		return Conversation.END

	workstations = controller.get_workstations()
	keyboard = map_workstations_to_keyboard(workstations)
	user_data["workstations_keyboard"] = keyboard
	update.message.reply_text("Choose a workstation to continue",
		reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))

	return "REVIEW_WORKSTATION"

# message (workstation id)
def review_workstation(bot,update,user_data):
	workstation_id = int(update.message.text)

	try:
		workstation = Workstation({"id":workstation_id})
		workstation.reload()
		user_data["workstation"] = workstation

		keyboard = [["/free"],["/occupied"]]
		aux_text = ""
		if Helper.is_adm(update.message.from_user.id):
			keyboard.append(["/update"])
			keyboard.append(["/remove"])
			aux_text += ";\n/update to update workstation's description;\n/remove to remove the workstation."


		text = "Workstation choosen: {}\n\t{}".format(
			workstation["id"],workstation["description"])

		update.message.reply_text(text)
		update.message.reply_text("Use /free to check free time slots;\n/occupied to check for occupied slots{}".format(aux_text),
			reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))

		user_data["options_keyboard"] = keyboard

		return "CHECK_WORKSTATION"

	except WorkstationNotFoundException:
		update.message.reply_text("Invalid workstation. Please, choose one.",
			reply_markup=ReplyKeyboardMarkup(user_data["workstations_keyboard"],one_time_keyboard=True))

		return "REVIEW_WORKSTATION"
#/free
def check_workstation_free_day(bot,update,user_data):
	user_data["free"] = True
	keyboard = [["Sunday"],["Monday"],["Tuesday"],["Wednesday"],
		["Thursday"],["Friday"],["Saturday"]]
	user_data["days_keyboard"] = keyboard

	update.message.reply_text("Choose a day to check.",
			reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))

	return 'CHECK_WORKSTATION_SLOTS'

#/occupied
def check_workstation_occupied_day(bot,update,user_data):
	user_data["free"] = False
	keyboard = [["Sunday"],["Monday"],["Tuesday"],["Wednesday"],
		["Thursday"],["Friday"],["Saturday"]]
	user_data["days_keyboard"] = keyboard

	update.message.reply_text("Choose a day to check.",
			reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))

	return 'CHECK_WORKSTATION_SLOTS'

#message with day.
def check_workstations_slots(bot,update,user_data):
	day = update.message.text

	if day not in ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]:
		update.message.reply_text("Invalid day. Try again.",
			reply_markup=ReplyKeyboardMarkup(user_data["days_keyboard"],one_time_keyboard=True))

		return 'CHECK_WORKSTATION_SLOTS'
	
	user_data["day"] = day.lower()	
	slots = user_data["workstation"].get_schedules(day.lower(),free=user_data["free"])
	if len(slots) == 0:
		update.message.reply_text("There is no slot to show. Send /back to return to workstations selection.")
		return "BACK"

	if not user_data["free"]:
		text = "Occupied slots:\n"

		if Helper.is_adm(update.message.from_user.id):
			for time in sorted(slots):
				user = User({"id":slots[time]})
				user.reload()
				text += "\t\t{} - {} {}\n".format(time,user["first_name"],user["last_name"])

		else:
			text += "\n".join([time for time in sorted(slots)])

		update.message.reply_text(text)

		user_slots = [time for time in sorted(slots) if slots[time]==update.message.from_user.id]
		
		if len(user_slots)>0:
			update.message.reply_text("You have time slots on this workstations. Send /release if you want to release some slots or /back to see the workstations again.",
				reply_markup=ReplyKeyboardMarkup([["/back"],["/release"]]))
			user_data["slots"] = user_slots
			return "BACK_OR_RELEASE"
		
		else:
			update.message.reply_text("Send /back to return to workstations selection.")
			return "BACK"
		

	else:
		user_data["slots"] = [time for time in sorted(slots)]
		text = "Free slots:\n"
		text += "\n".join(["\t\t{}".format(time) for time in sorted(slots)])

		update.message.reply_text(text)

		update.message.reply_text("If you want to request a time slot, send /request . Otherwise, send /back to return to workstations selection",
				reply_markup=ReplyKeyboardMarkup([["/back"],["/request"]]))

		return "BACK_OR_REQUEST"

# /request
def request_workstation(bot,update,user_data):
	slots = user_data["slots"]

	keyboard = map_times_to_keyboard(slots)
	user_data["slots_keyboard"] = keyboard
	update.message.reply_text("Select a slot to request.",
		reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))

	return "REQUESTING_WORKSTATION"

# message with time slot
def requesting_workstation(bot,update,user_data):
	time = update.message.text

	if not time in user_data["slots"]:
		update.message.reply_text("Invalid time slot. Try again.",
			reply_markup=ReplyKeyboardMarkup(user_data["slots_keyboard"],one_time_keyboard=True))
		
		return "REQUESTING_WORKSTATION"

	if user_data["workstation"].add_schedule(update.message.from_user.id,user_data["day"],time):
		update.message.reply_text("The workstation {} will be yours at {}".format(user_data["workstation"]["id"],time))	
	
	else:
		update.message.reply_text("Looks like someone has taken this slot first. Sorry...")
	user_data["slots"].remove(time)
	
	
	if len(user_data["slots"])==0:
		update.message.reply_text("There are no more slots on this workstation. Send /back to return to workstations selection.")
		return "BACK"

	keyboard = map_times_to_keyboard(user_data["slots"])
	user_data["slots_keyboard"] = keyboard
	update.message.reply_text("Select a slot to request or send /back to return to workstations selection.",
		reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))

	return "REQUESTING_WORKSTATION"

# /release
def release_workstation(bot,update,user_data):
	slots = user_data["slots"]

	keyboard = map_times_to_keyboard(slots)
	user_data["slots_keyboard"] = keyboard
	update.message.reply_text("Select a slot to release.",
		reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))

	return "RELEASING_WORKSTATION"

# message with time slot
def releasing_workstation(bot,update,user_data):
	time = update.message.text

	if not time in user_data["slots"]:
		update.message.reply_text("Invalid time slot. Try again.",
			reply_markup=ReplyKeyboardMarkup(user_data["slots_keyboard"],one_time_keyboard=True))
		
		return "RELEASING_WORKSTATION"

	print(user_data["slots"])
	print(time)
	user_data["workstation"].remove_schedule(user_data["day"],time)
	
	user_data["slots"].remove(time)

	if len(user_data["slots"])==0:
		update.message.reply_text("You have no more slots on this workstation. Send /back to return to workstations selection.")
		return "BACK"

	keyboard = map_times_to_keyboard(user_data["slots"])
	user_data["slots_keyboard"] = keyboard
	update.message.reply_text("Select a slot to release or send /back to return to workstations selection.",
		reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))

	return "RELEASING_WORKSTATION"

def done(bot,update):
	update.message.reply_text("Have a nice day!",reply_markup=ReplyKeyboardRemove())
	return Conversation.END

manage_workstations_conversation.add_command_entry_point("workstations",start_workstations,pass_user_data=True)

manage_workstations_conversation.add_message_to_state("REVIEW_WORKSTATION",review_workstation,pass_user_data=True)

manage_workstations_conversation.add_command_to_state("CHECK_WORKSTATION","free",check_workstation_free_day,pass_user_data=True)
manage_workstations_conversation.add_command_to_state("CHECK_WORKSTATION","occupied",check_workstation_occupied_day,pass_user_data=True)

manage_workstations_conversation.add_message_to_state("CHECK_WORKSTATION_SLOTS",check_workstations_slots,pass_user_data=True)

manage_workstations_conversation.add_command_to_state("BACK_OR_RELEASE","back",start_workstations,pass_user_data=True)
manage_workstations_conversation.add_command_to_state("BACK_OR_RELEASE","release",release_workstation,pass_user_data=True)

manage_workstations_conversation.add_command_to_state("BACK_OR_REQUEST","back",start_workstations,pass_user_data=True)
manage_workstations_conversation.add_command_to_state("BACK_OR_REQUEST","request",request_workstation,pass_user_data=True)

manage_workstations_conversation.add_command_to_state("BACK","back",start_workstations,pass_user_data=True)

manage_workstations_conversation.add_message_to_state("RELEASING_WORKSTATION",releasing_workstation,pass_user_data=True)

manage_workstations_conversation.add_message_to_state("REQUESTING_WORKSTATION",requesting_workstation,pass_user_data=True)

manage_workstations_conversation.add_command_to_fallback("back",start_workstations,pass_user_data=True)
manage_workstations_conversation.add_command_to_fallback("done",done)

workstations_blueprint.add_conversation(manage_workstations_conversation)