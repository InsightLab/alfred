from BotMother.Blueprint import Blueprint
from .helper import Helper
import re
from datetime import datetime as dt

#/clean
def clean(bot,update):
	user_id = update.message.from_user.id
	if not Helper.is_user(user_id):
		update.message.reply_text("You are not a member of Insight Data Science Lab. Access denied")
		return Conversation.END

	if update.message.reply_to_message is None:
		update.message.reply_text("Por favor, envie este comando como resposta para uma mensagem com a flag [clean]")
		return
	
	msg = update.message.reply_to_message.text

	#message pattern: [clean][cafeteira]
	tags = re.findall(r'\[(.*?)\]',msg)

	if len(tags)>1 and tags[0].lower()=="clean":
		obj = tags[1]
		user = update.message.from_user

		text = "Obrigado {}.\nManutenção registrada!\n".format(user.username, obj)
		
		with open("{}_cleaning_history.txt".format(obj), 'a') as f:
			f.write("{},{}\n".format(dt.now(),user.username))

		update.message.reply_text(text)
	else:
		update.message.reply_text("Por favor, envie este comando como resposta para uma mensagem com a flag [clean]")

clean_blueprint = Blueprint()

clean_blueprint.add_command_handler("clean",clean)