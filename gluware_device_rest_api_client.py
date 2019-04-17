# /* Copyright (C) 2019 Gluware - All Rights Reserved
# * This code is provided “as is” with no implied warranties or fitness
# * for a particular purpose. Gluware, Inc. is under no obligation to
# * provide maintenance, support, updates, enhancements or modifications.
# */

# REQUIRED PYTHON VERSION: 3.x
# Supports Gluware REST API v1
# Required Python modules:
# requests, urllib3

# This class provides convenience methods for the Gluware Device REST API
# The requests and urllib3 modules are used to simplify communication with the HTTP server,
# to handle the creation and processing of HTTP requests and responses, and to make use of
# session concepts to reduce the need for specifying auth params, etc., with each operation
# This class is provided only for illustrative purposes and to support the demo utility.
#
# Details for the Gluware REST API calls used below, including error responses, may be found at:
# https://<your Gluware control host>/api-docs/
# The available convenience methods encapsulating the Gluware REST API calls are:
# DEVICE OPERATIONS
# get_devices - Returns all devices matching query query details. Query details are json formatted
#               key/value pairs for device attributes. To get all devices pass None as the payload value.
#               Example query detail value: '{"orgId": "565a65db-54e7-4461-a954-f0f38f310e19"}'
#               GET https://<Gluware host>/api/devices?<key/value pairs from query details>
# get_device - Returns a single device matching the device_id parameter value
#              GET https://<Gluware host>/api/devices/74caf003-0b1d-4c03-a166-1dce207b3ad5
# create_device - Creates a new device with details passed in device_details parameter. Required parameters are
#                 name and orgId.
#                 POST https://<Gluware host>/api/devices
#                 Example POST payload:
#                 '{"name":"My First Device", "orgId": "565a65db-54e7-4461-a954-f0f38f310e19"}'
# update_device - Updates attributes of an existing device specified by the device id. Values to be updated
#                 should be provided in the device_details parameter in the form of json key/value pairs
#                 PUT https://<Gluware host>/api/devices/74caf003-0b1d-4c03-a166-1dce207b3ad5
#                 Example device detail value:
#                 '{"name": "My updated device name"}'
# discover_devices - Triggers device discovery on all devices provided in the device details parameter
#                    Device details should be a json object consisting of a "devices" array listing the
#                    device ids to be discovered. Response is either a "starting" message or an error.
#                    POST https://<Gluware host>/api/devices/discover
#                    Example discover payload:
#                    '{"devices": ["74caf003-0b1d-4c03-a166-1dce207b3ad5", "54d4d631-d828-48e1-9482-5f5582c86f6e"]}
# delete_device - Deletes an existing device specified by the device id.
#                 DELETE https://<Gluware host>/api/devices/54d4d631-d828-48e1-9482-5f5582c86f6e
#
# ORGANIZATION OPERATIONS
# get_organizations - Retrieves all organizations on the Gluware host
#                     GET https://<Gluware host>/api/organizations
# get_organization - Retrieves a specific organization specified by the organization id parameter value
#                    GET https://<Gluware host>/api/organizations/565a65db-54e7-4461-a954-f0f38f310e19
# get_organization_id_by_name - Convenience method that retrieves an organization by name instead of id.
#                               Both the org name and the name of it's parent org are required in order to
#                               differentiate between two organizations on a system that have the same name but
#                               different parents such as:
#                               GluwareSystemOrganization/Lab/US and GluwareSystemOrganization/Production/US
#                               This method really requests all organizations and then returns just the single
#                               organization matching both the parent name and the org name
#                               GET GET https://<Gluware host>/api/organizations, but with response parsing
#                               to drop all non-matching orgs

import requests
import urllib3

class APIClient:

    def __init__(self, control_url,username, password, organization_name, certificate_file):
        # Set up the endpoint to be used by all requests: "https://<host>/api/devices/"
        self.control_url = control_url
        if not self.control_url.endswith('/'):
            self.control_url = self.control_url + '/'
        if not self.control_url.endswith('api/devices/'):
            self.control_url = self.control_url + 'api/devices/'
        # Used to set a default organization
        self.organization_name = organization_name
        # By default certificate validation is disabled and related warnings are hidden
        # This is for demo purposes only. Production environments should always use cert
        # validation as a best practice
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.session = requests.Session()
        self.session.verify = False
        # If certificate validation is enabled, the CA certificate file will be used to validate
        # the API endpoint if the host cert is not in the default trust store
        self.certificate_file = certificate_file
        if certificate_file is not None:
            self.session.verify = certificate_file
        # User name and password for the Gluware control UI. This is used to authenticate and authorize
        # all requests to the REST API
        self.session.auth = (username, password)
        # Sets up request pooling which is useful for multi threaded applications
        adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
        self.session.mount('https://', adapter)
        self.session.mount('http://', adapter)

    def get_devices(self, query_details):
        r = self.session.get(self.control_url[:-1],params=query_details)
        if r.status_code == 200:
            return {"response_code": r.status_code, "response_content": r.json()}
        else:
            return {"response_code": r.status_code, "response_content": r.text}

    def get_device(self, device_id):
        r = self.session.get(self.control_url + device_id)
        if r.status_code == 200:
            return {"response_code": r.status_code, "response_content": r.json()}
        else:
            return {"response_code": r.status_code, "response_content": r.text}

    def create_device(self, device_details):
        r = self.session.post(self.control_url[:-1],json=device_details)
        if r.status_code == 200:
            return {"response_code": r.status_code, "response_content": r.json()}
        else:
            return {"response_code": r.status_code, "response_content": r.text}

    def update_device(self, device_id, device_details):
        r = self.session.put(self.control_url + device_id, json=device_details)
        if r.status_code == 200:
            return {"response_code": r.status_code, "response_content": r.json()}
        else:
            return {"response_code": r.status_code, "response_content": r.text}

    def discover_devices(self, device_details):
        r = self.session.post(self.control_url + "discover", json=device_details)
        if r.status_code == 200:
            return {"response_code": r.status_code, "response_content": r.json()}
        else:
            return {"response_code": r.status_code, "response_content": r.text}

    def delete_device(self, device_id):
        r = self.session.delete(self.control_url + device_id)
        print(r.url)
        print(r.text)
        if r.status_code == 200:
            return {"response_code": r.status_code, "response_content": r.json()}
        else:
            return {"response_code": r.status_code, "response_content": r.text}

    def get_organizations(self):
        org_url = self.control_url[:-12] + "api/organizations"
        r = self.session.get(org_url)
        if r.status_code == 200:
            return {"response_code": r.status_code, "response_content": r.json()}
        else:
            return {"response_code": r.status_code, "response_content": r.text}

    def get_organization(self, organization_id):
        org_url = self.control_url[:-12] + "api/organizations"
        r = self.session.get(org_url + '/' + organization_id)
        if r.status_code == 200:
            return {"response_code": r.status_code, "response_content": r.json()}
        else:
            return {"response_code": r.status_code, "response_content": r.text}

    def get_organization_id_by_name(self, organization_name, parent_organization_name):
        org_url = self.control_url[:-12] + "api/organizations"
        r = self.session.get(org_url)
        if r.status_code == 200:
            for org in r.json():
                if org["name"] == organization_name and org["parentName"] == parent_organization_name:
                    return {"response_code": r.status_code, "response_content": org["id"]}
            return {"response_code": 404, "response_content": "Organization Not Found"}
        elif r.status_code == 200:
            return {"response_code": r.status_code, "response_content": r.json()}
        else:
            return {"response_code": r.status_code, "response_content": r.text}

