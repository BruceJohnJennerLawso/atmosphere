## delet.py ####################################################################
## delet this object ###########################################################
################################################################################


class Foo(object):
	
	def __init__(self):
		self.bar = None

	def __enter__(self):
		if self.bar != 'open':
			print 'opening the bar'
			self.bar = 'open'
		return self # this is bound to the `as` part

	def close(self):
		if self.bar != 'closed':
			print 'closing the bar'
			self.bar = 'close'

	def __exit__(self, *err):
		self.close()


if __name__ == '__main__':
	with Foo() as foo:
		print foo, foo.bar
