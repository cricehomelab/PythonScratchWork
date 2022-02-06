"""

This is for gathering lana info from the registry, formatting it and matching it to an identified NIC

"""

import subprocess
from prettytable import PrettyTable


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
    # for item in only_nic:
    #     print(item)
    # print(f"only_nic: {only_nic}")

    for num, item in enumerate(only_nic):
        # print(f'num = {num} : item = {item}')
        item_holder = []

        for char in item:
            item_holder.append(char)
        if item_holder[0] == " ":
            del item_holder[0]
        item_holder = "".join(item_holder)
        # print(f'item holder ={item_holder}')
        del only_nic[num]
        only_nic.insert(num, item_holder)
    # print(f'removed spaces??? : {only_nic}')


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
            else:
                adapter_dict[item].append("NO IPv4")

    # print(f"adapter dict = {adapter_dict}")
    return adapter_dict


def one_nic_dict(adapters, nic):
    """
    one_nic_dict combines what was found in get_adapters() and format_nic_info(adapter_list) into a single dictionary
    and returns it

    :param adapters: dictionary of Numbered Keys starting at one and a list of NIC info ["english name", "IPv4"]
    :param nic: list of NIC information containing ["english name", "guid", ....]
    :return: dictionary of {numbered key (int): ["english name", "IPv4", "GUID"]
    """
    # print(adapters)
    for i in range(len(adapters)):
        # print(f"{i} adapters {adapters} ")
        # print(f"{adapters[i+1]}")
        # print(new_adapters[i + 1][0])
        for num, x in enumerate(nic):
            # print(f"x = {x}")
            if adapters[i + 1][0] in x:
                # print(f'should be a guid {new_nic_info[num + 1]}')
                adapters[i + 1].append(nic[num + 1])
    # print(f'end state of adpters {adapters}')
    return adapters


def display_nic_info(nic_dictionary):
    """
    displays nic info cleanly in the terminal.

    :param nic_dictionary: a dictionary of nic info from the one_nic_dict() function.
    :return: None
    """
    # TODO: this is only going to work in very specific scenarios. This will need to be completely re-worked, but since
    # it is currently not in use I am leaving it be.
    for item in nic_dictionary:
        if range(nic_dictionary[item] == 3):
            print(f'NIC {item} , {nic_dictionary[item][0]} , {nic_dictionary[item][1]} , {nic_dictionary[item][2]}')
        else:
            nic_dictionary[item].append(' n/a ')
            print(f'NIC {item} , {nic_dictionary[item][0]} , {nic_dictionary[item][1]} , {nic_dictionary[item][2]} ')


# next step is to read the lana bind and lana map registry values and add them to our final_dict display.
def get_nic_bindings():
    nic_binding = subprocess.check_output("reg query HKLM\\SYSTEM\\ControlSet001\\Services\\NetBIOS\\Linkage /v bind",
                                          shell=True)
    lana_map = subprocess.check_output("reg query HKLM\\SYSTEM\\ControlSet001\\Services\\NetBIOS\\Linkage /v LanaMap",
                                       shell=True)
    # decode_nic_binding = nic_binding.decode("utf-8")
    # decode_lana_map = nic_binding.decode("utf-8")

    # print(nic_binding)
    # print(lana_map)
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
    # print(binding_zero)
    binding_zero = binding_zero.split("\\")
    # print(f'1. {binding_list[0]}')
    #print(binding_zero)
    # del binding_list[0]
    del binding_zero[0]
    # print(f'2. {binding_list[0]}')
    binding_zero.insert(0, "\\")
    binding_zero = "".join(binding_zero)
    # print(binding_zero)
    # print(f'3. {binding_list[0]}')
    binding_list.insert(0, binding_zero)
    # print(f'4. {binding_list[0]}')

    for num, item in enumerate(binding_list):
        item = item.split("_")
        del item[0]
        binding_list[num] = item

    # for item in binding_list:
    #     print(item)

    # TODO: append the lana number to the binding_list
    # 1. Get the lana map.
    # Isolate the registry key down to just the lana map.
    lana_map = lana_map.split(b"\r\n")
    # print(lana_map)
    lana_map = lana_map[2]
    # print(lana_map)
    lana_map = lana_map.decode("utf-8")
    lana_map = lana_map.split("    ")
    # print(lana_map)
    lana_map = lana_map[3]
    lana_map = list(lana_map)
    # print(lana_map)
    holder = []
    lana_list = []
    for num, item in enumerate(lana_map, 1):
        holder.append(item)
        if num % 4 == 0:
            holder = "".join(holder)
            # print(holder)
            lana_list.append(holder)
            holder = []
            # print(f"holder = {holder}: num = {num}")
    # print(lana_list)
    lana_map = "".join(lana_map)
    # print(lana_map)
    # lana list holds the lana values like this '010#' where # is the lana position.
    # i want the lana_map so we can edit this later.
    # i want the lana list so we can parse that with the list we already have.
    # TODO: merge binding_list and lana_list
    for num, item in enumerate(lana_list):
        binding_list[num].append(item)
    return binding_list


def nic_list(adapters_dict, bindings):
    """
    nic_list(adapters_dict, bindings) - puts all the data together in an embedded list.

    :param adapters_dict: dictionary of adapters should come from the final_dict variable.
    :param bindings: embedded list of bindings should come from final_bindings variable.
    :return: embedded list of collated data from the 2 parameters.
    """
    for num, item in enumerate(bindings):
        # print(final_bindings[num][0])
        # adds n/a for ipv6.
        # TODO: might want to add the readable nic name later.
        if bindings[num][0] == "Tcpip6":
            # print("true")
            bindings[num].append("N/A")
            bindings[num].append("N/A")
        # add the readable nic name and IP address.
        else:
            # print('false')
            #looping through final_dict to get associated readable nic name and ipv4 address.
            # this will get the machine guids we need but not all of them will be associated with an IP address.
            # we need to sort these out and add 2 "N/A" fields to their list.
            # we also need to add the readable name and IP address to the ips that have this associated with it.
            # print(f'final_bindings[{num}][1] = {bindings[num][1]}')
            for items in adapters_dict:
                if adapters_dict[items][2] == bindings[num][1]:
                    # print('True')
                    bindings[num].append(adapters_dict[items][0])
                    bindings[num].append(adapters_dict[items][1])
                # currently somehow this entry is getting removed from final_bindings ['Tcpip', '{0592B33F-5CA6-4F46-88EC-3FA21B143809}', '0104'],
                # Not sure why.
    for num, item in enumerate(bindings):
        if len(item) == 3:
            bindings[num].append("N/A")
            bindings[num].append("N/A")
    return bindings


# display the data in a basic text table.
def nic_table(list):
    """
    Takes the data from the bindings_list embedded list and displays it as a table.

    :param list: this should come from the bindings_list variable. This is an embedded list.
    :return: None
    """
    table = PrettyTable()
    table.field_names= ["IpV4/IpV6", "GUID", "Lana Number", "Adapter", "IP Address"]
    for item in list:
        table.add_row(item)
    print(table)


# TODO: add functionality to be able to edit the registry values for nic.

def display_options():
    print("Current lana information:")
    getting_data = True
    while getting_data:
        new_adapters = get_adapters()
        new_nic_info = format_nic_info(get_nic_info())
        final_dict = one_nic_dict(new_adapters, new_nic_info)
        final_bindings = get_nic_bindings()
        bindings_list = nic_list(final_dict, final_bindings)
        print("type 'help' for a list of commands.")
        # gets user input and converts it to lowercase for easier parsing. 
        user_choice = input("input a command: ").lower()
        if user_choice == 'exit':
            print("Goodbye.")
            break
        elif user_choice == 'help':
            print("use one of the following options.")
            print("'exit': Will exit application.")
            print("'info': Displays current nic table.")
        # Displays lana table from the nic_table() function.
        elif user_choice == "info":
            nic_table(bindings_list)
        # Get user input on what values need changed.
        elif user_choice == "change":
            lana_change = []
            lana_change.append(input("which Lana Number would you like to change?: "))
            lana_change.append(input(f"which Lana Number would you like swap with {lana_change[0]}?: "))
            #TODO: make sure lana_change[0] and lana_change[1] are correct.
            change_lana(user_choice)
        else:
            print("that is not a valid command, type 'help' for a list of commands.")
# TODO: Change the lana map
def change_lana(input):
    print(f"changing lana {input[0]}, and lana {input[1]}.")
    # TODO: send command to change the lanamap in the registry.
    # TODO: backup current registry fields for lana
    # TODO: extract registry key
    # TODO: format registry changes
    # TODO: apply registry settings

# new_adapters = get_adapters()
# new_nic_info = format_nic_info(get_nic_info())
# final_dict = one_nic_dict(new_adapters, new_nic_info)
# final_bindings = get_nic_bindings()
# bindings_list = nic_list(final_dict, final_bindings)

display_options()
# display_options(bindings_list)




