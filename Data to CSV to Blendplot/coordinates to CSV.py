import json
import csv

def load_accepted_positions():
    #     https://stackoverflow.com/questions/36965507/writing-a-dictionary-to-a-text-file
    filename = 'Tim.json'

    with open(filename, 'r') as f:
        accepted_positions = json.loads(f.read())
        print('loaded %d position from save file' % (len(accepted_positions.keys())))
        'print(accepted_positions.keys())'
        'print(accepted_positions.items()'
    return accepted_positions

coord_dict = load_accepted_positions()

"x's are 0 and 3"
"y's are 1 and 4"
"z's are 2 and 5"

axes = ['x','y','z']
x=[]
y=[]
z=[]

for key, value in coord_dict.items():
    x.append(value[0])
    y.append(value[1])
    z.append(value[2])
    x.append(value[3])
    y.append(value[4])
    z.append(value[5])

"length of each list is 2x78 = 156"
"print(len(x))"

with open('Tim.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(axes)

    for i in range(len(x)):
        row = [x[i],y[i],z[i]]
        writer.writerow(row)

    print('plotted %d points to csv' % len(x))


