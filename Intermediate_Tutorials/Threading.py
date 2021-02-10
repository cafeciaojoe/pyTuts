"""
THREADING
https://www.youtube.com/watch?v=IEEhzQoKtQU

threading does not actually run code concurrently, it just gives the illusion of concurrency.
because when a pieces of code is waiting for an input, threading allows you to go and do something else.

io bound task : A task that is limited in time by the input or output of data such as
- openeing and closing files
- downloading somehting off the internet
- waiting for the user to do somehting
- waiting for a signal from another computer (or drone)

CPU bound task: a task limited in time by the speed at which the CPU can finish the task
- image processing
- file conversion
- 3D rendering.


"""

import time
import threading

start = time.perf_counter()

def do_something_1():
    print(f'Sleeping 1 second(s)...')
    time.sleep(1)
    print('done sleeping')

def do_something_3():
    print('Sleeping 3 seconds...')
    time.sleep(3)
    print('done sleeping')

t1 = None

# DO NOT EXECUTE THE TARGET
t1 = threading.Thread(target=do_something_1)
t2 = threading.Thread(target=do_something_3)

print(t1)

t1.start()
t2.start()

"""If you want the program to wait for the finish of a thread before moving on, use the join method """
t1.join()
t2.join()

print('something')

# threads = []
#
# """
# creating and starting 10 threads of the same function
# """
# for _ in range(10):
#     t = threading.Thread(target=do_something_1, args=[1.5])
#     t.start()
#     threads.append(t)
#
# """
# running the join method 10 times, one for each thread,
# not that this is done before all the threads finish.
# """
# for thread in threads:
#     thread.join()
#
# finish = time.perf_counter()
#
# print(F'Finished in {round(finish-start, 2)} second(s)')

