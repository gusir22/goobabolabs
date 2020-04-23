#!/usr/bin/env python

import subprocess, optparse, re

def create_parser():
    '''create parser args and returns the args'''
    #create object
    parser = optparse.OptionParser()

    #create parser args. -h | --help is included by default
    parser.add_option("-i", "--interface", dest="interface", help="Pick interface to change")
    parser.add_option("-m", "--mac", dest="requested_mac", help="Set new MAC")

    #returns args
    return parser.parse_args()

def version_init():
    '''check if parser args were given. Initiate the version requested by user'''
    #init parser
    (options, arguments) = create_parser()

    #check if parser args given
    if options.interface and options.requested_mac:
        parser_version(options.interface, options.requested_mac)
    else:
        command_version()

def parser_version(interface, requested_mac):
    '''run parser version'''
    #change MAC
    change_mac(interface, requested_mac)

def command_version():
    '''run command version'''
    #show user the available networks
    print('\n\n')
    subprocess.call(['ifconfig'])

    #set up validation flag, start validation loop
    validation_flag = True
    while validation_flag:
        #ask for targets
        interface = input("\n\nWhat network do you want to target?\t")
        requested_mac = input("\nType new MAC address:\t")

        #look for MAC patterns in requested_mac input
        validation_regex = re.compile(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w')
        match_flag = validation_regex.findall(requested_mac)

        #check for match
        if match_flag:
            #move on
            validation_flag = False
        else:
            #request input again
            print(f'''\n'{requested_mac}' is not a valid MAC address. Try again..

                -------------------------------------''')

    #change MAC
    change_mac(interface, requested_mac)

def change_mac(interface, requested_mac):
    '''changes network MAC address'''
    #stores old mac
    old_mac = find_mac(interface)

    #runs linux terminal commands to change MAC
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', requested_mac])
    subprocess.call(['ifconfig', interface, 'up'])

    #stores new MAC
    new_mac = find_mac(interface)

    #checks if MAC has changed
    if old_mac != new_mac:
        message = f'''\n\t-----------------------------------------------------------
          MAC {old_mac} was changed to {requested_mac}!
        -----------------------------------------------------------\n'''
        print(message)
        subprocess.call(['ifconfig', interface])
    else:
        message = 'MAC address was NOT changed!'
        print(message)

def find_mac(interface):
    '''find the MAC address and return its value'''
    #store interface ifconfig details
    mess = subprocess.check_output(['ifconfig', interface])

    #convert to string
    mess = str(mess)

    #find MAC
    mac_regex = re.compile(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w')
    mac = mac_regex.search(mess)

    #return MAC
    return mac.group()


#body
version_init() 
