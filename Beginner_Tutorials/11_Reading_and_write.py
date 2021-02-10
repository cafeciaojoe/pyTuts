
"""
r is read
w is write
careful with mode 'w', if the file already exist you will OVERWRITE IT! it is better to append mode 'a'
a is append
r+ read and write
help(open) for more info
"""
"""this is a shitty way of opening file
because you have to remember to close the file """
# f = open('readme.txt', 'r')
# print(f.name)
# f.close()

"""take this function (or class) and assign it to (or make an instance in the name of) 'f'"""

with open('readme.txt', 'r') as f:
    """.read() chucks the whole line in the variabe"""
    # f_contents = f.read()
    """.readline() chucks a particular line into the variable"""
    # f_contents = f.readline()

    """we can iterate over the lines in a file by using"""
    # for line in f:
    #     print(line,end='')
    # pass

    """we can read through a file a number of characters at a
    time by creating a while loop"""
    size_to_read = 10
    f_contents = f.read(size_to_read)
    while len(f_contents) > 0:
        print(f_contents, end='*')
        f_contents = f.read(size_to_read)
        """f.tell() tells you where you are int he file """
        print(f.tell())
        """f.seek() puts you where you want to be in the file"""
        # f.seek(0)

    """why do ne need f_contents = f.read(size_to_read)
    why cant we perform all the operations on f?
    wel that's because f is a method from an instance of the class 
    TextIOWrapper included in python.
    we need to perform opertations on what gets returned from
    f.read() not on the method itself. 
    """
    print(type(f))
    print(type(size_to_read))


"""we can open two files and cope one over to the other usign the same for loop as above"""
with open('test.txt', 'r') as rf:
    with open('test_copy.txt', 'w') as wf:
        for line in rf:
            wf.write(line)
print('rf is of type,',type(rf))

"""if we are copying files that are not lines of a text 
then we need to use binary mode, add a b to the end of r and w """
# with open('pos 0 0 .png', 'rb') as rf:
#     with open('pos 0 0 _copy.png', 'wb') as wf:
#         for line in rf:
#             wf.write(line)

with open('pos 0 0 .png', 'rb') as rf:
    with open('pos 0 0 _copy.png', 'wb') as wf:
        chunk_size = 4096
        f_contents = rf.read(chunk_size)

        while len(f_contents) == 4096:
            wf.write(f_contents)
            f_contents = rf.read(chunk_size)

