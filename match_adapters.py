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

# print(get_nic_info())

def format_nic_info(adapter_list):
    # print(adapter_list)
    # for item in adapter_list:
        # print(item)
    adapter_list_2 = []
    for item in adapter_list:
        adapter_list_2.append(item.split("  "))
    # print(adapter_list_2)
    raw_nic_info= []
    for num, item in enumerate(adapter_list_2):
        if item != " ":
            for items in item:
                #print(items)
                if items == '':
                    pass
                else:
                    raw_nic_info.append(items)
    #print(f'raw nic info: {raw_nic_info}')
    #return raw_nic_info
    only_nic = []

    for number, item in enumerate(raw_nic_info):
        # print(item)
        if item == ' ':
            pass
        elif item == "Description":
            pass
        elif item == " SettingID":
            pass
        else:
            only_nic.append(item)
    return only_nic





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


new_adapters = get_adapters()
new_nic_info = format_nic_info(get_nic_info())


def one_nic_dict(adapters, nic):
    """
    one_nic_dict combines what was found in get_adapters() and format_nic_info(adapter_list) into a single dictionary
    and returns it

    :param adapters: dictionary of Numbered Keys starting at one and a list of NIC info ["english name", "IPv4"]
    :param nic: list of NIC information containing ["english name", "guid", ....]
    :return: dictionary of {numbered key (int): ["english name", "IPv4", "GUID"]
    """
    for i in range(len(adapters)):
        # print(new_adapters[i + 1][0])
        for num, x in enumerate(nic):
            if adapters[i + 1][0] in x:
                # print(f'should be a guid {new_nic_info[num + 1]}')
                adapters[i + 1].append(nic[num + 1])
    return adapters

final_dict = one_nic_dict(new_adapters, new_nic_info)
#print(final_dict)

for item in final_dict:
    print(f'NIC {item} {final_dict[item]}')