import unittest
import sqlite3
import json
import os
import requests

# Name: Bella Karduck
# Who did you work with: Claire Yang

"""def readDataFromFile(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    f = open(full_path)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
    return json_data"""

def getCounties():
    url = "https://api.census.gov/data/2019/acs/acs1/subject?get=NAME,S0101_C01_001E&for=county:*"
    r = requests.get(url)
    #x = r.text
    countyDict = r.json()
    
    countyList = []
    for x in countyDict[1:]:
        newCountyDict = {}
        newCountyDict["name"] = x[0]
        newCountyDict["stateFIP"] = x[2]
        newCountyDict["countyFIP"] = x[3]
        fullFIP = str(x[2]) + str(x[3])
        newCountyDict["fullFIP"] = fullFIP
        countyList.append(newCountyDict)
        
    #newDict = {}
    
    return countyList

#print(getCounties())


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpCountyTable(cur, conn):
    countyList = getCounties()
    cur.execute(f'CREATE TABLE IF NOT EXISTS CountyFIP (countyID TEXT PRIMARY KEY, countyName TEXT, stateFIP TEXT, countyFIP TEXT)')
    conn.commit()
def makeCountyTable(cur, conn):
    countyList = getCounties()
    cur.execute(f'SELECT countyID FROM CountyFIP')
    startNum = len(cur.fetchall())
    for county in countyList:
        fullFIP = county['fullFIP']
        name = county['name']
        stateFIP = county['stateFIP']
        countyFIP = county['countyFIP']
        cur.execute(f'INSERT OR IGNORE INTO CountyFIP (countyID, countyName, stateFIP, countyFIP) VALUES (?, ?, ?, ?)', (fullFIP, name, stateFIP, countyFIP))
        cur.execute(f'SELECT countyID FROM CountyFIP')
        newNum = len(cur.fetchall())
        if (newNum - startNum >= 25):
            break
    conn.commit()






   
def main():
   getCounties()
   cur, conn = setUpDatabase("covidCounty.db")
   setUpCountyTable(cur, conn)
   makeCountyTable(cur, conn)

if __name__ == '__main__':
   main()