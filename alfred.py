from BotMother.BotConstructor import BotConstructor

from alfredbot.blueprints.users_blueprint import users_blueprint
from alfredbot.blueprints.workstations_blueprint import workstations_blueprint

from os import environ

token = environ.get("BOT_ALFRED_TOKEN")

bot = BotConstructor(token=token)

bot.add_blueprint(users_blueprint)
bot.add_blueprint(workstations_blueprint)

bot.start()

bot.idle()