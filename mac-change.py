import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")

    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")

    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify an interface")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac")

    return options


def change_mac(interface, new_mac):

    subprocess.call(["ifconfig", interface, "down"])

    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])

    subprocess.call(["ifconfig", interface, "up"])

    print(f"[+] Changing MAC address for {interface} to {str(new_mac)}")

# interface = options.interface
#
# new_mac = options.new_mac  # ether 1c:39:47:e3:36:2a

#
# print('opt', options, 'arg', 'arguments', 'opt new', options.new_mac)
# ifconfig_result.decode("utf-8")
# print(ifconfig_result.decode("utf-8"))


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(['ifconfig', interface])
    mac_address_search_result = re.search(r"(\w\w:){5}\w\w", ifconfig_result.decode("utf-8"))
    if mac_address_search_result:
        print(mac_address_search_result.group(0))
        return mac_address_search_result.group(0)
    else:
        print('Could not get MAC address')


options = get_arguments()
current_mac = get_current_mac(options.interface)
print(f'Current mac is {current_mac}')
change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print(f"[+] MAC address was successfully changed to {current_mac}.")
else:
    print("[-] MAC address did not get changed.")
