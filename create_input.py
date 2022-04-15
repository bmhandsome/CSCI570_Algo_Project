f = open("../datapoints/in3.txt", "r")

raw1 = []
raw2 = []
i = 0

for x in f:
    if i==0:
        raw1.append(x.strip())
        i+=1
    elif i==1:
        try:
            raw1.append(int(x.strip()))
        except:
            raw2.append(x.strip())
            i+=1
    else:
        raw2.append(int(x.strip()))


def CookingRaw(raw):
    meal = raw[0]
    for i in range(1, len(meal) + 1):
        meal = meal[:raw[i] + 1] + meal + meal[raw[i] + 1:]

    return meal

cooked1 = CookingRaw(raw1)
cooked2 = CookingRaw(raw2)
