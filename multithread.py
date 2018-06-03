## multithread.py ##############################################################
## testing out pythons multithread module ######################################
################################################################################
##from multiprocessing.dummy import Pool as ThreadPool 

import threading
import time

from random import shuffle


def getPrimesBetween(checkRange):
	primesList = []
	
	start = checkRange["start"]
	finish = checkRange["finish"]	
	
	for p in range(start, finish):
		for i in range(2, p):
			if p % i == 0:
				break
		else:
			primesList.append(p)
	return primesList

class ThreadWithReturnValue(threading.Thread):
	def __init__(self, group=None, target=None, name=None,
		args=(), kwargs={}, Verbose=None):
		threading.Thread.__init__(self, group, target, name, args, kwargs, Verbose)
		self._return = None
	def run(self):
		if self._Thread__target is not None:
			self._return = self._Thread__target(*self._Thread__args, **self._Thread__kwargs)
	def join(self):
		threading.Thread.join(self)
		return self._return




		
		

if(__name__ == "__main__"):
	##pool = ThreadPool(4) 
	##results = pool.map(getPrimesBetween, [{"start": 2, "finish": 8000}, {"start": 8001, "finish": 16000}, {"start": 16001, "finish": 24000}])
	
	##pool.close() 
	##pool.join() 
	##print "Started prime searching pool"
	##print len(getPrimesBetween(2, 80000))

	# do some stuff
	##download_thread = threading.Thread(target=getPrimesBetween, args=({"start": 2, "finish": 16000},))
	##download_thread.start()
    
	results = []
    
	primeSearchRanges = []
    
	startValue = 2
	for i in range(10):
		primeSearchRanges.append({"start": startValue, "finish": startValue+2499})
		startValue +=2500
    
	pendingThreads = []
	
	for searchRange in primeSearchRanges:
		pendingThreads.append(ThreadWithReturnValue(target=getPrimesBetween, args=(searchRange,)) )
    
	shuffle(pendingThreads)
    
	totalThreadCount = len(pendingThreads)
    
	##primeCalcThread = ThreadWithReturnValue(target=getPrimesBetween, args=({"start": 2, "finish": 26000},))
	# continue doing stuff
	
	
	
	##primeCalcThread.start()
	print "waiting for primes to finish calculating"
	
	activeThreads = []
	finishedThreads = []
	
	while(True):
		if(len(activeThreads) < 2):
			if(pendingThreads != []):
				activeThreads.append(pendingThreads.pop())
				activeThreads[-1].start()
		
		for thread in activeThreads:
			if(not thread.isAlive()):
				results.append(thread.join())
				finishedThreads.append( activeThreads.pop(activeThreads.index(thread)) )
		
		print len(results)
		if(len(finishedThreads) == totalThreadCount):
			break
	
	print results	
    ##print primeCalcThread.join()


