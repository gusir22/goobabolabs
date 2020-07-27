#!/usr/bin/env python3

import scapy.all as scapy
import optparse

def create_optparse():
    '''Retrieves arguments from optparse'''
    parser = optparse.OptionParser()
    parser.add_option('-t', '--target', dest='target', help='IP range you want to target for scan')
    (options, arguments) = parser.parse_args()
    return options

def scan(ip):
    '''Scans for IP addresses'''
    #scan network
    arp_request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst = 'ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    #parses results into a list of dictionaries
    clients_list = []
    for element in answered_list:
        clients_dict = {'ip': element[1].psrc, 'mac': element[1].hwsrc}
        clients_list.append(clients_dict)

    return clients_list

def print_result(results_list):
    '''Prints the result from the scan'''
    print("   IP\t\t\t   MAC Address\n------------------------------------------")
    for client in results_list:
        print(f'{client["ip"]}\t\t{client["mac"]}')

#body
options = create_optparse()
if options.target:
    ip = options.target
else:
    ip = "10.0.2.1/24"
results_list = scan(ip)
print_result(results_list)