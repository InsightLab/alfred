import pandas as pd

class Helper():
	df = pd.read_csv("data/users.csv")
	admins_id = df[df['type']==1]['id'].values
	users_id = df[df['type']>-1]['id'].values

	@staticmethod
	def reload_data():
		Helper.df = pd.read_csv("data/users.csv")
		Helper.admins_id = Helper.df[Helper.df['type']==1]['id'].values
		Helper.users_id = Helper.df[Helper.df['type']>-1]['id'].values

	@staticmethod
	def is_adm(id):
		Helper.reload_data()
		return id in Helper.admins_id

	@staticmethod
	def is_user(id):
		Helper.reload_data()
		return id in Helper.users_id

	@staticmethod
	def notify_admins(bot,text):
		Helper.reload_data()
		for id in Helper.admins_id:
			print("Sending to {}".format(id))
			bot.sendMessage(text=text,chat_id=str(id))