import requests
import json

baseUrl = "https://cadataapi.state.gov/api/TravelAdvisories" 

def loadDoSTravel(baseUrl):
    resp = requests.get(baseUrl, verify=False)
    dosRaw =  resp.text
    return(dosRaw)

def decodeTravel(raw):
    jsList = json.loads(raw)
    for key in jsList:
        print(key["Title"]+'\n'+key["Updated"])

if __name__ == '__main__': 
    decodeTravel(raw=loadDoSTravel(baseUrl=baseUrl))