nums = [1, 2, 3, 4, 555]

for num in nums:
    for numm in nums:
        print(numm)
        print('hi', num)
    # break
#
# for num in nums:
#     if num ==3:
#         print('found it')
#         print(num)
#         break
# """
# num is created when you use 'for num'
# """
# for num in nums:
#     if num == 3:
#         print('found')
#         """continue will skip to the next iteration of a loop
#         eg it will not finish this loop and print 'num'
#         """
#         continue
#     print(num)
#
# """num is redefined here stating at nums [0] which is 1 """
# for num in nums:
#     for letter in 'abc':
#         print(num, letter)

#"""range(start, stop, step)"""
# for i in range(10):
#     print(i)

# x = 0
#
# while True:
#     print(x)
#     x += 1

""""
when a class is usd ina  for loop, python calls the __iter__ and __next__ 
dunder methods. which return the class, and break the loop on some contiion
(respectively)
so you can do some operations with the all the cool methods from the class in a loop
while it checks on shome conditions for you. 

https://opensource.com/article/18/4/elegant-solutions-everyday-python-problems
"""


# class SyncLogger:
#     def __iter__(self):
#         return self
#
#     def __enter__(self):
#         if not True:
#             raise StopIteration
#
# with SyncLogger as logger:
#
#     for log_entry in logger:
#         print(type(logger))
#         print(type(log_entry))






