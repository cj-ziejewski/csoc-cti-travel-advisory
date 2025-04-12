import requests
import json
import sqlite3
import datetime

baseUrl = "https://cadataapi.state.gov/api/TravelAdvisories" 

def loadDoSTravel(baseUrl):
    resp = requests.get(baseUrl, verify=False)
    dosRaw =  resp.text
    return dosRaw

def decodeTravel(dosRaw):
    jsonList = json.loads(dosRaw)
    advisories = []
    for key in jsonList:
        advisories.append(key["Title"]+'\n'+key["Updated"])
    return advisories

def splitTravelAdvisory(advisoryLine):
    advisory = []
    timestamp = []
    elements = advisoryLine.split('\n')
    advisory = elements[0]
    timestamp = elements[1]
    return advisory, timestamp

def dbInit():
    try:
        dbConn = sqlite3.connect('travel.db')
        cursor = dbConn.cursor()
        table = """ CREATE TABLE IF NOT EXISTS advisories (
                    datetimeUpdated VARCHAR(25) NOT NULL,
                    datetimeAdded VARCHAR(25) NOT NULL,
                    threatLevel VARCHAR(7) NOT NULL,
                    country VARCHAR(128) NOT NULL
                    ); """
        cursor.execute(table)
    except sqlite3.Error as error:
        return error
    finally:
        if dbConn:
            return cursor

def dateConvert():
    currentTime = datetime.datetime.now()
    currentTime = currentTime.strftime("%Y-%m-%dT%H:%M:%S-04:00")
    return(str(currentTime))
if __name__ == '__main__': 
    print(dateConvert())