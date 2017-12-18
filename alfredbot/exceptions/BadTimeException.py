class BadTimeException(Exception):
	"""raise an exception of conflitant schedules"""

	def __init__(self, m):
		self.message = m
	def __str__(self):
		return self.message