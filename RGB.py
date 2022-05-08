'''
The goal of this research study is to develop and demonstrate methods to automate benchmarking the energy efficiency of high performance computing systems based on the Green500 methodology via direct measurements obtained from the baseboard management controllers using Redfish standard, instead of via an external power meter and a manual process. To achieve this goal, we design and develop an automatic Green500 benchmark tool based on Redfish, called RGB (Redfish Green500 Benchmarker). This tool also evaluates implementations of the Redfish standard to determine their ability to meet the requirements of the Green500 benchmarking protocols.

If you have any question about that please contact [Elham Hojati](https://github.com/El-H-git).

'''

import requests
import socket
import ipaddress
import json
import datetime
import random
import time
import threading
import sys
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
from pyfiglet import figlet_format
import cs 
import time
import sys
from colorama import init
	   


BMCpass='********'
from threading import Timer
power=[]
l1_fraction=1
dc_elements=[]
#part 0: initializing--------------------------------------------------------------------------------------------------

def initRGB():
     CHAR_PER_LINE=40
     print("...............................................................................")
     time.sleep(1)
     print("...............................................................................")
     time.sleep(1)
     print("...............................................................................")
     time.sleep(1)
     print("...............................................................................")	 
     cprint(figlet_format('Redfish    ' , font='starwars'),
            'yellow', 'on_red', attrs=['bold'])
     time.sleep(1)
     cprint(figlet_format('Green500  ' , font='starwars'),
            'yellow', 'on_green', attrs=['bold'])
     time.sleep(1)
     cprint(figlet_format('Tool            ' , font='starwars'),
            'yellow', 'on_blue', attrs=['bold'])
     time.sleep(1)
     print("...............................................................................")
     time.sleep(1)
     print("...............................................................................")
     time.sleep(1)
     print("...............................................................................")
     time.sleep(1)
     print("...............................................................................")
     init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
     CHAR_PER_LINE=80
     print("\n")
     cprint("RGB:".center(CHAR_PER_LINE-2), 'white','on_blue')
     cprint("Redfish Green500 Benchmarker".center(CHAR_PER_LINE-2), 'white','on_green')
#----------------------------------------------------------------------------------------------------------------------



#part 1: input function for selecting Requested Green500 level (1,2, 3) -----------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
def get_Green500_Level_info():
    init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
    CHAR_PER_LINE=80
    print("Green500 is for measuring,  recording, and reporting the power used by a HPC \n (high performance computing ) system while running a workload.")
    print("...............................................................................")
    time.sleep(1)
    print("...............................................................................")
    time.sleep(1)
    print("...............................................................................")
    print()
    print()
    cprint("getting RGB inputs".center(CHAR_PER_LINE-2), 'white','on_blue')
    cprint("Input 1: Green500 Guality level".center(CHAR_PER_LINE-2), 'white','on_blue')
    level= input("Please inset your selected Green500 Guality level (1, 2 or 3): ")
    print("...............................................................................")
    time.sleep(1)
    print("...............................................................................")
    time.sleep(1)
    print("...............................................................................")
    return(level)


	
	



	
#part 2: input get  datacenter information ----------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
def get_datacenter_info():
    global dc_elements
    init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
    CHAR_PER_LINE=80
    cprint("Input 2: A Redfish enabled cluster to be submitted to the Green500 List".center(CHAR_PER_LINE-2), 'white','on_blue')
    cprint("get_datacenter_information".center(CHAR_PER_LINE-2), 'white','on_blue')
    filename = input('Input a file contains datacenter information: ')
    print("getting Data Center information from file......................................")
    print("...............................................................................")
    time.sleep(1)
    print("...............................................................................")
    time.sleep(1)
    print("...............................................................................")
    try:
        data_file = open(filename, "r")    #"Machine Fraction.txt"
    except IOError:                      # we get here if file open failed
        print('Bad file name')
        return()
    
    linesList=data_file.readlines()
    i=0
    data_file.close()
    for e in linesList:
        e=e.strip()
        linesList[i]=e
        i=i+1
    dc_elements=linesList
    return(linesList)
#----------------------------------------------------------------------------------------------------------------------
	
	
	
	



	
#part 3: This function is for selecting machine fraction based on the level) ------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
def machine_fraction(level, l):
    print("...............................................................................")
    time.sleep(1)
    print("...............................................................................")
    time.sleep(1)
    print("...............................................................................")
    init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
    CHAR_PER_LINE=80
    cprint("Step A) Initialization step".center(CHAR_PER_LINE-2), 'white','on_blue')
    print("...............................................................................")
    time.sleep(1)
    print("...............................................................................")
    time.sleep(1)
    print("...............................................................................")
    mfl=[]
    global l1_fraction
    if(level=="1"):
        print("for level one of Green500 measurment, you need to select one of the following machine fraction of datacenter:")
        print(" 1) The entire system \n 2) at least  40  kW \n 3) the largest  of 1/10 of  the compute  subsystem, 2 kW, 15 compute nodes  \n ")
        i=input("\nwhich way to select machine fraction you want?(1/2/3)  ")
        if(i=='1'):
           l1_fraction=1
           machine_fraction_1_1(l)
        if(i=='2'):
           l1_fraction=2 
          # machine_fraction_1_2(l)
        if(i=='3'):
           l1_fraction=3
           #mfl=machine_fraction_1_3(l)
        


        
		   
    return(l, l1_fraction)
#----------------------------------------------------------------------------------------------------------------------








#part 4: This function is for selecting machine fraction based on the level- (The entire system) ----------------------
#----------------------------------------------------------------------------------------------------------------------
def machine_fraction_1_1(l):
     print("\n\n\n***     -----------------------------------------------------------------     ***\n ")
     print("***     -----------------------------------------------------------------     ***")
     print("***     ---selected machine fraction (list of computing nodes for Level 1):---     ***\n\n")
     x=1
     for i in l:
         print("compute node ",x,": ",i)
         x=x+1
     return(l)		   
   
#----------------------------------------------------------------------------------------------------------------------








#part 5: This function is for selecting machine fraction based on the level- at least  40  kW -------------------------
#----------------------------------------------------------------------------------------------------------------------
def machine_fraction_1_2(l):
     print("\n\n\n***     -----------------------------------------------------------------     ***\n ")
     print("***     -----------------------------------------------------------------     ***")
     print("***     ---selected machine fraction (list of computing nodes for Level 1):---     ***\n\n")
    
     total_power=0
     clusterSize=0
     t=0
     
     for i in power:
         t=t+1
         total_power=total_power+i	
         if (total_power>=40000):
              fracSize=t
              j=0
              while (j<fracSize):
                    print("compute node ",j+1,": ",l[j])
                    j=j+1
                    return(total_power)
     x=1
     for i in l:
         print("compute node ",x,": ",i)
         x=x+1 
                   
     return(total_power)
#----------------------------------------------------------------------------------------------------------------------








#part 6: This function is for selecting machine fraction based on the level- 15 compute nodes -------------------------
#----------------------------------------------------------------------------------------------------------------------
def machine_fraction_1_4(l):
     n=0
     l2=[]
     rnset=set()
     #print("len(l)= ",len(l))
     while(len(rnset)<48):
        rn=random.randint(0,len(l)-1)
        rnset.add(rn)
     print("The id of nodes selected randomly: ", rnset)
     for i in rnset:
          l2.append(l[i])
		  
     print("...............................................................................")
     time.sleep(1)
     print("...............................................................................")
     time.sleep(1)
     print("...............................................................................")

     print("\n\n selected machine fraction:\n\n")
     print("LIst of selected nodes: ",l2)
     return (l2)
#----------------------------------------------------------------------------------------------------------------------








#part 7: This function is for selecting machine fraction based on the level- the largest  of 1/10 of the compute subsystem, 2 kW ,
# the largest  of 1/10 of  the compute  subsystem, 2 kW, 15 compute nodes
#----------------------------------------------------------------------------------------------------------------------
def machine_fraction_1_3(l):
     
     print("\n\n\n***     -----------------------------------------------------------------     ***\n ")
     print("***     -----------------------------------------------------------------     ***")
     #print("***     ---selected machine fraction (list of computing nodes for Level 1):---     ***\n\n")

     total_power=0
     clusterSize=0
     power15=0
     power1of10size=len(l)//10
     power1of10=0
     power2k=0
     j=0
     while(j<=power1of10size):
         power1of10= power1of10+power[j]
         j=j+1
     if(power1of10size>total_power):
             total_power=power1of10size
     j=0
     while(j<=15):
         power15=power15+power[j]
         j=j+1    
         
     if(power15>total_power):
             total_power=power15
     t=0

     for i in power:
         t=t+1
         if(power2k<=2000):
                    power2k=power2k+i
        
     if(power2k>total_power):
             total_power=power2k
     return(total_power)
#----------------------------------------------------------------------------------------------------------------------






#part 8: This function is for Launching the Linpack benchmark for one minutes) ----------------------
#----------------------------------------------------------------------------------------------------------------------
def  run_linpack():

    print("...............................................................................")
    time.sleep(1)
    print("...............................................................................")
    time.sleep(1)
    print("...............................................................................")
    init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
    CHAR_PER_LINE=80
    cprint("Step B) Measurement Step ".center(CHAR_PER_LINE-2), 'white','on_blue')
    print("...............................................................................")
    time.sleep(1)
    print("...............................................................................")
    time.sleep(1)
    print("...............................................................................")
    cprint("The process of Launching the Linpack benchmark ) ".center(CHAR_PER_LINE-2), 'white','on_blue')
    cprint("for t sec (based on timing algorithm) ".center(CHAR_PER_LINE-2), 'white','on_blue')
    print("...............................................................................")
    time.sleep(1)
    print("...............................................................................")
    time.sleep(1)
    print("...............................................................................")	   
    return
#----------------------------------------------------------------------------------------------------------------------







#part 9: This function is for Recording Power -------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
def power_record(ip,index):
     global BMCpass
     print(" Start Power Recording Process for mcompute machine", ip, " ......")
     sample=0
     p=0
     t=0
     global power
	 

#********************************************************************************	
# Create a Redfish session

     s = requests.Session()
     s.auth = ('root', BMCpass)
	 


	 
     #t = Timer( 20, timeout)
     #t.start()
     while(t<=20):
         p1=int(getPowerInfo(s,ip))
         p=p+p1
         print(p1)
         time.sleep(1)
         t=t+1
   
     print("consumed Power for compute machine ", ip," =  ",p)
     power.append(p)
 #----------------------------------------------------------------------------------------------------------------------







 
 #part 9: This function is for Recording Power ------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
def total_power_record(l):

     init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
     CHAR_PER_LINE=80
     cprint(" Power Recording Process ".center(CHAR_PER_LINE-2), 'white','on_blue')
     print("...............................................................................")
     time.sleep(1)
     print("...............................................................................")
     time.sleep(1)
     print("...............................................................................")
     threads= []
     for i in range(0,len(l)):
          t = threading.Thread(target=power_record , args=(l[i],i))
          threads.append(t)
          t.start()

		  
     for t in threads:    
          t.join() 		  

 #----------------------------------------------------------------------------------------------------------------------




 #part 9: timer timeout function --------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------- 
def calculate_output():

    global dc_elements
    init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
    CHAR_PER_LINE=80
    cprint(" RGB Calculating Process ".center(CHAR_PER_LINE-2), 'white','on_blue')
	
    print("...............................................................................")
    time.sleep(1)
    print("...............................................................................")
    time.sleep(1)
    print("...............................................................................")
    cprint(" RGB OUTPUT: 1- GFLOPS Per Watt, 2- P̅(R_max)".center(CHAR_PER_LINE-2), 'white','on_blue')
    total_power=0
    #print("***     -----------------------------------------------------------------     ***")
    for i in power:
         total_power=total_power+i


    if l1_fraction==2:
       total_power=machine_fraction_1_2(dc_elements)
    if l1_fraction==3:
       total_power=machine_fraction_1_3(dc_elements)
    print("***     -----------------------------------------------------------------     ***\n\n\n")
    time.sleep(3)
    print("***     ------------ final Green500 Result for this system: -------------     ***")
    print("total consumed power=", total_power, " watts")
    print("getting linpack results......")
    print("Check the Linpack Benchmark Result to see theperformance output  (GFLOPS) ")
    print(" Find the Grean500 Evaluation Result based on the results of the Linpack Benchmark, and the total consumed power calculated by the RGB tool:" ,   " the Grean500 Evaluation Result (GFLOPS Per Watt)")
    print("***     -----------------------------------------------------------------     ***\n\n\n\n\n\n")
    cprint(" Output is ready to be submitted for Green500 List".center(CHAR_PER_LINE-2), 'white','on_green')
    print("\n\n\n\n\n")	
    time.sleep(3)	
#----------------------------------------------------------------------------------------------------------------------
 
 
 


 #part 9: timer timeout function --------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------- 
def timeout():
    print("Record over")
#----------------------------------------------------------------------------------------------------------------------
 
 
 
 

#part 10: This function is for disabling warnings in requests' vendored urllib3, (insecure request warnings)------------
#----------------------------------------------------------------------------------------------------------------------
def DisShowingInsecureWarning():
	from requests.packages.urllib3.exceptions import InsecureRequestWarning
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#----------------------------------------------------------------------------------------------------------------------








#part 11: This function is for  Getting the  IP Address from the user --------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
def readIP():
	e=1
	while(e==1):
	 try:
		 ip=input("Please insert your IP: ")
		 ip2=ipaddress.ip_address(ip)
		 ip=ip2.compressed   #convert IP format to string format
		 e=0
	 except ValueError:
	     print("your IP is not correct, please try again")
	return ip
#----------------------------------------------------------------------------------------------------------------------
   

   

      
   
   
   
#part 12: This function is for  Getting the machineأ¢â‚¬â„¢s hostname ---------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------

def getHostName(ip):
	try:
		ip100="10.100"+ip[6:]
		hn= socket.gethostbyaddr(ip100)
	except:
		print("cannot find the hostname")
		hn=""
	return(hn)
#----------------------------------------------------------------------------------------------------------------------








#part 4:  This function is for  Getting  timestamp from when the data was retrieved------------------------------------
#----------------------------------------------------------------------------------------------------------------------
def getTimeStamp():
	ctime=datetime.datetime.now() #current time
	str_ctime=str(ctime)          #convert the current time to string
	#print(ctime)
	return(str_ctime)
#----------------------------------------------------------------------------------------------------------------------













		
		
#part 6: This function is for getting the power values for the machine ------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
def getPowerInfo(s, ip):
	uri="https://"+ip+"/redfish/v1/Chassis/System.Embedded.1/Power/PowerControl"
	DisShowingInsecureWarning()
	try:
		systemPower = s.get(uri,verify=False)
	except():
		print("warning in getting Power Information from Redfish")
	systemPowerData = systemPower.json()
	print(systemPowerData)
	print("Consumed power=",systemPowerData['PowerConsumedWatts']," (watts).")
	return(systemPowerData['PowerConsumedWatts'])
#----------------------------------------------------------------------------------------------------------------------	
	





	
	
#part 7: This function is for getting the current state of the machine (on, off, etcأ¢â‚¬آ¦), and HostName ------------------
#----------------------------------------------------------------------------------------------------------------------	
def getVoltPowerInfo(ip):
	uri="https://"+ip+"/redfish/v1/Chassis/System.Embedded.1/Power"
	DisShowingInsecureWarning()
	try:
		systemVolt = requests.get(uri,verify=False, auth=('root',BMCpass))
	except():
		print("warning in getting Power Information from Redfish")
	systemVoltData = systemVolt.json()
	return (systemVoltData['Voltages'],systemVoltData['PowerControl'])
#----------------------------------------------------------------------------------------------------------------------	







	
#part 8: This function is for getting the current state of the machine (on, off, etcأ¢â‚¬آ¦), and HostName ------------------
#----------------------------------------------------------------------------------------------------------------------	
def getPowerState(ip):
	uri="https://"+ip+"/redfish/v1/Systems/System.Embedded.1"
	DisShowingInsecureWarning()
	try:
		systemHostName = requests.get(uri,verify=False,auth=('root',BMCpass))
	except():
		print("warning in Getting Power state from Redfish")	
	systemHostNameData = systemHostName.json()
	#print ("Host Name= ",systemHostNameData['HostName'])
	#print ("Power state= ",systemHostNameData['PowerState'])
	return(systemHostNameData['HostName'], systemHostNameData['PowerState'])
#----------------------------------------------------------------------------------------------------------------------	














# part 10: This fuction is for creating the full output-----------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------	
def createFullOutput(ip):
	outputjsondic={} 
	outputjsondic['IP1']=ip
	outputjsondic['IP2']="10.100"+ip[6:]
	outputjsondic['hostname']=getHostName(ip)
	outputjsondic['current_time']=getTimeStamp()
	outputjsondic['Temperatures']=getCPUtemp(ip)
	#outputjsondic['Consumed power']=getPowerInfo(ip)
	outputjsondic['Voltages'],  outputjsondic['Power Control'] =getVoltPowerInfo(ip)
	outputjsondic['Host Name'], outputjsondic['Power State']=getPowerState(ip)
	outputjsondic['SEL']=getSEL(ip)
	return(outputjsondic)
#i=1  # event number
#for EventLog in systemSELData['Members']: 
#	print ("Event", EventLog['Name'],"    ",EventLog['Created'], "\n Event Message:  ",EventLog['Message'])  
#	i=i+1
#----------------------------------------------------------------------------------------------------------------------		












#part 12: This fuction is for creating smaller jsondic ----------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------	
def createSmallOutput(ip):
    outputjsondic=createFullOutput(ip)
    SystemInfo={}
    SystemInfo['IP1']=outputjsondic['IP1'] 
    SystemInfo['IP2']=outputjsondic['IP2'] 
    SystemInfo['Host Name']=outputjsondic['hostname'][0]  
    SystemInfo['current_time']=outputjsondic['current_time']

	#initializing  temprature dictionary
    tempdic={}   
    for e in outputjsondic['Temperatures']: 
      tempdic[e['Name']]=e['ReadingCelsius']
      SystemInfo['Tempratures']=tempdic

	#initializing  SEL dictionary
    seldic={}  
    for e in outputjsondic['SEL']: 
      seldic[e['Name']]=e['Created']+"  "+e['Message']
    SystemInfo['SEL']=seldic
	
    SystemInfo['Power State']=outputjsondic['Power State']
    SystemInfo['HostNamebyRedfish']=outputjsondic['Host Name']
	
    #SystemInfo['Consumed power']=outputjsondic['Power Control'][0]['PowerConsumedWatts']


    voltdic={}
    for v in outputjsondic['Voltages']: 
      voltdic[v['Name']]=v['ReadingVolts']
    SystemInfo['Voltages']=voltdic
    return (SystemInfo)
	
	
	
#----------------------------------------------------------------------------------------------------------------------


	





#part 13 print smaller jsondic (SystemInfo) ------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
def printSmalloutput():
	ip=readIP()
	SystemInfo=createSmallOutput(ip)
	print("printing the small JSON OBJECT:")
	json_SystemInfo=json.dumps(SystemInfo)
	print(json_SystemInfo)
#----------------------------------------------------------------------------------------------------------------------
#printSmalloutput()












#part 14 get information for a list of nodes --------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
def getNodeData(sl): #sl is a list of  hostname and ip lists
    mylistJSON=[]
    myErrList=[]
    for l in sl:
        ip=l[0]
        hn=l[1]
        try:
             SystemInfo=createEricOutput(ip)
             json_SystemInfo=json.dumps(SystemInfo)
             mylistJSON.append(json_SystemInfo)
            
        except:
             myErrList.append([ip,hn,"Error"])
    return(mylistJSON,myErrList)  
#----------------------------------------------------------------------------------------------------------------------		








#part 15 main function ------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
def main1():
    sl=[]   # list of ip and hostname
    t=True
    while(t):
        if(input("Do you want to add an IP to the list?(Y/N)")=="Y"):
           ip=readIP()
           hn=getHostName(ip)
           sl.append([ip, hn])
        else:
           t=False
    print(getNodeData(sl))
		   




#part 15 main function ------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
def main():
      initRGB()
      level=get_Green500_Level_info()
      l=get_datacenter_info()
      print("***     -----------------------------------------------------------------     ***\n")
      print("***     ------------------  DataCenter Compute Nodes:  ------------------     ***\n")
      print("***     -----------------------------------------------------------------     ***")
      time.sleep(3)

      x=1
      for i in l:
         print("compute node ",x,": ",i)
         time.sleep(0.15)
         x=x+1
      print("\n\n\n\n")
      l2,a=machine_fraction(level,l)
      run_linpack()
      total_power_record(l)
      print("***     -----------------------------------------------------------------     ***\n")
      print("***     ----Total power consumed by each node in the seledted fraction of data center----     ***\n\n")
      time.sleep(3)
      print("The calculated power vector is",power)
      print("\n\n\n")
      calculate_output()


	  
#----------------------------------------------------------------------------------------------------------------------
main()








