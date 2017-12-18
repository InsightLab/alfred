from alfredbot.models.User import User
from alfredbot.controllers.User import UserController
u = User()
u.id = 1
u.first_name = "Joana"
u.username = "joaninha"

u.save()

controller = UserController()

print(User().get_all())