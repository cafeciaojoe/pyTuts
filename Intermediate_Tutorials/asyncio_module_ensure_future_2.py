import asyncio
import time

async def myTask():
    time.sleep(1)
    print("processing")

async def myTaskGenerator():
    # the for loop below will create 5 coroutines based on the function myTask
    for i in range(5):
        asyncio.ensure_future(myTask())
    # penting is of type 'set' and will show all of the pending tasks.
    # https://www.w3schools.com/python/python_sets.asp#:~:text=%2C%20%22cherry%22%7D-,Set,is%20both%20unordered%20and%20unindexed.
    pending = asyncio.Task.all_tasks()
    print(type(pending))

loop = asyncio.get_event_loop()
loop.run_until_complete(myTaskGenerator())
print('tasks completed')
loop.close()