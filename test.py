list = [1,1,1,1,1,1,1,1,1,1]

for i in range(len(list) - 1):
    if list[i] == list[i + 1]:
        print('Repeated')