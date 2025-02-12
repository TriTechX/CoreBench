#Built-in packages
import time
import os
import socket
import multiprocessing
import threading
import math
import platform
import ctypes
import random
from datetime import datetime
import subprocess
import re
import getpass
import csv
#Third-party packages
import cpuinfo
import psutil
import GPUtil
import distro
import speedtest
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
#Custom packages
import colours
#package functions
mpl.use("Agg")
homedir = os.getcwd()

# s'il vous plaît exterminer la vermine mercy bookoo
# if you can find a way to optimise the loading times that would be good
# i know it says GPU test in the notes, please do not make the GPU test because it requires pyCUDA and other cuda stuff that is beyond the storage limit for this account, I'll do it when I move to a collab or something idk


try:
    os.mkdir("DATA")
    os.chdir(homedir)
except PermissionError:
    print("Failed to make DATA directory. Please give CoreBench rw access to its current directory.")
    exit()
except FileExistsError:
    pass
    os.chdir(homedir)

def clear():

    name = str(os.name)
    if name in ["nt","dos"]:
        os.system("cls")
    else:
        os.system("clear")

clear()

#this is a part of the loading process that happens before the loading screen
def prefetch():
    global osName, memRaw, brandName, hostname, localIp, done
    osName = platform.system()
    memRaw = round(((psutil.virtual_memory().total)/(1e+6)))
    brandName = cpuinfo.get_cpu_info()["brand_raw"]
    hostname = socket.gethostname()
    localIp = socket.gethostbyname(socket.gethostname())
    done = True

#this shows the activating screen
def preload():
    global done
    print(colours.grey() + "Activating..." + colours.reset())
    while done == False:
        time.sleep(0.01)

#prepares for dynamic mode, just adjusts the CPU tests depending on how many CPU cores and threads you have
dynamicMode = False

#runs the activating process
if __name__ == "__main__":
    try:
        grep = threading.Thread(target=prefetch)
        load = threading.Thread(target=preload)

        done = False

        grep.start()
        load.start()

        grep.join()
        load.join()
    except Exception as e:
        f = open("log.txt", "a")
        f.write(e)
        f.close()

### ZONE OF EXPERIMENTATION ###
### END OF ZONE ###

#yeah
def get_user():
    return getpass.getuser()

#makes sure it's running admin
if str(os.name).lower() in ["nt", "dos", "windows"]:
    def checkRoot():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
else:
    def checkRoot():
        return os.getuid() == 0
if checkRoot:
    pass
else:
    print(colours.red() + "This script needs to be run as administrator, bugs may occur." + colours.reset())
    temp = input(colours.grey() + "Press [ENTER] to continue..." + colours.reset())
    

#Get system information, runs during the main load
def getData():
    try:
    
        global hostname, GPUs, osName, architecture, brandName, clockSpeed, CPUs, memRaw, memory, endLoad, distroName, localIp, Threads, threadsPerCore, osNamePretty, user, version
        try:
            hostname = socket.gethostname()
            localIp = socket.gethostbyname(socket.gethostname())
            GPUs = GPUtil.getGPUs()
            osName = platform.system()
            architecture = platform.machine()
            brandName = cpuinfo.get_cpu_info()["brand_raw"]
            clockSpeed = cpuinfo.get_cpu_info()["hz_advertised_friendly"]
            clockList = clockSpeed.split(" ")
            clockSpeed = float(clockList[0])
            clockSpeed = round(clockSpeed,2)
            clockSpeed = str(clockSpeed) + " GHz"
            CPUs = psutil.cpu_count(logical=False)
            Threads = os.cpu_count()
            threadsPerCore= int(os.cpu_count())/int(CPUs)
            memRaw = round(((psutil.virtual_memory().total)/(1e+6)))
            memory = round(((psutil.virtual_memory().total)/(1e+9)),2)
            user = get_user()
            if osName in ["Linux"]:
                time.sleep(1)
                distroName = str(distro.name(pretty=True))

                def distroColour():
                    result = subprocess.run(["neofetch"], capture_output=True, text=True)
        
                    f=open("NeofetchOut.txt", "w")
                    f.write(result.stdout)
                    f.close()
        
                    file_path = "NeofetchOut.txt"
                    f=open("NeofetchOut.txt", "r")
                    contents=f.read()
                    pattern = r"\033\[(3[0-7]|9[0-7])m"
                    match = re.findall(pattern, contents)
        
                    while "37" in match or "97" in match:
                        i=-1
                        for item in match:
                            i+=1
                            if item.strip() == "97" or item.strip() == "37":
                                match.pop(i)
        
        
                    distroColourCode = f"\033[{match[0]}m"
                    return distroColourCode
                osNamePretty=f"{distroColour()}{distroName}"
                os.remove("NeofetchOut.txt")
            
            else:
                if osName.lower() in ["nt", "dos", "windows"]:
                    osNamePretty=colours.blue() + osName
                else:
                    osNamePretty=colours.grey() + osName
                
        except Exception as e:
            f=open("log.txt","w")
            f.write(str(e))
            f.close()
            
        #UPDATE THIS WITH EVERY VERSION
        version = "1.1.0"
        #UPDATE THIS WITH EVERY VERSION
        
        endLoad = True
    #the classic messages we always have, feel free to add, trying to keep this one less bloated
    except Exception as e:
        f = open("log.txt","w")
        f.write(str(e))
        f.close()
messages = ["So, you're back...", "Hello there!", "It's hot in here...", "400FPS", "Disabling frame generation...", "RTX ON", "Removing nanites...", "Stealing your personal information...", "Pro tip: bench", "Sussy Bucket", "No standard users allowed!", "Connecting to the (totally functional) CoreBench database...", "Getting more ping...", "Optimizing...", "Initiating...", "WELCOME.", f"Here with your {brandName} I see...", f"{osName}? A fellow man of culture...", f"Eating all {memRaw}MB of RAM...", "Overclocking...", "Deleting main.py...", "Always remember to remove the French language pack!", f"Not much of a {osName} fan myself, but you do you...", f"Welcome back {hostname}.", f"Haha! Got your IP! Seriously! {localIp}", "I use Arch btw", "I use Core btw", "Over 6GHz!", "Bringing out the Intel Pentium...", "Gathering texel fillrate...", "Collecting frames...", "No fake frames here!", "Changing boot order...", "Imagine if you were using this on Windows lol", "Still held prisoner by Replit.", "It's dangerous to go alone.", "All your bench are belong to us.", "GPU bench coming soon. Maybe.", "Unused RAM is useless RAM. Give some to me."]

message = messages[random.randint(0,len(messages)-1)]


#runs the loading screen
def loadingScreen():
    try:
    
        def clear():
            
            name = str(os.name)
            if name in ["nt","dos"]:
                os.system("cls")
            else:
                os.system("clear")
        
        global endLoad
        clear()
        
        while endLoad == False:
            
            print(colours.cyan() + """░█████╗░░█████╗░██████╗░███████╗""")
            print("""██╔══██╗██╔══██╗██╔══██╗██╔════╝""")
            print("""██║░░╚═╝██║░░██║██████╔╝█████╗░░""")
            print("""██║░░██╗██║░░██║██╔══██╗██╔══╝░░""")
            print("""╚█████╔╝╚█████╔╝██║░░██║███████╗""")
            print("""░╚════╝░░╚════╝░╚═╝░░╚═╝╚══════╝""")
            print()
            print(colours.magenta() + """██████╗░███████╗███╗░░██╗░█████╗░██╗░░██╗""")
            print("""██╔══██╗██╔════╝████╗░██║██╔══██╗██║░░██║""")
            print("""██████╦╝█████╗░░██╔██╗██║██║░░╚═╝███████║""")
            print("""██╔══██╗██╔══╝░░██║╚████║██║░░██╗██╔══██║""")
            print("""██████╦╝███████╗██║░╚███║╚█████╔╝██║░░██║""")
            print("""╚═════╝░╚══════╝╚═╝░░╚══╝░╚════╝░╚═╝░░╚═╝""")
            print(colours.reset())
            print(colours.grey() + "© TriTech 2025 - If you paid for this software, get a refund.\n" + colours.reset())
            print(message)
            time.sleep(0.3)
            clear()
            print(colours.magenta() + """░█████╗░░█████╗░██████╗░███████╗""")
            print("""██╔══██╗██╔══██╗██╔══██╗██╔════╝""")
            print("""██║░░╚═╝██║░░██║██████╔╝█████╗░░""")
            print("""██║░░██╗██║░░██║██╔══██╗██╔══╝░░""")
            print("""╚█████╔╝╚█████╔╝██║░░██║███████╗""")
            print("""░╚════╝░░╚════╝░╚═╝░░╚═╝╚══════╝""")
            print()
            print(colours.green() + """██████╗░███████╗███╗░░██╗░█████╗░██╗░░██╗""")
            print("""██╔══██╗██╔════╝████╗░██║██╔══██╗██║░░██║""")
            print("""██████╦╝█████╗░░██╔██╗██║██║░░╚═╝███████║""")
            print("""██╔══██╗██╔══╝░░██║╚████║██║░░██╗██╔══██║""")
            print("""██████╦╝███████╗██║░╚███║╚█████╔╝██║░░██║""")
            print("""╚═════╝░╚══════╝╚═╝░░╚══╝░╚════╝░╚═╝░░╚═╝""")
            print(colours.reset())
            print(colours.grey() + "© TriTech 2025 - If you paid for this software, get a refund.\n" + colours.reset())
            print(message)
            time.sleep(0.3)
            clear()
            print(colours.green() + """░█████╗░░█████╗░██████╗░███████╗""")
            print("""██╔══██╗██╔══██╗██╔══██╗██╔════╝""")
            print("""██║░░╚═╝██║░░██║██████╔╝█████╗░░""")
            print("""██║░░██╗██║░░██║██╔══██╗██╔══╝░░""")
            print("""╚█████╔╝╚█████╔╝██║░░██║███████╗""")
            print("""░╚════╝░░╚════╝░╚═╝░░╚═╝╚══════╝""")
            print()
            print(colours.cyan() + """██████╗░███████╗███╗░░██╗░█████╗░██╗░░██╗""")
            print("""██╔══██╗██╔════╝████╗░██║██╔══██╗██║░░██║""")
            print("""██████╦╝█████╗░░██╔██╗██║██║░░╚═╝███████║""")
            print("""██╔══██╗██╔══╝░░██║╚████║██║░░██╗██╔══██║""")
            print("""██████╦╝███████╗██║░╚███║╚█████╔╝██║░░██║""")
            print("""╚═════╝░╚══════╝╚═╝░░╚══╝░╚════╝░╚═╝░░╚═╝""")
            print(colours.reset())
            print(colours.grey() + "© TriTech 2025 - If you paid for this software, get a refund.\n" + colours.reset())
            print(message)
            time.sleep(0.3)
            clear()
    except Exception as e:
        f=open("log.txt","a")
        f.write(e)
        f.close()

if __name__ == "__main__":
    try:
        grep = threading.Thread(target=getData)
        load = threading.Thread(target=loadingScreen)
    
        endLoad = False
        
        grep.start()
        load.start()
    
        grep.join()
        load.join()
    
    except Exception as e:
        f = open("log.txt","a")
        f.write(e)
        f.close()

def prettyPrintData():
    if "AMD" in brandName:
        cpuColour = colours.red()
    elif "Intel" in brandName:
        cpuColour = colours.cyan()
    else:
        cpuColour = colours.magenta()

    print("------")

    print(f"{colours.magenta()}OS Name{colours.reset()}: {osNamePretty}")
        
    
    print(f"{colours.cyan()}Architecture{colours.reset()}: {architecture}")
    
    
    print("------")
    
    
    print(f"{colours.magenta()}CPU name{colours.reset()}: {cpuColour}{brandName}{colours.reset()}")
    
    
    print(f"{colours.cyan()}CPU clock speed{colours.reset()}: {clockSpeed}")
    
    
    print(f"{colours.green()}CPUs{colours.reset()}: {CPUs} Cores")
    print(f"{colours.cyan()}Threads{colours.reset()}: {Threads} Threads")
    
    print("------")
    
    
    print(f"{colours.magenta()}RAM{colours.reset()}: {memory}{colours.cyan()} GB{colours.reset()}")
    
    print("------")
    
    for gpu in GPUs:
        print(f"{colours.cyan()}GPU Name{colours.reset()}: {gpu.name}")
        print(f"{colours.magenta()}VRAM{colours.reset()}: {gpu.memoryTotal} MB")


if len(GPUs)>0:
    gpuPresent = True
else:
    gpuPresent = False


#set clear() to clear the screen
def clear():

    name = str(os.name)
    if name in ["nt","dos"]:
        os.system("cls")
    else:
        os.system("clear")

N = 1000000
#intensity of the test, point system will not scale with intensity
filename = "corebenchinfo.txt"

if not os.path.exists(filename) or os.path.getsize(filename) == 0:
    f=open("corebenchinfo.txt", "w")
    f.close()
    os.remove("corebenchinfo.txt")
    f=open("corebenchinfo.txt", "w")
    
    f.write("OS Name: " + str(osName) + "\n")
    f.write("Architecture: " + str(architecture) + "\n")
    f.write("CPU Name: " + str(brandName) + "\n")
    f.write("CPU clock speed: " + str(clockSpeed) + "\n")
    f.write("CPUs: " + str(CPUs) + "\n")
    f.write("Threads: " + str(Threads) + "\n")
    f.write("Threads Per Core: " + str(threadsPerCore) + "\n")
    f.write("RAM: " + str(memRaw) + " MB\n")
    for gpu in GPUs:
        f.write("GPU Name: " + str(gpu.name) + "\n")
        f.write("GPU Name: " + str(gpu.memoryTotal) + " MB\n")
    f.close()

filename="DATA/corebenchdata.csv"
if not os.path.exists(filename) or os.path.getsize(filename) == 0:
    f=open(filename, "w")
    headers=[["single", "mcore", "mthread", "full"]]

    with open("DATA/corebenchdata.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(headers)
        
    f.close()
#write specifications to a file
#single core CPU test
def singleCore(showResults):

    def oneSigFig(num):
        output = int(round(num, 1-len(str(int(abs(num))))))
        return output
    
    p = psutil.Process(os.getpid())
    for item in p.cpu_affinity():
        try:
            p.cpu_affinity([0])
        except:
            p.cpu_affinity(list(range(os.cpu_count()))) #reset
    
    global SINGLENO, N
    numList = []

    SINGLENO = int(N/2)
    #Stage 1, adds all the numbers to a list

    percent = 0
    oldPercent = 0
    print(f"Single Core test {colours.green()}initiated{colours.reset()}. This one takes a {colours.magenta()}while{colours.reset()}...")
    print("------")
    print("Stage 1: {}% done".format(percent))

    start = time.perf_counter()

    for x in range(0,SINGLENO):

        percent = int(oneSigFig((x/SINGLENO)*100))

        if oldPercent != percent:
            clear()
            print(f"Single Core test {colours.green()}initiated{colours.reset()}. This one takes a {colours.magenta()}while{colours.reset()}...")
            print("------")
            print("Stage 1: {}% done".format(percent))

        numList.append(x)

        oldPercent = percent

    end = time.perf_counter()
    stageOne = end-start
    
    #Stage 2, finds the square root of all of those numbers

    percent = 0
    oldPercent = 0

    clear()
    print(f"Single Core test {colours.green()}initiated{colours.reset()}. This one takes a {colours.magenta()}while{colours.reset()}...")
    print("------")
    print("Stage 2: {}% done".format(percent))

    start = time.perf_counter()

    i=0

    for item in numList:

        i+=1

        percent = oneSigFig((i/SINGLENO)*100)

        if oldPercent != percent:
            clear()
            print(f"Single Core test {colours.green()}initiated{colours.reset()}. This one takes a {colours.magenta()}while{colours.reset()}...")
            print("------")
            print("Stage 2: {}% done".format(percent))

        for number in range(item-100,item):
            result=math.sqrt(abs(number))

        oldPercent = percent

    end = time.perf_counter()
    stageTwo = end-start

    #Stage 3, goes through every element in the list, finds its square root then pops it.

    percent = 0
    oldPercent = 0

    clear()
    print(f"Don't {colours.red()}worry{colours.reset()} if this one takes ages.")
    print("------")
    print("Stage 3: {}% done".format(percent))

    start = time.perf_counter()

    i=0

    for item in numList:

        i+=1

        percent = oneSigFig((i/(SINGLENO/2))*100)

        if oldPercent != percent:
            clear()
            print(f"Don't {colours.red()}worry{colours.reset()} if this one takes ages.")
            print("------")
            print("Stage 3: {}% done".format(percent))

        result = math.sqrt(item)
        numList.pop(i-1)

        oldPercent = percent

    end=time.perf_counter()
    stageThree=end-start

    #Calculates the total time and score.

    totalTime = stageOne + stageTwo + stageThree
    avgTime = totalTime/3
    score = round((1/avgTime)*(math.e)*(1000*3))
    clear()

    if not dynamicMode and not fullTest:
        data = [[score, "", "", ""]]
        filename = "DATA/corebenchdata.csv"
        with open("DATA/corebenchdata.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(data)
    
    if showResults == True:
        if dynamicMode == True:
            print(f"{colours.grey()}DYNAMIC MODE IS ON{colours.reset()}")
            print("------")
        print(f"{colours.green()}Single Core Benchmark Complete!{colours.reset()} ({colours.grey()}{version}{colours.reset()})")
        print(f"{colours.magenta()}Total time{colours.reset()}: {totalTime} seconds")
        print(f"{colours.cyan()}Single core score{colours.reset()}: {score}")
    
    return score



#Multicore test
def multiCore(showResults): 
    p = psutil.Process(os.getpid())
    p.cpu_affinity(list(range(os.cpu_count())))
    #function to create the list
    def createList(threadNo):
        global N

        percent = 0
        oldPercent = 0

        newList = []

        print("[{}{}-sC{}] Building list...".format(colours.grey(), threadNo, colours.reset()))

        for x in range(0,N):

            newList.append(x)

            oldPercent = percent

        return newList


    #sqrts every number in the created list
    def intense1(threadNo):
        global N
        list = createList(threadNo)
        print("[{}{}-rC{}] Crunching numbers...".format(colours.cyan(), threadNo, colours.reset()))
    
        for x in range(0,5):
            for item in list:
    
                result = math.sqrt(item)
        print("[{}{}-cC{}] Instance complete!".format(colours.green(), threadNo, colours.reset()))
    #uses division
    def intense2(threadNo):
        global N, CPUs
        list = createList(threadNo)
        print("[{}{}-rC{}] Crunching numbers...".format(colours.cyan(), threadNo, colours.reset()))
    
        for x in range(0,5):
            for item in list:
    
                result = item/(item+1/(item+1/2))
        print("[{}{}-cC{}] Instance complete!".format(colours.green(), threadNo, colours.reset()))
    #checks for dynamic mode
    if dynamicMode == True:
        coreCount = int(CPUs)
    else:
        coreCount = 6

    #running process function (creates variable numbers of functions in dynamic mode)
    
    timeList = []

    print(f"This one {colours.cyan()}generally{colours.reset()} doesn't take too long.")
    print("------")

    if __name__ == "__main__":
        def run_processes():
            if __name__ == "__main__":
                global coreCount, CPUs, coreContext
    
                if dynamicMode == True:
                    coreCount = int(CPUs)
                else:
                    coreCount = 6
    
                processes = []
                ticker = 0
    
                for i in range(coreCount):
                    if ticker == 0:
                        p = coreContext.Process(target=intense1, args=(i+1,))
                        tecker = 1
                    elif ticker == 1:
                        p = coreContext.Process(target=intense2, args=(i+1,))
                        ticker = 0
                    if tecker == 1:
                        ticker = 1
    
                    processes.append(p)
                    p.start()
    
                for p in processes:
                    p.join()
                    
    #run the test 3 times
    for x in range(0,3):
        start=time.perf_counter()
        #run tests
        if __name__ == "__main__":     
            run_processes()

        end=time.perf_counter()
        Time = end-start
        timeList.append(Time)

    totalTime = 0
    for item in timeList:
        totalTime+=item

    avgTime = totalTime/3
    score = round((1/avgTime)*(math.e)*(1000*(1/math.log(coreCount+4,10))))
    clear()

    if not dynamicMode and not fullTest:
        data = [["", score, "", ""]]
        filename = "DATA/corebenchdata.csv"
        with open("DATA/corebenchdata.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(data)
        
    if showResults == True:
        if dynamicMode == True:
            print(f"{colours.grey()}DYNAMIC MODE IS ON{colours.reset()}")
            print("------")
        print(f"{colours.green()}Multi Core Test Complete!{colours.reset()} ({colours.grey()}{version}{colours.reset()})")
        print("------")
        print(f"{colours.magenta()}Total time{colours.reset()}: {totalTime} seconds")
        print(f"{colours.cyan()}Multi core score{colours.reset()}: {score} points")

    return score


#multithreading test, with the same basic algorithms as the multicore test
def multiThread(showResults):
    p = psutil.Process(os.getpid())
    p.cpu_affinity(list(range(os.cpu_count())))
    
    def createList(threadNo):
        global N

        percent = 0
        oldPercent = 0

        newList = []

        print("[{}{}-sT{}]Building list...".format(colours.grey(), threadNo, colours.reset()))

        for x in range(0,N):

            newList.append(x)

            oldPercent = percent

        return newList


    #sqrts every number in the created list
    def intense1(threadNo):

        global N

        list = createList(threadNo)

        print("[{}{}-rT{}] Crunching numbers...".format(colours.magenta(), threadNo, colours.reset()))

        for x in range(0,5):
            for item in list:
    
                result = math.sqrt(item)

        print("[{}{}-cT{}] Instance complete!".format(colours.green(), threadNo, colours.reset()))

    def intense2(threadNo):

        global N

        list = createList(threadNo)

        print("[{}{}-rT{}] Crunching numbers...".format(colours.magenta(), threadNo, colours.reset()))

        for x in range(0,5):
            for item in list:
    
                result = item/(item+1/(item+1/2))

        print("[{}{}-cT{}] Instance complete!".format(colours.green(), threadNo, colours.reset()))
        
    if __name__ == "__main__": 
        if dynamicMode == True:
            threadCount = Threads
            
        else:
            threadCount = 12
            
        def run_threads():
            global threadCount, Threads

            if dynamicMode == True:
                threadCount = int(Threads)
            else:
                threadCount = 12

            threads = []
            ticker = 0

            for i in range(threadCount):
                if ticker == 0:
                    t = threading.Thread(target=intense1, args=(i+1,))
                    tecker = 1
                elif ticker == 1:
                    t = threading.Thread(target=intense2, args=(i+1,))
                    ticker = 0
                if tecker == 1:
                    ticker = 1

                threads.append(t)
                t.start()

            for t in threads:
                t.join()
                
        timeList = []
        print(f"The {colours.red()}pain{colours.reset()} should be {colours.magenta()}over quickly{colours.reset()}...")
        print("------")
        for x in range(0,3):

            start=time.perf_counter()
            if __name__ == "__main__":
                run_threads()

            end=time.perf_counter()

            Time = end-start
            timeList.append(Time)

        print(timeList)

        totalTime = 0

        for item in timeList:
            totalTime+=item

        avgTime = totalTime/3

        score = round((1/avgTime)*(math.e)*(2000*(1/math.log(threadCount+8,10))))
        clear()

        if not dynamicMode and not fullTest:
            data = [["", "", score, ""]]
            filename = "DATA/corebenchdata.csv"
            with open("DATA/corebenchdata.csv", "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerows(data)
                
        if showResults == True:
            if dynamicMode == True:
                print(f"{colours.grey()}DYNAMIC MODE IS ON{colours.reset()}")
                print("------")
            print(f"{colours.green()}Multi Thread Test Complete!{colours.reset()} ({colours.grey()}{version}{colours.reset()})")
            print("------")
            print(f"{colours.magenta()}Total time{colours.reset()}: {totalTime} seconds")
            print(f"{colours.cyan()}Multi thread score{colours.reset()}: {score} points")

        return score


def fullCPUTest():
    global fullTest, brandName, version

    fullTest = True
    def clear():

        name = str(os.name)
        if name in ["nt","dos"]:
            os.system("cls")
        else:
            os.system("clear")

    def coolDown(points):
        os.system("clear")
        print(f"Allowing {colours.green()}time{colours.reset()} for {colours.cyan()}cooldown{colours.reset()}...")
        time.sleep(5)
        os.system("clear")
        print(f"Your system scored {colours.magenta()}{points}{colours.reset()} points on the {colours.red()}most recent test{colours.red()}.")
        time.sleep(5)
        os.system("clear")
        for x in range(0,3):
            if 3-x != 1:
                print(f"{colours.magenta()}{3-x}{colours.reset()} seconds...")
            else:
                print(f"{colours.magenta()}{3-x}{colours.reset()} second...")
            time.sleep(1)
            os.system("clear")
        
    singleCoreScore = singleCore(False)
    coolDown(singleCoreScore)
    multiCoreScore = multiCore(False)
    coolDown(multiCoreScore)
    multiThreadScore = multiThread(False)

    clear()
    
    totalScore = singleCoreScore+multiCoreScore+multiThreadScore
    finalScore = int(round(totalScore/3))

    if not dynamicMode:
        data = [[singleCoreScore, multiCoreScore, multiThreadScore, finalScore]]
        filename = "DATA/corebenchdata.csv"
        with open("DATA/corebenchdata.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(data)
    
    now = datetime.now()
    prettyDate = now.strftime("%d-%m-%y %H:%M")
    prettyDateUnderscore = now.strftime("%d-%m-%y_%H:%M")
    if dynamicMode == True:
        print(f"{colours.grey()}DYNAMIC MODE IS ON{colours.reset()}")
        print("------")
    print(f"{colours.green()}Overall CPU Performance Test Complete!{colours.reset()} ({colours.grey()}{version}{colours.reset()})")
    print("------")
    print(f"{colours.magenta()}Total points scored{colours.reset()}: {totalScore} || (S:{singleCoreScore}, M:{multiCoreScore}, MT:{multiThreadScore})")
    print(f"[{colours.cyan()}Overall score{colours.reset()}: {finalScore}]")

    try:
        with open("corebenchinfo.txt", "a") as f:
            if dynamicMode == False:
                f.write(f"\n\n({version}) {prettyDate} Results:\n------\nSingle Core: {singleCoreScore}\nMulti Core: {multiCoreScore}\nMulti Thread: {multiThreadScore}\nAverage Score: {finalScore}")
            else:
                f.write(f"\n\n{prettyDate} Results:\n------\nSingle Core: {singleCoreScore}\nMulti Core: {multiCoreScore}\nMulti Thread: {multiThreadScore}\nAverage Score: {finalScore}\n^^^ DYNAMIC MODE SCORE ^^^")
            f.flush()
    except Exception as e:
        print(f"{colours.red()}Error writing to file:{colours.reset()} {e}")

    
    #start data process here
    currentScores = [singleCoreScore, multiCoreScore, multiThreadScore]

    def avg(colName):
        file = open("DATA/corebenchdata.csv", "r", newline="", encoding="utf-8")
    
        reader = csv.reader(file)
    
        header = next(reader)
        col_index = header.index(colName)
    
        total = 0
        n = 0
        
        for row in reader:
            if str(row[col_index]).strip(" ") != "":
                total += int(row[col_index])
                n+=1
    
        avg = int(round(total/n))
        file.close()
        return avg

    singleAvg = avg("single")
    multiCoreAvg = avg("mcore")
    multiThreadAvg = avg("mthread")

    averageScores = [singleAvg, multiCoreAvg, multiThreadAvg]
    barNames = ["Single core", "Multicore", "Multithread"]
    
    x = np.arange(len(barNames))
    barWidth = 0.4
    fig, ax = plt.subplots(figsize = (8,5))


    current_bars = ax.bar(x - barWidth / 2, currentScores, width=barWidth, label = "Current Scores", color = "#26e2ec")

    for i, bar in enumerate(current_bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height,
                f"{currentScores[i]:.0f}", 
                ha="center", va="bottom")


    average_bars = ax.bar(x + barWidth / 2, averageScores, width = barWidth, label = "Average Scores", color = "#cd26ec")

    for i, bar in enumerate(average_bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height,
                f"{averageScores[i]:.0f}", 
                ha="center", va="bottom")

    ax.set_xticks(x)
    ax.set_xticklabels(barNames, rotation = 10)
    ax.legend()
    if dynamicMode:
        plt.title("DYNAMIC - CoreBench (v{}) {} results".format(version, brandName))
    else:
        plt.title("CoreBench (v{}) {} results".format(version, brandName))
    if dynamicMode:
        plt.savefig("DATA/DYNAMIC - corebenchdata_{}.png".format(prettyDateUnderscore))
    else:
        plt.savefig("DATA/corebenchdata_{}.png".format(prettyDateUnderscore))


def test_speed():
    try:
        print("Initiating internet speed test...")
        print("------")

        for x in range(0,10):
            try:
                st = speedtest.Speedtest()
                connected=True
                break
            except:
                connected=False
                pass
                
        if not connected:
            st = speedtest.Speedtest()
                
        clear()

        print(f"Test {colours.green()}initiated{colours.reset()}. This {colours.red()}shouldn't{colours.reset()} take too long.")
        print("------")
        downloads = []
        uploads = []
        pings = []
        
        print(f"[{colours.grey()}IS{colours.reset()}] Attempting connection to server...")
        st.get_best_server()
        
        for x in range(0,3):
            
    
            print(f"[{colours.cyan()}IS{colours.reset()}] Running download test...")
            download = st.download()/1e+6
            downloads.append(download)
    
            print(f"[{colours.cyan()}IS{colours.reset()}] Running upload test...")
            upload = st.upload()/1e+6
            uploads.append(upload)
    
            print(f"[{colours.cyan()}IS{colours.reset()}] Pinging server...")
            ping = st.results.ping
            pings.append(ping)
    
        clear()
        
        download = round(sum(downloads)/3,2)
        upload = round(sum(uploads)/3,2)
        ping = round(sum(pings)/3,2)
        

        score = int(round((((download+(upload*15)))/2)-ping))
        
        print(f"{colours.green()}Internet Speed Test Complete!{colours.reset()} ({colours.grey()}{version}{colours.reset()})")
        print(f"{colours.magenta()}Score{colours.reset()}: {score}")
        print("------")
        print(f"{colours.magenta()}Download speed{colours.reset()}: {download} {colours.cyan()}Mbps{colours.reset()}")
        print(f"{colours.cyan()}Upload speed{colours.reset()}: {upload} {colours.magenta()}Mbps{colours.reset()}")
        print(f"{colours.green()}Ping{colours.reset()}: {ping} {colours.cyan()}ms{colours.reset()}")

    except speedtest.ConfigRetrievalError as e:
        print(f"{colours.red()}Failed to connect to server.{colours.reset()}")
        print(f"{colours.grey()}This could potentially be a rate limit, please try again later.{colours.reset()}")
        f=open("error.txt","w")
        f.write(e)
        f.close()

if dynamicMode == True:
    print(f"{colours.grey()}DYNAMIC MODE IS ON{colours.reset()}")
    print("------")
print(f"Welcome back, {colours.green()}{user}{colours.reset()}!")
print(f"Version: {colours.grey()}{version}{colours.reset()}")
prettyPrintData()

if osName.lower() in ["nt", "dos", "windows"]:
    coreContext = multiprocessing.get_context("spawn")
    #Set process priority
    p = psutil.Process(os.getpid())

    p.nice(psutil.HIGH_PRIORITY_CLASS)
    
else:
    coreContext = multiprocessing.get_context("fork")


while True:
    fullTest = False
    p = psutil.Process(os.getpid())
    p.cpu_affinity(list(range(os.cpu_count())))
    
    temp = input(colours.grey()+"Press [ENTER] to continue..."+colours.reset())
    
    clear()
    
    time.sleep(0.1)
    
    #Main program
    '''
    sc - single core
    st - single core
    mc - multi core
    mt - multi thread
    nic - internet speed
    n - internet speed
    '''
    validChoice = ["sc", "st", "mc", "mt", "nic", "n", "fullc", "fc"]
    validArgs = ["d"]
    valid = False
    print(f"Please enter the {colours.magenta()}test command{colours.reset()}.")
    while not valid:
        args = None
        multiArgs = False
        skip = False
        
        choice = input("=> ")
        choice = choice.lower().strip(" ")
        try:
            #Checks to see if it contains args
            try:
                choice, args = choice.split(" -")
            except:
                choice, args = choice.split("-")
                
            multiArgs = True
            if choice in validChoice:
                skip = False
            else:
                skip = True
        except:
            #Has no args, gets sent here
            #If the choice is valid, it goes through the next validation process     
            if choice in validChoice:
                valid = True
                skip = False
            else:
                valid = False
                skip = True
        
        if not skip:
            if not multiArgs:
                dynamicMode = False
                valid = True
                #Checks for correct base but no args
            elif args == "d":
                dynamicMode = True
                valid = True
                #Dynamic mode
            else:
                dynamicMode = False
                valid = False
                #No valid arguments

        else:
            valid = False
            print(f"{colours.red()}Invalid command{colours.reset()}")
            #Invalid base

    base = choice
    
    if base in ["sc", "st"]:
        index = 0
    elif base == "mc":
        index = 1
    elif base == "mt":
        index = 2
    elif base in ["fullc", "fc"]:
        index = 3
    elif base in ["n", "nic"]:
        index = 4
        
    if index == 0:
        singleCore(True)
        prettyPrintData()
    elif index == 1:
        multiCore(True)
        prettyPrintData()
    elif index == 2:
        multiThread(True)
        prettyPrintData()
    elif index == 3:
        fullCPUTest()
        prettyPrintData()
    elif index == 4:
        test_speed()
        prettyPrintData()
