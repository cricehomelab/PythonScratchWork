lana = '0101010001020103010401050106010701080109010A010B010C010D010E'

def split(word):
    return [char for char in lana]

lana = split(lana)
# print(lana)
newstring = ''
holder = []
new_list = []
for num, item in enumerate(lana, 1):
    holder.append(item)
    if num % 2 == 0:
        new_list.append(holder)
        holder = []
lana = new_list
# print(lana)
del lana[0]
for num, item in enumerate(lana):
    if type(item) == list:
        lana[num] = str(item[0] + item[1])
        # print(item)
# print(lana)
lana = ",".join(lana)
# print(lana)
