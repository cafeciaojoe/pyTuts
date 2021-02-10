A = None
B = None

if A:
    print('A is not a thing it is None')

A = 1
if A:
    print('A is now a thing, it is 1')

print('A is not None... {}. Because A is None '.format(A is not None))
print('A is not None... {}. Because B is None '.format(B is not None))

"""
the line below is like saying:

A = (B is not None)
"""
A = B is not None

print('A is not None... {}. Because A was set to "B is not None" which is a boolean of False'.format(A is not None))
print(A)


