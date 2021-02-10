import concurrent.futures
import time

start = time.perf_counter()

def do_something_1(secs):
    print(f'Sleeping {secs} second(s)...')
    time.sleep(secs)
    return 'done sleeping'

# make sure you execute the method in the context manager by using the parethesis.
with concurrent.futures.ThreadPoolExecutor() as executor:
    f1 = executor.submit(do_something_1, 1)
    print(f1.result())