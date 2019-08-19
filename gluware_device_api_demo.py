# /* Copyright (C) 2019 Gluware - All Rights Reserved
# * This code is provided “as is” with no implied warranties or fitness
# * for a particular purpose. Gluware, Inc. is under no obligation to
# * provide maintenance, support, updates, enhancements or modifications.
# */

# REQUIRED PYTHON VERSION: 3.x
# Supports Gluware REST API v1
# Python modules that must be available are:
# requests, urllib3, and Menu.
# To install these modules run pip in your environment
# Ex.
#    pip install requests
#    pip install urllib3
#    pip install Menu
# This file and gluware_device_rest_api_client.py must be in the same directory or in sys.path
# Usage: python GluwareDeviceAPIDemo
#
# This demo uses a set of basic text menus to demonstrate various calls to the Gluware Device REST API
# There are 3 primary submenus: Connection Info, Organizations, and Devices
#
# NOTE: Connection information must be supplied in order to use any of the Organization or Device calls
# Connection info required: Gluware Control username and password and the Gluware Control hostname or IP
# Once the connection information is set it will be automatically used by the demo for each call to the REST API
#
# Demo example flow:
# 1. Run the demo from the command line or using a python IDE of your choice
# 2. Select the Connection Info option from the main menu and enter your Gluware Control credentials and ip/hostname
# 3. Enter the Organizations sub menu by selected the Organizations option in the main menu
# 4. List all of the Organization in your Gluware Control system by choosing the List Organizations option from the Organizations
#    sub menu. Highlight and copy one of the organization IDs for use in subsequent steps
# 5. Close the Organizaton sub menu by selecting the Close Organizations sub menu option to return to the main menu
# 6. Select the Devices option from the main menu
# 7. Select the "Retrieve Devices By Org ID" option from the Devices sub menu and enter the Organization ID from step 4
# 8. To create a new device select the "Create Discoverable Device" option from the Devices menu
# 9. Enter the Device Name, Organization ID from step 4, Device Connection Info (IP Address, Username, Password,
#    Enable Password (if needed), Connection Type and Port. Highlight and copy the ID value for the newly created device
# 10. Select the Update Device By ID option from the Devices sub menu
# 11. Enter the Device ID from Step 9
# 12. Enter a device element name to update such as "description"
# 13. Enter the new value for the element name selected in step 12
# 14. Select the Discover Device option from the Devices sub menu
# 15. Enter the Device ID from Step 9. This will kick off device discovery. If you repeat the next step quickly you can
#     see the discovery status value change.
# 16. Select the Retrieve Device By ID from the Devices sub element
# 17. Enter the Device ID from Step 9. Note the discovery status value as well as the value of whatever element name you
#     selected in steps 11 and 12
# 18. Select the Delete Device By ID option from the Devices sub menu
# 19. Enter the Device ID from Step 9
# 20. Select the Retrieve Device By ID option from the Devices sub menu
# 21. Enter the Device ID from Step 9 and note that the response code indicates the resource is not found since it was
#     deleted in steps 18 and 19
# 22. Select the Close Devices Sub Menu option from the Devices sub menu
# 23. Select the Quit option from the main menu to exit the demo


import gluware_device_rest_api_client
from menu import Menu
import pprint

def print_orgs():
    if connectionInfoIsSet():
        resp = client.get_organizations()
        if resp["response_code"] == 200:
            pprint.pprint(resp["response_content"])
        else:
            print("Error:")
            pprint.pprint(resp)
    input("Enter any key to return to menu: ")

def print_orgs_by_name():
    if connectionInfoIsSet():
        org_name = input("Enter Organization Name: ")
        resp = client.get_organization_id_by_name(org_name, "GluwareSystemOrganization")
        if resp["response_code"] == 200:
            pprint.pprint(resp["response_content"])
        else:
            print("Error:")
            pprint.pprint(resp)
    input("Enter any key to return to menu: ")

def print_sub_org_by_name():
    if connectionInfoIsSet():
        org_name = input("Enter Organization Name: ")
        parent_name = input("Enter Parent Organization Name: ")
        resp = client.get_organization_id_by_name(org_name, parent_name)
        if resp["response_code"] == 200:
            pprint.pprint(resp["response_content"])
        else:
            print("Error:")
            pprint.pprint(resp)
    input("Enter any key to return to menu: ")

def print_org_by_id():
    if connectionInfoIsSet():
        org_id = input("Enter Organization ID: ")
        resp = client.get_organization(org_id)
        if resp["response_code"] == 200:
            pprint.pprint(resp["response_content"])
        else:
            print("Error:")
            pprint.pprint(resp)
    input("Enter any key to return to menu: ")

def print_devices():
    if connectionInfoIsSet():
        resp = client.get_devices(None)
        if resp["response_code"] == 200:
            pprint.pprint(resp["response_content"])
        else:
            print("Error")
            pprint.pprint(resp)
    input("Enter any key to return to menu: ")

def print_devices_in_org_id():
    if connectionInfoIsSet():
        org_id = input("Enter Organization ID: ")
        payload = {"orgId": org_id}
        resp = client.get_devices(payload)
        if resp["response_code"] == 200:
            pprint.pprint(resp["response_content"])
        else:
            print("Error")
            pprint.pprint(resp)
    input("Enter any key to return to menu: ")

def print_device_by_id():
    if connectionInfoIsSet():
        dev_id = input("Enter Device ID: ")
        resp = client.get_device(dev_id)
        if resp["response_code"] == 200:
            pprint.pprint(resp["response_content"])
        else:
            print("Error")
            pprint.pprint(resp)
    input("Enter any key to return to menu: ")

def create_device():
    if connectionInfoIsSet():
        dev_name = input("Enter Device Name: ")
        org_id = input("Enter Organization ID: ")
        payload = '{"name":"' + dev_name + '", "orgId": "' + org_id + '"}'
        resp = client.create_device(payload)
        if resp["response_code"] == 200:
            pprint.pprint(resp["response_content"])
        else:
            print("Error")
            pprint.pprint(resp)
    input("Enter any key to return to menu: ")

def create_discoverable_device():
    if connectionInfoIsSet():
        dev_name = input("Enter Device Name: ")
        org_id = input("Enter Organization ID: ")
        device_ip_address = input("Enter Device IP Address: ")
        device_user_name = input("Enter Device Username: ")
        device_password = input("Enter Device Password: ")
        device_enable_password = input("Enter Enable Password (Press Enter if not used): ")
        device_connect_type = input("Enter Connection Type ('ssh' or 'telnet'): ")
        device_connect_port = input("Enter Connection Port (ssh = 22): ")
        connection_information = '"connectionInformation": {"ip": "'+ device_ip_address + '", "password": "' \
                                + device_password + '", "userName": "' + device_user_name + '", ' \
                                + '"type": "' + device_connect_type + '", "port": '+ device_connect_port + ', ' \
                                + '"enablePassword": "' + device_enable_password + '", "proxyList": []}'
        payload = '{"name":"' + dev_name + '", "orgId": "' + org_id + '", ' + connection_information + '}'
        resp = client.create_device(payload)
        if resp["response_code"] == 200:
            pprint.pprint(resp["response_content"])
        else:
            print("Error")
            pprint.pprint(resp)
    input("Enter any key to return to menu: ")

def delete_device():
    if connectionInfoIsSet():
        dev_id = input("Enter Device ID: ")
        resp = client.delete_device(dev_id)
        if resp["response_code"] == 200:
            print("Device deleted")
        else:
            print("Error")
            pprint.pprint(resp)
    input("Enter any key to return to menu: ")

def update_device():
    if connectionInfoIsSet():
        print("Common elements that can be updated are: name, orgId, description and custom field names")
        dev_id = input("Enter Device ID: ")
        element_name = input("Enter device element name to be updated: ")
        element_value = input("Enter value for device element: ")
        payload = '{"' + element_name + '": "' + element_value + '"}'
        resp = client.update_device(dev_id, payload)
        if resp["response_code"] == 200:
            pprint.pprint(resp["response_content"])
        else:
            print("Error")
            pprint.pprint(resp)
    input("Enter any key to return to menu: ")

def update_device_connection_info():
    if connectionInfoIsSet():
        dev_id = input("Enter Device ID: ")
        device_ip_address = input("Enter Device IP Address: ")
        device_user_name = input("Enter Device Username: ")
        device_password = input("Enter Device Password: ")
        device_enable_password = input("Enter Enable Password (Press Enter if not used): ")
        device_connect_type = input("Enter Connection Type ('ssh' or 'telnet'): ")
        device_connect_port = input("Enter Connection Port (ssh = 22): ")
        connection_information = '"connectionInformation": {"ip": "' + device_ip_address + '", "password": "' \
                                 + device_password + '", "userName": "' + device_user_name + '", ' \
                                 + '"type": "' + device_connect_type + '", "port": ' + device_connect_port + ', ' \
                                 + '"enablePassword": "' + device_enable_password + '", "proxyList": []}'
        payload = '{' + connection_information + '}'
        resp = client.update_device(dev_id, payload)
        if resp["response_code"] == 200:
            pprint.pprint(resp["response_content"])
        else:
            print("Error")
            pprint.pprint(resp)
    input("Enter any key to return to menu: ")

def discover_device():
    if connectionInfoIsSet():
        dev_id = input("Enter Device ID: ")
        payload = '{"devices": ["' + dev_id + '"]}'
        resp = client.discover_devices(payload)
        if resp["response_code"] == 200:
            pprint.pprint(resp["response_content"])
        else:
            print("Error")
            pprint.pprint(resp)
    input("Enter any key to return to menu: ")

def set_connection_info():
    global gluware_username, gluware_password, gluware_host_name
    gluware_username = input("Enter username for connection: ")
    gluware_password = input("Enter password for connection: ")
    gluware_host_name = input("Enter hostname or IP for connection: ")
    global client
    client = gluware_device_rest_api_client.APIClient("https://" + gluware_host_name, gluware_username, gluware_password, gluware_org_name,
                                  None)
def connectionInfoIsSet():
    global gluware_username, gluware_password, gluware_host_name
    if (gluware_username == "" or gluware_password == "" or gluware_host_name == ""):
        print("Please set up Connection Information using the option in the root menu.")
        return False
    else:
        return True


gluware_org_name = ""
gluware_host_name = ""
gluware_username = ""
gluware_password = ""
client = gluware_device_rest_api_client.APIClient("https://" + gluware_host_name, gluware_username, gluware_password, \
                                                  gluware_org_name, None)
menu = Menu()
orgs = Menu(title = "Organizations")
devs = Menu(title = "Devices")
menu.set_options([("Set Connection Info", set_connection_info),("Organization", orgs.open), ("Devices", devs.open), \
                  ("Quit", menu.close)])
menu.set_title("Gluware API Demo")
orgs.set_options([("List All Organizations", print_orgs),("Retrieve Organization ID by Name", print_orgs_by_name), \
                  ("Retrieve SubOrganization ID By Name",print_sub_org_by_name), \
                  ("Retrieve Organization By ID", print_org_by_id), \
                  ("Close Organizations Sub Menu", orgs.close)])
devs.set_options([("List All Devices", print_devices),("List Devices By Org ID", print_devices_in_org_id), \
                  ("Retrieve Device By ID", print_device_by_id), ("Create Basic Device", create_device), \
                  ("Create Discoverable Device", create_discoverable_device), \
                  ("Discover Device", discover_device), ("Update Device by ID", update_device), \
                  ("Update Device Connection Information", update_device_connection_info), \
                  ("Delete Device by ID", delete_device), ("Close Devices Sub Menu", devs.close)])
menu.open()



