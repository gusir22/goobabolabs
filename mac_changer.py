#!/usr/bin/env python3

'''
Features:
    -Allow user to use inputs or optparse versions
    -Change MAC address
    -Confirm new MAC is different from current MAC
    -Confirm MAC has been changed
    -Reset to default MAC
'''

import subprocess
import optparse
import re

def change_mac(interface, new_mac, old_mac):
    '''Changes the mac address for a targeted interface'''
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])
    confirm_change(interface, new_mac, old_mac)

def old_mac(interface, new_mac):
    '''Retrieves and stores the old mac address'''
    #retrieves old MAC address
    ifconfig_result = subprocess.check_output(['ifconfig', interface])
    ifconfig_result = str(ifconfig_result)
    old_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    old_mac = old_mac.group(0)

    #validates for a new unique MAC address
    while new_mac == old_mac:
        message = f'\nThat is the current MAC for {interface}. Please pick a different one..'
        print(message)
        new_mac = input('new mac> ')

    #confirms new MAC is valid and unique
    print(f'\n[+] New MAC for {interface} validated..')
    return (new_mac, old_mac)

def create_optparse():
    '''Retrieves arguments from optparse'''
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help='Interface you want to change the MAC address')
    parser.add_option('-m', '--mac', dest='new_mac', help='The new MAC address')
    parser.add_option('-r', '--reset', dest='reset', help='Enter interface to reset to default MAC address')
    (options, arguments) = parser.parse_args()
    return options

def init_version(options):
    '''Determines what version and command the user wants to use'''
    if not options.interface and not options.new_mac and not options.reset:
        #init input version

        #print commands list and ask for user input
        commands = '''
        -COMMANDS-
        Change MAC ("C")
        Reset Default MAC ("R")
        Quit ("Q")
        '''
        print(commands)
        command = input('Enter a command> ')

        #parse user commands
        if command.lower() == 'c':
            #proceed to change MAC
            subprocess.call(['ifconfig'])
            interface = input('interface> ')
            new_mac = input('new mac> ')
        elif command.lower() == 'r':
            #proceed to reset default mac
            macs = {'eth0': '08:00:27:59:fb:fa'}
            interface = input('interface> ')
            new_mac = macs[interface]
        elif command.lower() == 'q':
            #proceed to quit
            print('\n[+] Exiting program')
            exit()
    else:
        #init optparse version/ask for missing info

        if options.reset:
            #if reset activated
            macs = {'eth0': '08:00:27:59:fb:fa'}
            interface = options.reset
            new_mac = macs[interface]
        elif not options.interface and options.new_mac:
            #if missing interface
            interface = input('interface> ')
            new_mac = options.new_mac
        elif options.interface and not options.new_mac:
            #if missing new_mac
            interface = options.interface
            new_mac = input('new mac> ')
        else:
            #if complete info
            interface = options.interface
            new_mac = options.new_mac

    return (interface, new_mac)

def confirm_change(interface, new_mac, old_mac):
    '''Confirms that MAC has changed to requested address'''

    #retrieve the changed MAC
    ifconfig_result = subprocess.check_output(['ifconfig', interface])
    ifconfig_result = str(ifconfig_result)
    confirmed_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    confirmed_mac = confirmed_mac.group(0)

    #verify if changed MAC
    if new_mac == confirmed_mac:
        #if MAC changed to requested address
        print(f'\n[+] MAC address has been changed from {old_mac} to {new_mac}')
        subprocess.call(['ifconfig',interface])
    else:
        #if failed to change MAC
        print(f'\n[+] Failed to change MAC to {new_mac}')

        #ask user if they want to try again or quit
        retry = input('Enter "Y" to try again, "N" to exit> ')
        if retry.lower() == 'y':
            #try again
            change_mac(interface, new_mac)
        elif retry.lower() == 'n':
            #quit program
            exit()

#body
if __name__ == '__main__':
    options = create_optparse()
    (interface, new_mac) = init_version(options)
    (new_mac,old_mac) = old_mac(interface, new_mac)
    change_mac(interface, new_mac, old_mac)


