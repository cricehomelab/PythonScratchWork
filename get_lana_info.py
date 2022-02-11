"""

This is for gathering lana info from the registry, formatting it and matching it to an identified NIC

"""
import os
import subprocess
import logging
from prettytable import PrettyTable
from datetime import date, datetime


# set up dates and times for logging.
def today_is():
    current_day = date.today()
    current_day = current_day.strftime("%Y%m%d")
    return current_day


def log_time():
    next_time = datetime.now()
    next_time = next_time.strftime("%Y%m%d %H:%M:%S.%f")
    return next_time

# declare what day it is.
day = today_is()


# set up logging to work.
logging.basicConfig(filename=f'{day}-lana-change.log', encoding='utf-8', filemode='w', level=logging.DEBUG)

def add_log(message, type):
    if type == "info":
        logging.info(f'{log_time()} : {message}')
    elif type == "debug":
        logging.debug(f'{log_time()} : {message}')
    elif type == "warning":
        logging.warning(f'{log_time()} : {message}')


def get_nic_info():
    """
    gets a list of NIC names both the readable name and the machine name and returns it.

    :return: non_byte_list - a list of nic names and their computer name.
    """
    add_log("getting NIC info", 'info')
    nic_info = subprocess.check_output("WMIC nicconfig get description, SettingID", shell=True)

    nic_list = nic_info.split(b"\r\r\n")

    non_byte_list = []
    for item in nic_list:
        non_byte_list.append(item.decode("utf-8"))
    return non_byte_list


def format_nic_info(adapter_list):
    add_log("formatting adapter information.", 'info')
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
        del only_nic[num]
        only_nic.insert(num, item_holder)
    return only_nic


def get_adapters():
    """
    gets the network adapter names. returns them in a dictionary.

    :return: dictionary with key pair entries {# : [<NIC Name>, <IPv4 address>], ...}
    """
    add_log('getting adapters with IP addresses', 'info')
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
    add_log('formatting adapters into a dictionary', 'info')
    # print(adapters)
    for i in range(len(adapters)):
        for num, x in enumerate(nic):
            if adapters[i + 1][0] in x:
                adapters[i + 1].append(nic[num + 1])
    return adapters


# next step is to read the lana bind and lana map registry values and add them to our final_dict display.
def get_nic_bindings():
    '''

    :return:
    '''
    add_log('getting Nic info from the registry.', 'info')
    nic_binding = subprocess.check_output("reg query HKLM\\SYSTEM\\ControlSet001\\Services\\NetBIOS\\Linkage /v bind",
                                          shell=True)
    lana_map = subprocess.check_output("reg query HKLM\\SYSTEM\\ControlSet001\\Services\\NetBIOS\\Linkage /v LanaMap",
                                       shell=True)

    # make lana_map readable and split the lana numbers into a list.
    # Format the NIC Binding Key.
    split_binding = nic_binding.split(b"\r\n")
    needed_bindings = split_binding[2]
    bindings_list_bits = needed_bindings.split(b"\\0")
    binding_list = []
    for item in bindings_list_bits:
        binding_list.append(item.decode("utf-8"))
    binding_zero = binding_list.pop(0)
    binding_zero = binding_zero.split("\\")
    del binding_zero[0]
    binding_zero.insert(0, "\\")
    binding_zero = "".join(binding_zero)
    binding_list.insert(0, binding_zero)

    for num, item in enumerate(binding_list):
        item = item.split("_")
        del item[0]
        binding_list[num] = item

    # append the lana number to the binding_list
    # 1. Get the lana map.
    # Isolate the registry key down to just the lana map.
    lana_map = lana_map.split(b"\r\n")
    lana_map = lana_map[2]
    lana_map = lana_map.decode("utf-8")
    lana_map = lana_map.split("    ")
    lana_map = lana_map[3]
    lana_map = list(lana_map)
    holder = []
    lana_list = []

    for num, item in enumerate(lana_map, 1):
        holder.append(item)
        if num % 4 == 0:
            holder = "".join(holder)
            lana_list.append(holder)
            holder = []
    lana_map = "".join(lana_map)
    # print(lana_map)
    # lana list holds the lana values like this '010#' where # is the lana position.
    # i want the lana_map so we can edit this later.
    # i want the lana list so we can parse that with the list we already have.
    # merge binding_list and lana_list
    for num, item in enumerate(lana_list):
        binding_list[num].append(item)
    return binding_list, lana_list


def nic_list(adapters_dict, bindings):
    """
    nic_list(adapters_dict, bindings) - puts all the data together in an embedded list.

    :param adapters_dict: dictionary of adapters should come from the final_dict variable.
    :param bindings: embedded list of bindings should come from final_bindings variable.
    :return: embedded list of collated data from the 2 parameters.
    """
    add_log('creating nested list for table.', 'info')
    for num, item in enumerate(bindings):
        # adds n/a for ipv6.
        # TODO: might want to add the readable nic name later.
        if bindings[num][0] == "Tcpip6":
            bindings[num].append("N/A")
            bindings[num].append("N/A")
        else:
            # looping through final_dict to get associated readable nic name and ipv4 address.
            # this will get the machine guids we need but not all of them will be associated with an IP address.
            # we need to sort these out and add 2 "N/A" fields to their list.
            # we also need to add the readable name and IP address to the ips that have this associated with it.
            for items in adapters_dict:
                if adapters_dict[items][2] == bindings[num][1]:
                    # print('True')
                    bindings[num].append(adapters_dict[items][0])
                    bindings[num].append(adapters_dict[items][1])
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
    add_log('creating table for nic information', 'info')
    table = PrettyTable()
    table.field_names= ["IpV4/IpV6", "GUID", "Lana Number", "Adapter", "IP Address"]
    for item in list:
        table.add_row(item)
    print(table)


# TODO: add functionality to be able to edit the registry values for nic.

def display_options():
    add_log('starting main loop', 'info')
    getting_data = True
    while getting_data:
        new_adapters = get_adapters()
        new_nic_info = format_nic_info(get_nic_info())
        final_dict = one_nic_dict(new_adapters, new_nic_info)
        bindings_and_map = []
        bindings_and_map = get_nic_bindings()
        final_bindings = bindings_and_map[0]
        lana_map = bindings_and_map[1]
        bindings_list = nic_list(final_dict, final_bindings)
        print("type 'help' for a list of commands.")
        # gets user input and converts it to lowercase for easier parsing.
        user_choice = input("input a command: ").lower()
        # TODO: add an option to restore backup configurations.
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
            #make sure lana_change[0] and lana_change[1] are generally correct.
            if len(lana_change[0]) == 4 and len(lana_change[1]) == 4:
                change_lana(lana_change, lana_map)
            else:
                print("invalid lana numbers.")
        else:
            print("that is not a valid command, type 'help' for a list of commands.")


def split(word):
    return [char for char in word]


# TODO: Change the lana map
def change_lana(input, lana):
    add_log(f'changing lana {input[0]}, with lana {input[1]}', 'info')
    print(input)
    print(f"changing lana {input[0]}, and lana {input[1]}.")
    directory = os.getcwd()
    # TODO: enable a way to make multiple backups.
    filepath = directory + "\\backup.reg"
    add_log(f"backing up reg key to {filepath}", "info")
    # export reg key as a backup.
    # TODO: Re-enable
    # subprocess.check_output(f"reg export HKLM\\SYSTEM\\ControlSet001\\Services\\NetBIOS\\Linkage {filepath}",
    #                                    shell=True)
    # TODO: should probably check to make sure they are valid changes
    print(lana)
    lana_num_1 =lana.index(input[0])
    lana_num_2 = lana.index(input[1])
    lana[lana_num_1] = input[1]
    lana[lana_num_2] = input[0]
    lana = "".join(lana)
    print(f'lana = {lana}')
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
    print(lana)
    # TODO: send command to change the lanamap in the registry.
    # THIS WILL DELETE A REGISTRY KEY MAKE SURE IT WORKS BEFORE RUNNING
    # ***************************************************************************************************************
    # subprocess.run("reg delete HKEY_LOCAL_MACHINE\\System\\ControlSet001\\Services\\NetBIOS\\Linkage /v LanaMap /f")
    # ***************************************************************************************************************
    line1 = "Windows Registry Editor Version 5.00 \n"
    line2 = "\n"
    line3 = "[HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Services\\NetBIOS\\Linkage] \n"
    line4 = '"LanaMap"=hex:01,00,01,01,01,02,01,03,01,04,01,05'
    linelist = [line1, line2, line3, line4]

    # creates and opens a file named regupdate.reg in the working directory
    file = open("regupdate.reg", "w")
    # adds the desired content to the .reg file.
    file.writelines(line1)
    file.writelines(line2)
    file.writelines(line3)
    file.writelines(line4)
    file.close()
    # THIS WILL IMPORT A REGISTRY KEY MAKE SURE IT WORKS BEFORE RUNNING
    # ********************************************************************************************************************
    # subprocess.run('reg import regupdate.reg')
    # subprocess.check_output('reg query HKEY_LOCAL_MACHINE\\System\\ControlSet001\\Services\\NetBIOS\\Linkage /v LanaMap')
    # ********************************************************************************************************************

# new_adapters = get_adapters()
# new_nic_info = format_nic_info(get_nic_info())
# final_dict = one_nic_dict(new_adapters, new_nic_info)
# final_bindings = get_nic_bindings()
# bindings_list = nic_list(final_dict, final_bindings)

display_options()
# display_options(bindings_list)

# TODO: Logging is available, and implemented. Need to be more granular with logging information.



