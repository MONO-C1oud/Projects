import threading
import time

def testing():
	print("This line was executed by {}".format(threading.current_thread().name))
	time.sleep(2)

THREADS = []

for i in range(0,5):
	t = threading.Thread(target=testing)
	t.start()
	#t.join()
	THREADS.append(t)

print(THREADS)