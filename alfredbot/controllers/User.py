from alfredbot.models.User import User

class UserController():
		

	def add_user(self,id,first_name,last_name,username,mail):
		#create an user model
		user = User({
			"id":id,
			"first_name":first_name,
			"last_name":last_name,
			"username":username,
			"mail":mail,
			"type":-1
		})

		#save in the database
		user.save()

		return user

	def get_users(self):
		return User().get_all()

	def remove_user(self,id):
		user = User({"id":id})
		user.remove()

	def validate_user(self,user_id):
		#load the user in the database
		user = User({"id":user_id})
		user.reload()
		
		#set as an active user
		if user["type"] == -1 :
			user["type"] = 0
			user.save()

		return user