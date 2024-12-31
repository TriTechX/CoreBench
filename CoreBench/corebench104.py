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
#Third-party packages
import cpuinfo
import psutil
import GPUtil
from pick import pick
import distro
#Custom packages
import colours

osName = platform.system()
memRaw = round(((psutil.virtual_memory().total)/(1e+6)))
brandName = cpuinfo.get_cpu_info()["brand_raw"]
hostname = socket.gethostname()
localIp = socket.gethostbyname(socket.gethostname())

### ZONE OF EXPERIMENTATION ###
### END OF ZONE ###

if str(os.name) in ["nt", "dos"]:
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
    

#Get system information
def getData():
    try:
    
        global hostname, GPUs, osName, architecture, brandName, clockSpeed, CPUs, memRaw, memory, endLoad, distroName, localIp, Threads, threadsPerCore, osNamePretty
        
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
        else:
            osNamePretty=osName
            
    except Exception as e:
        f=open("log.txt","w")
        f.write(e)
        f.close()

    endLoad = True

messages = ["So, you're back...", "Hello there!", "It's hot in here...", "400FPS", "Disabling frame generation...", "RTX ON", "Removing nanites...", "Stealing your personal information...", "Pro tip: bench", "Sussy Bucket", "No standard users allowed!", "Connecting to the (totally functional) CoreBench database...", "Getting more ping...", "Optimizing...", "Initiating...", "WELCOME.", f"Here with your {brandName} I see...", f"{osName}? A fellow man of culture...", f"Eating all {memRaw}MB of RAM...", "Overclocking...", "Deleting main.py...", "Always remember to remove the French language pack!", f"Not much of a {osName} fan myself, but you do you...", f"Welcome back {hostname}.", f"Haha! Got your IP! Seriously! {localIp}", "I use Arch btw", "I use Core btw"]

message = messages[random.randint(0,len(messages)-1)]

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
            print(colours.grey() + "© TriTech 2024 - If you paid for this software, get a refund.\n" + colours.reset())
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
            print(colours.grey() + "© TriTech 2024 - If you paid for this software, get a refund.\n" + colours.reset())
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
            print(colours.grey() + "© TriTech 2024 - If you paid for this software, get a refund.\n" + colours.reset())
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
    
        print("Load done!")
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

    if osName in ["Linux"]:
        print(f"{colours.magenta()}OS Name{colours.reset()}: {osNamePretty}")
    else:
        print(f"{colours.magenta()}OS Name{colours.reset()}: {osNamePretty}")
    
    print(f"{colours.cyan()}Architecture{colours.reset()}: {architecture}")
    
    
    print("------")
    
    
    print(f"{colours.magenta()}CPU name{colours.reset()}: {cpuColour}{brandName}{colours.reset()}")
    
    
    print(f"{colours.cyan()}CPU clock speed{colours.reset()}: {clockSpeed}")
    
    
    print(f"{colours.green()}CPUs{colours.reset()}: {CPUs} Cores")
    print(f"{colours.green()}Threads{colours.reset()}: {Threads} Threads")
    
    print("------")
    
    
    print(f"{colours.magenta()}RAM{colours.reset()}: {memory}{colours.cyan()} GB{colours.reset()}")
    
    print("------")
    
    for gpu in GPUs:
        print(f"{colours.cyan()}GPU Name{colours.reset()}: {gpu.name}")
        print(f"{colours.magenta()}VRAM{colours.reset()}: {gpu.memoryTotal} MB")


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

if not os.path.exists(filename):
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
#write specifications to a file
#single core CPU test
def singleCore(showResults):
    global N
    numList = []

    #Stage 1, adds all the numbers to a list

    percent = 0
    oldPercent = 0
    print(f"Single Core test {colours.green()}initiated{colours.reset()}. This one takes a {colours.magenta()}while{colours.reset()}...")
    print("------")
    print("Stage 1: {}% done".format(percent))

    start = time.perf_counter()

    for x in range(0,N):

        percent = int(round((x/1000000)*100,0))

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

        percent = round(i/1000000*100)

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

        percent = round(i/500000*100)

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
    averageTime = totalTime/3
    score = round(((1/averageTime)*10000)*3)
    clear()

    if showResults == True:
        
        print(f"{colours.green()}Single Core Benchmark Complete!{colours.reset()}")
        print(f"{colours.magenta()}Total time{colours.reset()}: {totalTime} seconds")
        print(f"{colours.cyan()}Single core score{colours.reset()}: {score}")
    
    return score



#Multicore test
def multiCore(showResults): 

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

    def intense2(threadNo):
    
        global N
    
        list = createList(threadNo)
    
        print("[{}{}-rC{}] Crunching numbers...".format(colours.cyan(), threadNo, colours.reset()))
    
        for x in range(0,5):
            for item in list:
    
                result = item/(item+1/(item+1/2))

    if __name__ == "__main__": 
        def run_processes():
            core1 = multiprocessing.Process(target=intense1, args=(1,))
            core2 = multiprocessing.Process(target=intense2, args=(2,))
            core3 = multiprocessing.Process(target=intense1, args=(3,))
            core4 = multiprocessing.Process(target=intense2, args=(4,))

            core1.start()
            core2.start()
            core3.start()
            core4.start()

            core1.join()
            core2.join()
            core3.join()
            core4.join()

        timeList = []

        print(f"This one {colours.cyan()}generally{colours.reset()} doesn't take too long.")
        print("------")
        for x in range(0,3):
            start=time.perf_counter()

            run_processes()

            end=time.perf_counter()
            Time = end-start
            timeList.append(Time)

        totalTime = 0
        for item in timeList:
            totalTime+=item

        avgTime = totalTime/3
        score = round((1/avgTime)*(math.e)*1000)
        clear()

        if showResults == True:
            print(f"{colours.green()}Multi Core Test Complete!{colours.reset()}")
            print("------")
            print(f"{colours.magenta()}Total time{colours.reset()}: {totalTime} seconds")
            print(f"{colours.cyan()}Multi core score{colours.reset()}: {score} points")

        return score


#multithreading test, with the same basic algorithms as the multicore test
def multiThread(showResults):

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

    def intense2(threadNo):

        global N

        list = createList(threadNo)

        print("[{}{}-rT{}] Crunching numbers...".format(colours.magenta(), threadNo, colours.reset()))

        for x in range(0,5):
            for item in list:
    
                result = item/(item+1/(item+1/2))

    if __name__ == "__main__": 

        def run_threads():
            thread1 = threading.Thread(target=intense1, args=(1,))
            thread2 = threading.Thread(target=intense2, args=(2,))
            thread3 = threading.Thread(target=intense1, args=(3,))
            thread4 = threading.Thread(target=intense2, args=(4,))

            thread1.start()
            thread2.start()
            thread3.start()
            thread4.start()

            thread1.join()
            thread2.join()
            thread3.join()
            thread4.join()

        timeList = []
        print(f"The {colours.red()}pain{colours.reset()} should be {colours.magenta()}over quickly{colours.reset()}...")
        print("------")
        for x in range(0,3):

            start=time.perf_counter()

            run_threads()

            end=time.perf_counter()

            Time = end-start
            timeList.append(Time)

        print(timeList)

        totalTime = 0

        for item in timeList:
            totalTime+=item

        avgTime = totalTime/3

        score = round((1/avgTime)*(math.e)*1000)
        clear()

        if showResults == True:
            print(f"{colours.green()}Multi Thread Test Complete!{colours.reset()}")
            print("------")
            print(f"{colours.magenta()}Total time{colours.reset()}: {totalTime} seconds")
            print(f"{colours.cyan()}Multi thread score{colours.reset()}: {score} points")

        return score


def fullCPUTest():
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
            print(f"{colours.magenta()}{3-x}{colours.reset()} seconds...")
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
    
    now = datetime.now()
    prettyDate = now.strftime("%d-%m-%y %H:%M")
    
    print(f"{colours.green()}Overall CPU Performance Test Complete!{colours.reset()}")
    print("------")
    print(f"{colours.magenta()}Total points scored{colours.reset()}: {totalScore} || (S:{singleCoreScore}, M:{multiCoreScore}, MT:{multiThreadScore})")
    print(f"{colours.cyan()}Overall score{colours.reset()}: {finalScore}")

    f=open("corebenchinfo.txt","a")
    f.write(f"\n\n{prettyDate} Results:\n------\nSingle Core: {singleCoreScore}\nMulti Core: {multiCoreScore}\nMulti Thread: {multiThreadScore}\nAverage Score: {finalScore}")
    f.close()


prettyPrintData()

while True:
    temp = input(colours.grey()+"Press [ENTER] to continue..."+colours.reset())
    
    clear()
    
    time.sleep(1)
    
    #Main program
    
    question = "Please select the test you wish to perform"
    choices = ["CPU: Single core & thread test", "CPU: Multi core test", "CPU: Multi thread test", "CPU: Full test"]
    
    option, index = pick(choices, question, indicator='=>', default_index=0)
        
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
