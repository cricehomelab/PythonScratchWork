"""

trying to combine the info i've gathered from decoded_bytelist.py and nic_machine_names.py to form a table
with a NIC number, a nic name and a machine name.

"""

import subprocess


def get_nic_info():
    """
    gets a list of NIC names both the readable name and the machine name and returns it.

    :return: non_byte_list - a list of nic names and their computer name.
    """
    nic_info = subprocess.check_output("WMIC nicconfig get description, SettingID", shell=True)
    # output.decode("utf-8")

    # print(nic_info)

    nic_list = []
    nic_list = nic_info.split(b"\r\r\n")

    # for item in nic_list:
    #     print(item)

    non_byte_list = []
    for item in nic_list:
        non_byte_list.append(item.decode("utf-8"))

    # for item in non_byte_list:
    #     print(item)

    return non_byte_list


def get_adapters():
    """
    gets the network adapter names. returns them in a dictionary.

    :return: dictionary with key pair entries {# : [<NIC Name>, <IPv4 address>], ...}
    """
    # output a basic command to a variable
    output = subprocess.check_output("ipconfig /all", shell=True)
    #output.decode("utf-8")
    # print(output)

    # makes it into a list
    for item in output:
        #                        b is required here for a "bytes" output.
        new_output = output.split(b"\r\n")

    # This decodes the byte strings to normal strings.
    decoded = []
    for items in new_output:
        decoded.append(items.decode("utf-8"))

    # get adapter names, and IP names into a list.
    adapters = []
    count = 1
    for item in decoded:
        if "Description" in item:
            adapters.append(count)
            adapters.append(item[39:])
            count += 1
        if "IPv4 Address" in item:
            adapters.append(item[39:])


    # put the network adapters in a numbered dictionary.
    adapter_dict = {}
    for num, item in enumerate(adapters):
        # print(num)
        if type(item) == int:
            adapter_dict[item] = [adapters[num + 1]]
            if num + 2 in range(len(adapters)):
                adapter_dict[item].append(adapters[num + 2])

    return adapter_dict

list_of_adapters = get_adapters()
list_of_nics = get_nic_info()

print(list_of_adapters)
print(list_of_nics)