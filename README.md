# gluware-rest-api-demo

Demonstrates usage of Gluware's REST API

**REQUIRED PYTHON VERSION: 3.x** 
Supports Gluware REST API v1

Python modules that must be available are: requests, urllib3, and Menu
To install these modules run pip in your environment:
 - pip install requests 
 - pip install urllib3 
 - pip install Menu

This file and gluware_device_rest_api_client.py must be in the same directory or in sys.path 
Usage: *python GluwareDeviceAPIDemo.py*

This demo uses a set of basic text menus to demonstrate various calls to the Gluware Device REST API. There are 3 primary submenus: Connection Info, Organizations, and Devices.

NOTE: Connection information must be supplied in order to use any of the Organization or Device calls.

Required Connection Info: Gluware Control username and password and the Gluware Control hostname or IP.
Once the connection information is set it will be automatically used by the demo for each call to the REST API.

Demo example flow:
1.  Run the demo from the command line or using a python IDE of your choice
2.  Select the Connection Info option from the main menu and enter your Gluware Control credentials and ip/hostname
3.  Enter the Organizations sub menu by selected the Organizations option in the main menu
4.  List all of the Organization in your Gluware Control system by choosing the List Organizations option from the Organizations sub menu. Highlight and copy one of the organization IDs for use in subsequent steps
5.  Close the Organizaton sub menu by selecting the Close Organizations sub menu option to return to the main menu
6.  Select the Devices option from the main menu
7.  Select the "Retrieve Devices By Org ID" option from the Devices sub menu and enter the Organization ID from step 4
8.  To create a new device select the "Create Discoverable Device" option from the Devices menu
9.  Enter the Device Name, Organization ID from step 4, Device Connection Info (IP Address, Username, Password, Enable Password (if needed), Connection Type and Port. Highlight and copy the ID value for the newly created device
10.  Select the Update Device By ID option from the Devices sub menu
11.  Enter the Device ID from Step 9
12.  Enter a device element name to update such as "description"
13.  Enter the new value for the element name selected in step 12
14.  Select the Discover Device option from the Devices sub menu
15.  Enter the Device ID from Step 9. This will kick off device discovery. If you repeat the next step quickly you can see the discovery status value change.
16.  Select the Retrieve Device By ID from the Devices sub element
17.  Enter the Device ID from Step 9. Note the discovery status value as well as the value of whatever element name you selected in steps 11 and 12
18.  Select the Delete Device By ID option from the Devices sub menu
19.  Enter the Device ID from Step 9
20.  Select the Retrieve Device By ID option from the Devices sub menu
21.  Enter the Device ID from Step 9 and note that the response code indicates the resource is not found since it was deleted in steps 18 and 19
22.  Select the Close Devices Sub Menu option from the Devices sub menu
23.  Select the Quit option from the main menu to exit the demo

*** Information regarding gluware_device_rest_api_client.py ***

This class provides convenience methods for the Gluware Device REST API. The requests and urllib3 modules are used to simplify communication with the HTTP server, to handle the creation and processing of HTTP requests and responses, and to make use of session concepts to reduce the need for specifying auth params, etc., with each operation. This class is provided only for illustrative purposes and to support the demo utility.

Details for the Gluware REST API calls used below, including error responses, may be found at: 
https://[your gluware control host or ip]/api-docs/ 

The available convenience methods encapsulating the Gluware REST API calls are: 

**DEVICE OPERATIONS** 
*get_devices* - Returns all devices matching query query details. Query details are json formatted key/value pairs for device attributes. To get all devices pass None as the payload value. 
Example query detail value: 
'{"orgId": "565a65db-54e7-4461-a954-f0f38f310e19"}' 
GET https:///api/devices?<key/value pairs from query details>

*get_device* - Returns a single device matching the device_id parameter value 
GET https:///api/devices/74caf003-0b1d-4c03-a166-1dce207b3ad5

*create_device* - Creates a new device with details passed in device_details parameter. Required parameters are name and orgId. 
POST https:///api/devices 
Example POST payload: 
'{"name":"My First Device", "orgId": "565a65db-54e7-4461-a954-f0f38f310e19"}'

*update_device* - Updates attributes of an existing device specified by the device id. Values to be updated should be provided in the device_details parameter in the form of json key/value pairs 
PUT https:///api/devices/74caf003-0b1d-4c03-a166-1dce207b3ad5 
Example device detail value: 
'{"name": "My updated device name"}'

*discover_devices* - Triggers device discovery on all devices provided in the device details parameter Device details should be a json object consisting of a "devices" array listing the device ids to be discovered. Response is either a "starting" message or an error. 
POST https:///api/devices/discover 
Example discover payload: 
'{"devices": ["74caf003-0b1d-4c03-a166-1dce207b3ad5", "54d4d631-d828-48e1-9482-5f5582c86f6e"]}

*delete_device* - Deletes an existing device specified by the device id. 
DELETE https:///api/devices/54d4d631-d828-48e1-9482-5f5582c86f6e

**ORGANIZATION OPERATIONS**

*get_organizations* - Retrieves all organizations on the Gluware host 
GET https:///api/organizations

*get_organization* - Retrieves a specific organization specified by the organization id parameter value 
GET https:///api/organizations/565a65db-54e7-4461-a954-f0f38f310e19

*get_organization_id_by_name* - Convenience method that retrieves an organization by name instead of id. Both the org name and the name of it's parent org are required in order to differentiate between two organizations on a system that have the same name but different parents such as: GluwareSystemOrganization/Lab/US and GluwareSystemOrganization/Production/US. 

This method simply requests all organizations and returns only the single organization matching both the parent name and the org name. 

GET https:///api/organizations, but with response parsing to drop all non-matching orgs
