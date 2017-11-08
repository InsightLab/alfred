"""
Module containing the exceptions signatures
"""

class BaseException(Exception):
	def __init__(self, m):
		self.message = m
	def __str__(self):
		return self.message

#exception used when a non callable object is passed
class NotCallableException(BaseException):
	pass

#exception used when a non string object is passed
class NotAStringException(BaseException):
	pass

#exception used when a non Blueprint object is passed
class NotABlueprintException(BaseException):
	pass

#exception used when a non Conversation object is passed
class NotAConversation(BaseException):
	pass

#exception used when a bot is not especified by the user
class BotNotDefined(BaseException):
	pass