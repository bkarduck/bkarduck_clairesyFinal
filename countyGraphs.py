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
    cur.execute("SELECT Low100Poverty.countyID, CountyFIP.stateName, Low100Poverty.povertyRate FROM Low100Poverty JOIN CountyFIP ON Low100Poverty.countyID = CountyFIP.countyID WHERE Low100Poverty.povertyRate < 5")
    richestCounties = cur.fetchall()
    print(richestCounties)
    RichStateCount = {}
   
    for county in richestCounties:
        if county[1] in RichStateCount:
            RichStateCount[county[1]] += 1
        else:
            RichStateCount[county[1]] = 1
    RichStateCount = sorted(RichStateCount.items(), key=lambda item: item[1], reverse= True)
    richStateList = []
    for state in RichStateCount:
         if int(state[1]) > 1:
            richStateList.append(state)
    print(richStateList)
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
    cur.execute("SELECT High100Poverty.countyID, CountyFIP.stateName, High100Poverty.povertyRate FROM High100Poverty JOIN CountyFIP ON High100Poverty.countyID = CountyFIP.countyID WHERE High100Poverty.povertyRate > 22")
    poorestCounties = cur.fetchall()
    
    PoorStateCount = {}
   
    for county in poorestCounties:
        if county[1] in PoorStateCount:
            PoorStateCount[county[1]] += 1
        else:
            PoorStateCount[county[1]] = 1
    PoorStateCount = sorted(PoorStateCount.items(), key=lambda item: item[1], reverse= True)
    poorStateList = []
    for state in PoorStateCount:
         if int(state[1]) > 1:
            poorStateList.append(state)
    print(poorStateList)
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
        


def main():
   
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/county.db')
    cur = conn.cursor()
    low100BarGraph(cur, conn)
    high100BarGraph(cur, conn)

    conn.close()



  

if __name__ == "__main__":
    main()
    