from BotMother.BotConstructor import BotConstructor

from alfredbot.blueprints.users_blueprint import users_blueprint

from os import environ

token = environ.get("BOT_ALFRED_TOKEN")

bot = BotConstructor(token=token)

bot.add_blueprint(users_blueprint)

bot.start()

bot.idle()