
import requests
import json
from authliboclc import wskey
from authliboclc import user

###################
#    Functions
###################

#General Functions
def parseConfigFile(fileName):
    """ Function that parses the configuration file
    """
    with open(fileName) as jsonFile:
        data = json.load(jsonFile)
    jsonFile.close()

    return data

#Requests Functions
def sendGetRequestToOCLC(url):
    """ Function builds a get request to OCLC's API
    """
    configData = parseConfigFile("config.json")

    #Assign variables
    key = configData["client_id"]
    secret = configData["client_secret"]
    principal_id = configData["principalID"]
    principal_idns = configData["principalIDNS"] 
    institution_id = configData["institutionId"]

    my_wskey = wskey.Wskey(
        key=key,
        secret=secret,
        options=None)

    my_user = user.User(
        authenticating_institution_id=institution_id,
        principal_id=principal_id,
        principal_idns=principal_idns)

    authorization_header = my_wskey.get_hmac_signature(
        method='GET',
        request_url=url,
        options={
            'user': my_user,
            'auth_params': None})

    my_request = requests.get(
        url=url,
        data=None,
        headers={'Authorization': authorization_header,
        "accept" : "application/atom+json",
        "Content-Type": "application/atom+json"})
    
    return my_request

def sendPutRequestToOCLC(url, bodyData):
    """ Function builds a put request to OCLC's API and send data
    """

    configData = parseConfigFile("config.json")

    #Assign variables
    key = configData["client_id"]
    secret = configData["client_secret"]
    principal_id = configData["principalID"]
    principal_idns = configData["principalIDNS"] 
    institution_id = configData["institutionId"]

    my_wskey = wskey.Wskey(
        key=key,
        secret=secret,
        options=None)

    my_user = user.User(
        authenticating_institution_id=institution_id,
        principal_id=principal_id,
        principal_idns=principal_idns)

    authorization_header = my_wskey.get_hmac_signature(
        method='PUT',
        request_url=url,
        options={
            'user': my_user,
            'auth_params': None})

    my_request = requests.put(
        url=url,
        data=bodyData,
        headers={'Authorization': authorization_header,
                "accept" : "application/atom+json",
                "Content-Type": "application/atom+json"})
    
    return my_request

#LHR Parsing and Editing functions
def updateLHR(requestContent, originalBarcode, note):
    """ Function that reads and update the LHR to add a public note
    """
    recordJson = json.loads(requestContent)
    holdingArray = recordJson["content"]["holding"]

    for item in holdingArray:
        barcode = item["pieceDesignation"][0]
        if barcode == originalBarcode:
            if item["note"] == []:
                item["note"].append({"value": note, "type": "PUBLIC"})
                print("Note added")
            else:
                if item["note"][0]["value"] != note:
                    item["note"].append({"value": note, "type": "PUBLIC"})
                    print("Another Note added")
                else:
                    print("Note already there")
                
    newLHR = json.dumps(recordJson)
    
    return newLHR

def searchByBarcode(requestContent):
    """ Function that 
    """
    recordJson = json.loads(requestContent)
    if "entries" in recordJson: 
        idUrl = recordJson["entries"][0]["content"]["id"]
        idInst = idUrl.split("https://circ.sd00.worldcat.org/LHR/")[1]
        id = idInst.split("?")[0]
    else:
        id = None
    return id


def retrieveLHRIdentifier(url, barcode):

    ##Build request URL
    search_request_url = url + "?q=barcode:" + barcode

    ##Read LHR and retrieve LHR (get request)
    my_request = sendGetRequestToOCLC(search_request_url)   

    LHRId = searchByBarcode(my_request.content)
    
    return LHRId


def addNoteToLHR(url, LHRIdentifier, barcode, note):

    ##Build request URL
    search_request_url = url + "/" + LHRIdentifier

    ##Read LHR and retrieve LHR (get request)
    my_request = sendGetRequestToOCLC(search_request_url)
    print(my_request.content)


    ##Build new LHR
    myNewLHR = updateLHR(my_request.content, barcode, note)

    ##Send new LHR back to OCLC (Put request)
    my_request = sendPutRequestToOCLC(search_request_url, myNewLHR) 
    print(barcode, my_request)
    print(my_request.content)  