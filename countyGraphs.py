import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import requests
import re
import os
import csv
import sqlite3
import json

def low100BarGraph(cur, conn):
    cur.execute("SELECT Low100Poverty.countyID, CountyFIP.name, Low100Poverty.povertyRate FROM Low100Poverty JOIN CountyFIP ON Low100Poverty.countyID = CountyFIP.countyID WHERE Low100Poverty.povertyRate < 5")
    richestCounties = cur.fetchall()
    
    RichStateCount = {}
   
    for county in richestCounties:
        nameList = county[1].split(",")
        stateName = nameList[1][1:]
        if stateName in RichStateCount:
            RichStateCount[stateName] += 1
        else:
            RichStateCount[stateName] = 1
    RichStateCount = sorted(RichStateCount.items(), key=lambda item: item[1], reverse= True)
    richStateList = []
    for state in RichStateCount:
         if int(state[1]) > 1:
            
            richStateList.append(state)
   
    state = []
    count = []
    for x in richStateList:
        state.append(x[0])
        count.append(int(x[1]))
    
    plt.bar(state, count, color='darkorchid', edgecolor = "grey")
    plt.yticks(np.arange(0, 7, 1)) 
    
    plt.ylabel("Number of Counties in a State with a Poverty Rate Below 5")

    plt.xlabel("State Name")

    plt.title("States with Multiple Large Counties That Have a Poverty Rate Below 5")

    plt.tight_layout()

    plt.show()

def high100BarGraph(cur, conn):
    cur.execute("SELECT High100Poverty.countyID, CountyFIP.name, High100Poverty.povertyRate FROM High100Poverty JOIN CountyFIP ON High100Poverty.countyID = CountyFIP.countyID WHERE High100Poverty.povertyRate > 22")
    poorestCounties = cur.fetchall()
    
    PoorStateCount = {}
   
    for county in poorestCounties:
        nameList = county[1].split(",")
        stateName = nameList[1][1:]
        if stateName in PoorStateCount:
            PoorStateCount[stateName] += 1
        else:
            PoorStateCount[stateName] = 1
    PoorStateCount = sorted(PoorStateCount.items(), key=lambda item: item[1], reverse= True)
    poorStateList = []
    for state in PoorStateCount:
         if int(state[1]) > 1:
            
            poorStateList.append(state)
    state = []
    count = []
    for x in poorStateList:
        state.append(x[0])
        count.append(int(x[1]))
    
     
    
    plt.bar(state, count, color='firebrick', edgecolor = "black")

    
    
    
   
    plt.yticks(np.arange(0, 5, 1)) 
 

    plt.ylabel("Number of Counties in a State with a Poverty Rate Above 22")

    plt.xlabel("State Name")

    plt.title("States with Multiple Large Counties That Have a Poverty Rate Above 22")

    plt.tight_layout()

    plt.show()

def richestAvgIncome(cur, conn):
    cur.execute("SELECT Low100Poverty.countyID, CountyFIP.name, Low100Poverty.povertyRate, Low100Poverty.medianIncome FROM Low100Poverty JOIN CountyFIP ON Low100Poverty.countyID = CountyFIP.countyID WHERE Low100Poverty.povertyRate < 5")
    richestCounties = cur.fetchall()
    incomeDict = {}
    incomeCalcDict = {}
    incomeAvg = {}
    
    for county in richestCounties:
        nameList = county[1].split(",")
        stateName = nameList[1][1:]
        if stateName in incomeDict:
            incomeDict[stateName] += 1
            incomeCalcDict[stateName] += county[3]
            incomeAvg[stateName] = incomeCalcDict[stateName] / incomeDict[stateName]
        else:
            incomeDict[stateName] = 1
            incomeCalcDict[stateName] = county[3]
    return incomeAvg

def richestCountiesIncomeGraph(cur, conn):
    incomeAvg = richestAvgIncome(cur, conn)
    state = []
    income = []
    for x in incomeAvg.items():
        state.append(x[0])
        income.append(x[1])

    plt.bar(state, income, color='darkblue', edgecolor = "grey")
  
    
    plt.ylabel("Average Income of All Counties in a State with a Poverty Rate Below 5")

    plt.xlabel("State Name")

    plt.title("Average Income of All Large Counties in a State That Have a Poverty Rate Below 5")

    plt.tight_layout()

    plt.show()

def writePovertyDataFile(filename, cur, conn):

    path = os.path.dirname(os.path.abspath(__file__)) + os.sep
    write_file = open(path + filename, "w")
    write = csv.writer(write_file, delimiter=",")
    write.writerow(("State Name", "Average Income"))
    avgIncome = richestAvgIncome(cur, conn)

    for state in avgIncome.items():  
        write.writerow((state[0], state[1]))
   
         
    conn.commit()
    write_file.close()
    
     



def main():
   
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/county.db')
    cur = conn.cursor()
    low100BarGraph(cur, conn)
    high100BarGraph(cur, conn)
    richestCountiesIncomeGraph(cur, conn)
    writePovertyDataFile("richestCountiesAvgIncome.csv", cur, conn)
    conn.close()



  

if __name__ == "__main__":
    main()
    