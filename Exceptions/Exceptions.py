class BaseException(Exception):
	def __init__(self, m):
		self.message = m
	def __str__(self):
		return self.message


class NotCallableException(BaseException):
	pass

class NotAStringException(BaseException):
	pass

class NotABlueprintException(BaseException):
	pass

class NotABlueprint(BaseException):
	pass