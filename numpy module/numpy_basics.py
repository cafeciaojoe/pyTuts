# https://numpy.org/doc/stable/user/absolute_beginners.html

import numpy as np

"One way we can initialize NumPy arrays is from Python lists, using nested lists for two- or higher-dimensional data."
a = np.array([1, 2, 3, 4, 5, 6])

"We can access the elements in the array using square brackets. When you’re accessing elements, " \
"remember that indexing in NumPy starts at 0. That means that if you want to access the first element " \
"in your array, you’ll be accessing element “0”."
print(a[0])
print(a[0:3])