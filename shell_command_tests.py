
"""
This was made outdated by  decoded_bytelist.py

This was a first iteration at getting a list of NICs with an ipv4 address. All of it came back as a byte string.

"""


import subprocess

# run a basic command:
# didnt work it just outputs and I could not save to a variable.
# ipinfo = os.system("ipconfig /all")
# print(ipinfo)
# os.system('ipconfig | findstr /i "ipv4"')


def get_adapters():
    """
    gets the network adapter names. returns them in a dictionary.

    :return: dictionary with key pair entries {# : [<NIC Name>, <IPv4 address>], ...}
    """
    # output a basic command to a variable
    output = subprocess.check_output("ipconfig /all", shell=True)
    #print(output)

    # makes it into a list
    for item in output:
        #                        b is required here for a "bytes" output.
       new_output = output.split(b"\r\n")


    #print(new_output)

    # get adapter names, and IP names into a list.
    adapters = []
    count = 0
    for item in new_output:
        if b"Description" in item:
            adapters.append(count)
            adapters.append(item[39:])
            count += 1
        if b"IPv4 Address" in item:
            adapters.append(item[39:])


    # put the network adapters in a numbered dictionary.
    adapter_dict = {}
    for num, item in enumerate(adapters):
        #print(num)
        if type(item) == int:
            adapter_dict[item] = [adapters[num + 1]]
            if num + 2 in range(len(adapters)):
                adapter_dict[item].append(adapters[num + 2])

    return adapter_dict

list = get_adapters()

print(list)
print(len(list))

# a more concise list of NIC adapters in a numbered dictionary.
for item in list:
     print(f"{item} {list[item]}")



