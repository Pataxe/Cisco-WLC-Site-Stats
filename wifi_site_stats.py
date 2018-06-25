# Python 3.6
# Made to run on Windows at command prompt
# the main function runs it all and calls the other functions
#Takes a site ID at the command line and returns the connection stats for all the MAC addresses connected to it

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
import argparse
import re

platform = 'cisco_wlc'

def main():
    net_connect = connect_to_host(host_ip)  # connect to host
    #get a list of APs matching the site ID
    ap_list = get_ap_list(net_connect, site_id)
    ap_chan_widths = get_width(net_connect, ap_list)
    print ('Use the channel widths on this chart to get the actual speed: http://mcsindex.com/')
    #print the channel widths
    for ap in ap_chan_widths:
        print (ap, ap_chan_widths[ap])
    client_list_a = get_client_list_a(net_connect, ap_list)
    client_list_b = get_client_list_b(net_connect, ap_list)
    #print the list of client info
    print("#####################         Clients on the 5ghz band:           #####################")
    for client in client_list_a:
        print('      ********** ' + client + '*' * 10)
        get_client_info(net_connect, client, 'a')
    print("#####################         Clients on the 2.4ghz band:           #####################")
    for client in client_list_b:
        print('      ********** ' + client + '*' * 10)
        get_client_info(net_connect, client, 'b')

def get_client_list_a(net_connect, ap_list):
    #initialize list for mac addresses
    mac_list = []
    #list of the radio bands (2.4 & 5)
    radio_list = ['a']
    #regex pattern for the mac
    mac_pattern = r'[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]'
    #loop through both radio types
    for band in radio_list:
        #loop through the AP list
        for ap in ap_list:
            c_command = 'sh client ap 802.11' + band + ' ' + ap
            raw_output = net_connect.send_command(c_command)
            output_lines = raw_output.split('\n')
            for line in output_lines:
                matched = re.match(mac_pattern, line)
                if matched:
                    matched_new = matched.group()
                    mac_list.append(matched_new)
    return mac_list

def get_client_list_b(net_connect, ap_list):
        #initialize list for mac addresses
        mac_list = []
        #list of the radio bands (2.4 & 5)
        radio_list = ['b']
        #regex pattern for the mac
        mac_pattern = r'[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]:[a-zA-Z0-9][a-zA-Z0-9]'
        #loop through both radio types
        for band in radio_list:
            #loop through the AP list
            for ap in ap_list:
                c_command = 'sh client ap 802.11' + band + ' ' + ap
                raw_output = net_connect.send_command(c_command)
                output_lines = raw_output.split('\n')
                for line in output_lines:
                    matched = re.match(mac_pattern, line)
                    if matched:
                        matched_new = matched.group()
                        mac_list.append(matched_new)
        return mac_list

def get_ap_list(net_connect, site_id):
    c_command = 'sh ap summary'
    raw_output = net_connect.send_command(c_command)
    output_list = []
    # extract the macs
    #break the output up into lines
    output_lines = raw_output.split('\n')
    for x in output_lines:
        line_split = x.split()
        if len(line_split) > 0:
            if site_id in line_split[0]:
                output_list.append(line_split[0])
    #return the list of matching APs for the site id
    return output_list

def get_client_info(net_connect, mac, band):
    cli_command = 'show client detail ' + mac #test command, need to make this variables
    raw_output = net_connect.send_command(cli_command)
    output_lines = raw_output.split('\n')
    #get the info we need, iterate through and look for the matching line_split
    for line in output_lines:
        if 'Current Rate' in line:
            print(line)
        elif 'Radio Signal Strength Indicator' in line:
            print(line)
        elif 'Signal to Noise Ratio' in line:
            print(line)

def get_width(net_connect, ap_list):
    ap_channel_widths = {}
    for ap in ap_list:
        cli_command = "show ap config 802.11a " + ap
        raw_output = net_connect.send_command(cli_command)
        output_lines = raw_output.split('\n')
        for line in output_lines:
            if 'Channel Width' in line:
                ap_channel_widths[ap] = line
                #print (ap_channel_widths)
    return ap_channel_widths

def connect_to_host(_ip):
    try:
        return ConnectHandler(device_type=platform, username=_username, ip=_ip, password=password)
    except(NetMikoTimeoutException):
        print (str(i) + ' is not reachable')
    except(NetMikoAuthenticationException):
        print (' Cannot connect . . . bad username or password')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This program will return the connection statistics of the site\'s currently associated clients')
    #requiredNamed = parser.add_argument_group('Required Named Arguments')
    #requiredNamed = parser.add_argument('-i', help='IP address of the WLC')
    parser.add_argument('-i',  required=True, help='IP address of the WLC')
    parser.add_argument('-s',   required=True, help='Site ID of the site to be checked')
    parser.add_argument('-u',  required=True, help='User name for the WLC')
    parser.add_argument('-p', required=True, help='Password for the WLC')
    args = parser.parse_args()
    _username = args.u #username from the command line
    password = args.p #password for the wlc
    site_id = args.s #site ID to be checked
    host_ip = args.i #ip address of the wlc
    main()
