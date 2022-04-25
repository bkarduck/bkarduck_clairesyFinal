from operator import itemgetter
import unittest
import sqlite3
import json
import os
import requests
import csv

# Name: Bella Karduck, Claire Yang


def getCounties():
    url = "https://api.census.gov/data/2019/acs/acs1/subject?get=NAME,S0101_C01_001E&for=county:*"
    r = requests.get(url)
    countyDict = r.json()
    
    countyList = []
    for x in countyDict[1:]:
        newCountyDict = {}
        newCountyDict["name"] = x[0]
    
        fullFIP = str(x[2]) + str(x[3])
        newCountyDict["fullFIP"] = fullFIP
        countyList.append(newCountyDict)

    
    return countyList

def get2020CountyPoverty():
    url = "https://api.census.gov/data/timeseries/poverty/saipe?get=SAEPOVRTALL_PT,SAEMHI_PT,GEOID&for=county:*&in=state:*&time=2020"
    r = requests.get(url)

    countyList = getCounties()
    newList = []
    for x in countyList:
        y = x['fullFIP']
        newList.append(y)
    countyPovertyDict = r.json()
    
    countyPovertyList = []
    for x in countyPovertyDict[1:]:
        newPovertyDict = {}
        ## FullFIP is the US standardized numbering system for different counties
        if x[2] in newList:
            newPovertyDict["fullFIP"] = x[2]
            newPovertyDict["povertyRate"] = float(x[0])
            newPovertyDict["medianIncome"] = float(x[1])
      
            countyPovertyList.append(newPovertyDict)
        
  
    return countyPovertyList
def getHighest100Poverty():
    newList = get2020CountyPoverty()
    sortedPoverty = sorted(newList, key = itemgetter('povertyRate'), reverse=True)
    counter = 0
    highest100Poverty = []
    for x in sortedPoverty:
        highest100Poverty.append(x)
        counter += 1
        if counter >= 100:
            break

   
    return highest100Poverty

def getLowest100Poverty():
    newList = get2020CountyPoverty()
    sortedPoverty = sorted(newList, key = itemgetter('povertyRate'))
    counter = 0
    lowest100Poverty = []
    for x in sortedPoverty:
        lowest100Poverty.append(x)
        counter += 1
        if counter >= 100:
            break

   
    return lowest100Poverty




def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpCountyTable(cur, conn):
    
    cur.execute(f'CREATE TABLE IF NOT EXISTS CountyFIP (countyID TEXT PRIMARY KEY, name TEXT)')
    cur.execute(f'CREATE TABLE IF NOT EXISTS Low100Poverty (countyID TEXT PRIMARY KEY, povertyRate NUMBER, medianIncome NUMBER)')
    cur.execute(f'CREATE TABLE IF NOT EXISTS High100Poverty (countyID TEXT PRIMARY KEY, povertyRate NUMBER, medianIncome NUMBER)')

    conn.commit()
def makeCountyPlusHighPovTable(cur, conn):
    countyList = getCounties()
    high100Pov = getHighest100Poverty()
   
    cur.execute(f'SELECT countyID FROM CountyFIP')
    startNum = len(cur.fetchall())
    for county in countyList:
        for x in high100Pov:
            if county['fullFIP'] == x['fullFIP']:
                fullFIP = county['fullFIP']
                name = county['name']
                
                povRate = x['povertyRate']
                medIncome = x['medianIncome']

                cur.execute(f'INSERT OR IGNORE INTO High100Poverty (countyID, povertyRate, medianIncome) VALUES (?, ?, ?)', (fullFIP, povRate, medIncome))

                cur.execute(f'INSERT OR IGNORE INTO CountyFIP (countyID, name) VALUES (?, ?)', (fullFIP, name))
                cur.execute(f'SELECT countyID FROM CountyFIP')
        newNum = len(cur.fetchall())
        if (newNum - startNum >= 25):
            break
    conn.commit()
def makeCountyPlusLowPovTable(cur, conn):
    countyList = getCounties()
    
    low100Pov = getLowest100Poverty()

    cur.execute(f'SELECT countyID FROM CountyFIP')
    startNum = len(cur.fetchall())
    for county in countyList:
        for x in low100Pov:
            if county['fullFIP'] == x['fullFIP']:
      
                fullFIP = county['fullFIP']
                name = county['name']
              
                povRate = x['povertyRate']
                medIncome = x['medianIncome']

                cur.execute(f'INSERT OR IGNORE INTO Low100Poverty (countyID, povertyRate, medianIncome) VALUES (?, ?, ?)', (fullFIP, povRate, medIncome))

                cur.execute(f'INSERT OR IGNORE INTO CountyFIP (countyID, name) VALUES (?, ?)', (fullFIP, name))
                cur.execute(f'SELECT countyID FROM CountyFIP')
        newNum = len(cur.fetchall())
        if (newNum - startNum >= 25):
            break
    conn.commit()
    

   
def main():
    getCounties()
    cur, conn = setUpDatabase("county.db")
    setUpCountyTable(cur, conn)
    
    makeCountyPlusHighPovTable(cur, conn)
    makeCountyPlusLowPovTable(cur, conn)
  
    conn.close()
  
   

if __name__ == '__main__':
   main()