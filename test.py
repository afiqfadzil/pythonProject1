with open("calculation.txt", mode="r") as myfile:
    data = myfile.read()
    a = data.split(",")
    print(a)
    c= [float(e)for e in a]
    print(c)
    a,b = c
    print(a)
    print(b)


