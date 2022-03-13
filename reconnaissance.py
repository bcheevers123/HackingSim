from datetime import datetime
import subprocess
import re
import sys
import pandas as pd
from tabulate import tabulate

def scanIPBlock(targetHostnames):
        #Search through output for are targetHostnames
	result = subprocess.run(['nmap','-sP', '192.168.1.1/24'], universal_newlines = True ,stdout = subprocess.PIPE)
	targets = []
	for tHostname in targetHostnames:
	    for line in result.stdout.split("\n"):
                 if tHostname in line:
                    ipAddress = re.findall(r'[0-9]+(?:.[0-9]+){3}',line)[0]
                    print("Found: "+tHostname+ " at "+ ipAddress)
                    targets.append((tHostname,ipAddress))

	if targets == []:
	    print("Failed to find any targets, Aborting")
	else:
	    return targets
	    
def vulnScan(targets):
    portInfo = []
    columnNames = ["Port","Protocol","State","Service"]
    for target in targets:
        rows = []
        print("Executing: nmap -Pn "+target[1])
        result = subprocess.run(['nmap','-Pn',target[1]], universal_newlines = True, stdout = subprocess.PIPE)
        for line in result.stdout.split("\n"):
            #This could be improved "/" indicates a row in table output
            if "/" in line and "Starting" not in line:
                tableInfo = line.split(" ")
                #Remove spaces from output
                tableInfo = [value for value in tableInfo if value != ""]
                port = tableInfo[0].split("/")[0]
                protocol = tableInfo[0].split("/")[1]
                status = tableInfo[1]
                service = tableInfo[2]
                newRow = pd.Series(data=[port,protocol,status,service],index=["Port","Protocol","State","Service"])
                rows.append(newRow)
                
        portsDF = pd.DataFrame(rows, columns = columnNames)
        print("Port Scan Results for: "+ target[0])
        print(tabulate(portsDF, headers="keys", tablefmt='psql'))
        portInfo.append([target[0],target[1],portsDF])
        return portInfo

def gatherInfoSoftware(targets):
    softwareVers = []
    for target in targets:
        print("Gathering Software Info about "+target[0])
        openPorts = target[2]["Port"].tolist()
        for port in openPorts:
            print("nmap -A "+target[1]+ " -p " +str(port))
            result = subprocess.run(['nmap','-A', target[1], '-p',str(port)],universal_newlines = True, stdout = subprocess.PIPE)
            for line in result.stdout.split("\n"):
                if port in line and target[2].loc[target[2]['Port'] == port, 'Service'].item() in line:
                    line = line.split(" ")
                    line.remove('')
                    #Delete data we already have e.g 445/tcp open..
                    line.remove(line[0])
                    line.remove(line[0])
                    line.remove(line[0])
                    softwareVer = " ".join(line).strip()
                    if softwareVer == "":
                        softwareVer = "NMAP could not determine"
                    print(" ".join(line).strip())
                    softwareVers.append(softwareVer)
                    
                    
    print(softwareVers)
    #Need to ensure that the umber of entries matches the number of services.
    #If we can't find out what is being run, add a filler comment
    invalidSV = True
    while invalidSV:
    	try:
    	    target[2]['Software Version'] = softwareVers
    	    invalidSV = False
    	except:
    	    softwareVers.append("Could not read output")
    print(targets)
    return targets
        

