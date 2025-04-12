import json
import sqlite3
import datetime
import requests

BASEURL = "https://cadataapi.state.gov/api/TravelAdvisories"

def loadDoSTravel(BASEURL):
    resp = requests.get(BASEURL, verify=False)
    dosRaw =  resp.text
    return dosRaw

def decodeTravel(dosRaw):
    jsonList = json.loads(dosRaw)
    advisories = []
    for key in jsonList:
        advisories.append(key["Title"]+'\n'+key["Updated"])
    return advisories

def splitTravelAdvisory(advisoryLine):
    elements = advisoryLine.split('\n')
    return elements

def dbInit():
    try:
        dbConn = sqlite3.connect('travel.db')
        cursor = dbConn.cursor()
        table = """ CREATE TABLE IF NOT EXISTS travel (
                    datetimeUpdated VARCHAR(25) NOT NULL,
                    datetimeAdded VARCHAR(25) NOT NULL,
                    advisory VARCHAR(128) NOT NULL
                    ); """
        cursor.execute(table)
    except sqlite3.Error as error:
        return error
    finally:
        if dbConn:
            return dbConn, cursor

def dbAddEntry(dbConn, cursor, advisory, timestamp, currentTime):
    try:
        query = """INSERT INTO travel
                    VALUES (
                    {},
                    {},
                    {}
                    );
                """.format(str(currentTime),str(timestamp),str(advisory))
        cursor.execute(query)
        dbConn.commit()
    except sqlite3.Error as error:
        return error

def sanityCheckQuery(dbConn, cursor):
    try:
        query = """SELECT advisory FROM travel WHERE advisory IS NOT NULL"""
        output = cursor.execute(query)
    except sqlite3.Error as error:
        return error
    finally:
        if dbConn:
            dbConn.commit()
            return output

def dateConvert():
    currentTime = datetime.datetime.now()
    currentTime = currentTime.strftime("%Y-%m-%dT%H:%M:%S-04:00")
    return str(currentTime)

if __name__ == '__main__':
    dbObjects = dbInit()
    advisoriesList = decodeTravel(dosRaw=loadDoSTravel(BASEURL=BASEURL))
    for i in advisoriesList:
        timestamp = splitTravelAdvisory(advisoryLine=i)[1]
        advisory = splitTravelAdvisory(advisoryLine=i)[0]
        dbAddEntry(dbConn=dbObjects[0],cursor=dbObjects[1],timestamp=timestamp, advisory=advisory, currentTime=dateConvert())
    checkContents = sanityCheckQuery(dbConn=dbObjects[0],cursor=dbObjects[1])
    for row in checkContents:
        print(row)


### Dummy change to re-test Grype