"""

This is for gathering lana info from the registry, formatting it and matching it to an identified NIC

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


def format_nic_info(adapter_list):
    adapter_list_2 = []
    for item in adapter_list:
        adapter_list_2.append(item.split("  "))
    raw_nic_info = []
    for num, item in enumerate(adapter_list_2):
        if item != " ":
            for items in item:
                if items == '':
                    pass
                else:
                    raw_nic_info.append(items)
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

    # makes it into a list
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


def display_nic_info(nic_dictionary):
    """
    displays nic info cleanly in the terminal

    :param nic_dictionary: a dictionary of nic info from the one_nic_dict() function.
    :return: None
    """
    for item in nic_dictionary:
        if range(nic_dictionary[item] == 3):
            print(f'NIC {item} , {nic_dictionary[item][0]} , {nic_dictionary[item][1]} , {nic_dictionary[item][2]}')
        else:
            nic_dictionary[item].append(' n/a ')
            print(f'NIC {item} , {nic_dictionary[item][0]} , {nic_dictionary[item][1]} , {nic_dictionary[item][2]} ')


final_dict = one_nic_dict(new_adapters, new_nic_info)
#print(final_dict)

display_nic_info(final_dict)


# TODO: next step is to read the lana bind and lana map registry values and add them to our final_dict display.
def get_nic_bindings():
    nic_binding = subprocess.check_output("reg query HKLM\\SYSTEM\\ControlSet001\\Services\\NetBIOS\\Linkage /v bind",
                                          shell=True)
    lana_map = subprocess.check_output("reg query HKLM\\SYSTEM\\ControlSet001\\Services\\NetBIOS\\Linkage /v LanaMap",
                                       shell=True)
    # decode_nic_binding = nic_binding.decode("utf-8")
    # decode_lana_map = nic_binding.decode("utf-8")

    # print(nic_binding)
    print(lana_map)
    # TODO: make lana_map readable and split the lana numbers into a list.

    # TODO: Format the NIC Binding Key.
    split_binding = nic_binding.split(b"\r\n")
    # print(split_binding[2])
    needed_bindings = split_binding[2]
    # print(needed_bindings)
    bindings_list_bits = needed_bindings.split(b"\\0")
    # print(bindings_list_bits)
    binding_list = []
    for item in bindings_list_bits:
        binding_list.append(item.decode("utf-8"))
        # print(item.decode("utf-8"))
    # print(binding_list)
    binding_zero = binding_list.pop(0)
    binding_zero = binding_zero.split("\\")
    # print(binding_zero)
    del binding_list[0]
    del binding_zero[0]
    binding_zero.insert(0, "\\")
    binding_zero = "".join(binding_zero)
    # print(binding_zero)
    binding_list.insert(0, binding_zero)
    # print(binding_list[0])
    # print(binding_list)
    # for item in binding_list:
    #     print(item)
    # This is almost usable now. We just need to separate out the machine GUIDs from the "\DeviceNetBT_Tcpip_" or the
    # \Device\NetBT_Tcpip6_ but we need to keep track of whether this is an ipv4 or ipv6.

    # trying with one entry.
    # bind = binding_list[0]
    # print(bind)
    # split_bind = bind.split("_")
    # print(split_bind)
    # del split_bind[0]
    # binding_list[0] = split_bind
    # print(binding_list[0])

    for num, item in enumerate(binding_list):
        item = item.split("_")
        del item[0]
        binding_list[num] = item

    for item in binding_list:
        print(item)

    # TODO: append the lana number to the binding_list






# TODO: add functionality to be able to edit the registry values for nic.
get_nic_bindings()
