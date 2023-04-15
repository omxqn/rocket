import random

list_1 = []
list_non = []
list_dob = []
for i in range(10):
    list_1.append(random.randint(1,50))

for num in list_1:
    if list_1.count(num) > 1:
        if num not in list_dob:
            list_dob.append(num)
    else:
        list_non.append(num)
print(list_1,list_non,list_dob)


