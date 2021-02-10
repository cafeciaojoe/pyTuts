"""https://www.youtube.com/watch?v=L3RyxVOLjz8"""

"""Futures
Futures in asyncio are very much similar to the Future objects you would see within Python ThreadPoolExecutors or 
ProcessPoolExecutors and tt follows an almost identical implementation. Future objects are created with the intention 
that they will eventually be given a result some time in the future, hence the name. This is beneficial as it means 
that within your Python program you can go off and perform other tasks whilst you are waiting for your Future to 
return a result.

Thankfully working with Futures in asyncio is relatively easy thanks to the ensure_future() method which takes in a 
coroutine and returns the Future version of that coroutinep"""

import asyncio
import random

#you may also see it built this way
# @asyncio.coroutine
# def myCoroutine2():
#     print('my coroutine 2')

async def myCoroutine(id):
    process_time = random.randint(1,5)
    await asyncio.sleep(process_time)
    print("coroutine: {}, has successfully completed after {} seconds".format(id, process_time))

async def main():
    tasks = []
        # from the list of tasks created above, the for loop will start a coroutine with the id  being 1-10"""
    for i in range(10):
        # at this point create_task and unsure future, seem to be interchangeable
        # tasks.append(asyncio.create_task(myCoroutine(i)))
        tasks.append(asyncio.ensure_future(myCoroutine(i)))
        # using an asterix when calling a function, passes the whole iterable in as discrete arguments. """
    await asyncio.gather(*tasks)




loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
