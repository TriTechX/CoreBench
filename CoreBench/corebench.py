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
import sys
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

# s'il vous plaît exterminer la vermine mercy bookoooooooo
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
    sys.stdout.write("\033c") 
    sys.stdout.flush()

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
if checkRoot():
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
            
            def get_advertised_cpu_clock():
                try:
                    output = subprocess.check_output("lscpu", shell=True, text=True)
                    for line in output.split("\n"):
                        if "CPU max MHz" in line:  # Find the max advertised MHz
                            max_mhz = float(line.split(":")[1].strip().split()[0])  # Extract and convert to float
                            return f"{max_mhz/1000:.2f} GHz"  # Convert MHz to GHz and round to 2 decimal places
                except Exception as e:
                    return str(e)
            
            clockSpeed = get_advertised_cpu_clock()
            CPUs = psutil.cpu_count(logical=False)
            Threads = os.cpu_count()
            threadsPerCore= int(os.cpu_count())/int(CPUs)
            memRaw = round(((psutil.virtual_memory().total)/(1024**2)))
            memory = math.ceil(((psutil.virtual_memory().total)/(1024**3)))

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
            print(f"A fatal error ocurred.\n{e}")
            quit()
            
        #UPDATE THIS WITH EVERY VERSION
        version = "1.3.1"
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
        print(f"A fatal error ocurred.\n{e}")
        quit()

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
    if GPUs:
        print("------")

if len(GPUs)>0:
    gpuPresent = True
else:
    gpuPresent = False


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

#single core test algorithm rewrite
def singleCoreCheck():
    p = psutil.Process(os.getpid())
    
    validCore = False
    try: #try
        p.cpu_affinity([0])
        validCore = True
    except: #try harder
        for item in p.cpu_affinity():
            if validCore == True:
                break
            else:
                try:
                    p.cpu_affinity([item])
                    validCore = True
                except:
                    p.cpu_affinity(list(range(os.cpu_count()))) #reset

    if validCore == False:
        quit() #give up

def singleCore(showResults):
    global CPUs, fullTest

    singleCoreCheck()

    if dynamicMode == True:
        coreCount = CPUs
    else:
        coreCount = 6

    scoreList = []
    timeList = []

    percentageComplete = 0

    ballHeight = 5000
    
    GFLUCTUATION = random.randint(-10,10)/10
    ACCELERATION = 9.81+GFLUCTUATION
    BOUNCECONSTANT = random.randint(1, 10)

    timeSimulated = 0
    timeIncrement = 1e-6
    distanceTravelled = 0


    timeToHit = math.sqrt(ballHeight/(0.5*ACCELERATION))

    ticker = -1

    timeList = []

    start = time.perf_counter()

    for x in range(0,3):

        ticker += 1
        yVel = 0
        timeSimulated = 0
        oldPercentageComplete = -1

        roundStart = time.perf_counter()
        while distanceTravelled < ballHeight:

            percentageComplete = ((math.sqrt(distanceTravelled) / math.sqrt(ballHeight)) * (100 / 3)) + ((100 / 3) * ticker)
            percentageComplete = round(percentageComplete,0)

            if oldPercentageComplete != percentageComplete:
                clear()
                buffer = []

                buffer.append(f"{colours.cyan()}Stage 1{colours.reset()} in progress...")
                buffer.append("[{}{}-sS{}] {}% Done".format(colours.grey(),1,colours.reset(),int(round(percentageComplete))))
                try:
                    timeElapsed = time.perf_counter()-roundStart
                    buffer.append("------")
                    buffer.append("{}Round {} stats{}:".format(colours.green(),ticker+1,colours.reset()))
                    buffer.append("---")
                    buffer.append(f"{colours.magenta()}Velocity{colours.reset()}: {round(-yVel,2)}m/s")
                    buffer.append(f"{colours.magenta()}Distance{colours.reset()}: {round(distanceTravelled,2)}m")
                    buffer.append(f"{colours.magenta()}Time simulated{colours.reset()}: {round(timeSimulated,2)}s")
                    buffer.append("---")
                    buffer.append(f"{colours.magenta()}Time elapsed{colours.reset()}: {int(round(timeElapsed))}s")
                    print("\n".join(buffer))
                except:
                    pass

            oldPercentageComplete = percentageComplete

            yVel = yVel-timeIncrement*ACCELERATION
            timeSimulated+=timeIncrement

            
            distanceTravelled = 0.5 * ACCELERATION * timeSimulated**2

        yVel = -yVel - (BOUNCECONSTANT)

        timeList.append(timeSimulated)

        u = yVel
        a = ACCELERATION

        distanceTravelled = 0
        estimatedHeight =  (u**2)/(2*a)

    end = time.perf_counter()

    totalTime = end-start
    avgTime = (end-start)/3
    score = round((1/(avgTime/(3*math.e)))*(math.e)*(1000*(1/math.log(coreCount+4,10))))

    allPassTimeAvg = sum(timeList)/3
    allPassTimeAvg = float(str(allPassTimeAvg).rstrip("0").rstrip("."))

    #Stage 1 algorithm end#

    percentageAccuracy = 100.0 - (((allPassTimeAvg-timeToHit)/timeToHit) *100.0)

    print("---")
    print(f"{colours.green()}Stage 1 complete{colours.reset()}.")
    print(f"{colours.magenta()}Physics simulation accuracy{colours.reset()}: {round(percentageAccuracy)}%")

    scoreList.append(score)
    timeList.append(totalTime)
    
    time.sleep(3)

    #Stage 2

    percentageComplete = 0

    arrowHeight = 5000
    
    GFLUCTUATION = random.randint(-10,10)/10
    ACCELERATION = 9.81+GFLUCTUATION

    timeSimulated = 0
    timeIncrement = 1e-6

    yDistanceTravelled = 0
    xDistanceTravelled = 0

    yVel = 0
    xVel = 50

    timeToHit = math.sqrt(arrowHeight/(0.5*ACCELERATION))

    ticker = -1

    timeList = []
    oldPercentageComplete = -1

    start = time.perf_counter()

    for x in range(0,3):

        ticker+=1
        yVel = 0
        yDistanceTravelled = 0
        xDistanceTravelled = 0
        timeSimulated = 0

        roundStart = time.perf_counter()
        while yDistanceTravelled < arrowHeight:

            percentageComplete = ((math.sqrt(yDistanceTravelled) / math.sqrt(arrowHeight)) * (100 / 3)) + ((100 / 3) * ticker)

            if round(oldPercentageComplete) != round(percentageComplete):
                clear()
                buffer = []

                buffer.append(f"{colours.cyan()}Stage 2{colours.reset()} in progress...")
                buffer.append("[{}{}-sS{}] {}% Done".format(colours.grey(),2,colours.reset(),int(round(percentageComplete))))
                try:
                    timeElapsed = time.perf_counter()-roundStart
                    buffer.append("------")
                    buffer.append("{}Round {} stats{}:".format(colours.green(),ticker+1,colours.reset()))
                    buffer.append("---")
                    buffer.append(f"{colours.magenta()}Angle{colours.reset()}: {round(angle,2)}°")
                    buffer.append(f"{colours.magenta()}Y velocity{colours.reset()}: {round(-yVel,2)}m/s")
                    buffer.append(f"{colours.magenta()}Distance fallen{colours.reset()}: {round(yDistanceTravelled,2)}m")
                    buffer.append(f"{colours.magenta()}Time simulated{colours.reset()}: {round(timeSimulated,2)}s")
                    buffer.append(f"{colours.magenta()}Resultant velocity{colours.reset()}: {round(resultantVelocity,2)}m/s")
                    buffer.append("---")
                    buffer.append(f"{colours.magenta()}Time elapsed{colours.reset()}: {int(round(timeElapsed))}")
                    print("\n".join(buffer))
                except:
                    pass
            
            oldPercentageComplete = percentageComplete

            yVel = yVel - timeIncrement*ACCELERATION

            timeSimulated+=timeIncrement
            yDistanceTravelled = 0.5 * ACCELERATION * timeSimulated**2

            xDistanceTravelled = xVel*timeSimulated

            angle = -math.atan2(yVel,xVel)*(180/math.pi) #radians to degrees
            resultantVelocity = math.sqrt(yVel**2+xVel**2) #calculates the resultant velocity
    end = time.perf_counter()

    totalTime = end-start
    avgTime = (end-start)/3
    score = round((1/(avgTime/(3*math.e)))*(math.e)*(1000*(1/math.log(coreCount+4,10))))

    print("---")
    print(f"{colours.green()}Stage 2 complete{colours.reset()}.")

    scoreList.append(score)
    timeList.append(totalTime)

    time.sleep(3)

    #Stage 3: calculate GFLOPS of one core
    N = 1024
    matA = np.random.rand(N, N)
    matB = np.random.rand(N, N)

    start = time.perf_counter()

    oldPercentageComplete = -1
    I = 5000

    for _ in range(3):
        matC = np.dot(matA,matB) # warmup avoiding CPU frequency scaling issues

    gflopData = []
    ticker = 0

    for x in range(I):
        startTemp = time.perf_counter_ns()
        percentageComplete = (x/I)*100

        if int(round(oldPercentageComplete)) != int(round(percentageComplete)):
            clear()
            buffer = []
            buffer.append(f"{colours.cyan()}Stage 3{colours.reset()} in progress...")
            buffer.append("[{}{}-sS{}] {}% Done".format(colours.grey(),3,colours.reset(),int(round(percentageComplete))))

            try:
                buffer.append("------")
                buffer.append(f"{colours.green()}Stats{colours.reset()}:")
                buffer.append("---")
                buffer.append(f"{colours.magenta()}GFLOPs for last run{colours.reset()}: {round(flopTemp/1000000000,2)}")
                print("\n".join(buffer))
            except:
                pass

        
        oldPercentageComplete = percentageComplete

        matC = np.dot(matA, matB)  # Matrix multiplication

        endTemp = time.perf_counter_ns()

        flopTemp = (2 * N**3) / (endTemp/1000000000 - startTemp/1000000000)
        gflopTemp = flopTemp/1000000000

        ticker +=1

        gflopData.append(gflopTemp)

    end = time.perf_counter()

    #compute the mean
    gflopAvg = sum(gflopData)/len(gflopData)

    #calculate the standard deviation from the mean
    stdDeviationNumerator = 0

    for item in gflopData:
        value = (item-gflopAvg)**2
        stdDeviationNumerator += value
    
    stdDeviation = math.sqrt(stdDeviationNumerator/len(gflopData))

    #calculate the Z-score for each point
    gflopNormalised = []
    discarded = []
    for item in gflopData:
        zScore = (item-gflopAvg)/(stdDeviation)

        if zScore < 2 and zScore > -2:
            gflopNormalised.append(item)
        else:
            discarded.append(item)
            pass # <-- too anomalous, discarded

    gflopAvgNormalised = sum(gflopNormalised)/len(gflopNormalised)
    percentDiscarded = (len(discarded)/len(gflopData))*100

    totalTime = end-start
    avgTime = totalTime/6 #not avg but idgaf
    score = round((1/(avgTime/(3*math.e)))*(math.e)*(1000*(1/math.log(coreCount+4,10))))

    timeList.append(totalTime)
    scoreList.append(score)

    flops = (2 * N**3) / ((end - start)/I)
    
    gflops = gflopAvgNormalised

    cpu_freq = psutil.cpu_freq().current * 1e6
    flop_per_cycle = (gflops * 1e9) / cpu_freq
    
    cpuTypeList = ["AVX", "AVX2", "AVX-512", "SSE"]
    cpuTypeFlop = [8,16,32,4]

    index = min(range(len(cpuTypeFlop)), key=lambda i: abs(cpuTypeFlop[i] - flop_per_cycle))
    cpuType = cpuTypeList[index]

    print(f"{colours.cyan()}FLOP per cycle{colours.reset()}: {round(flop_per_cycle,2)}")
    print(f"{colours.green()}Estimated SIMD Instruction Set{colours.reset()}: {cpuType}")
    print("---")
    print(f"{colours.magenta()}GFLOPs Performance{colours.reset()}: {round(gflops,2)}")
    print(f"{colours.green()}Stage 3 complete{colours.reset()}.")
    print("------")
    print(f"{colours.cyan()}Discarded values: {percentDiscarded}%")
    time.sleep(3)

    clear()

    score = int(round(sum(scoreList)/3))
    totalTime = sum(timeList)
    
    if not dynamicMode and not fullTest:
        data = [[score, "", "", ""]]
        filename = "DATA/corebenchdata.csv"
        with open(filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(data)

    if showResults == True:
        if dynamicMode == True:
            print(f"{colours.grey()}DYNAMIC MODE IS ON{colours.reset()}")
            print("------")
        print(f"{colours.green()}Single Core Benchmark Complete!{colours.reset()} ({colours.grey()}{version}{colours.reset()})")
        print(f"{colours.magenta()}Total time{colours.reset()}: {totalTime} seconds")
        print(f"{colours.cyan()}Single core score{colours.reset()}: {score}")
        print("---")
        print(f"{colours.green()}Floating point operations performance{colours.reset()}: {round(gflops,2)} GFLOPs")
    
    return score


#Multicore test
def multiCore(showResults): 
    p = psutil.Process(os.getpid())
    p.cpu_affinity(list(range(os.cpu_count())))

    def intense1(threadNo):
        print("[{}{}-rC{}] Crunching numbers...".format(colours.cyan(), threadNo, colours.reset()))
    
        ballHeight = 500
        
        GFLUCTUATION = random.randint(-10,10)/10
        ACCELERATION = 9.81+GFLUCTUATION
        BOUNCECONSTANT = random.randint(1, 10)

        timeSimulated = 0
        timeIncrement = 1e-6
        distanceTravelled = 0

        yVel = 0


        timeToHit = math.sqrt(ballHeight/(0.5*ACCELERATION))

        while distanceTravelled < ballHeight:

            yVel = yVel-timeIncrement*ACCELERATION
            timeSimulated+=timeIncrement

            
            distanceTravelled = 0.5 * ACCELERATION * timeSimulated**2

        yVel = -yVel - (BOUNCECONSTANT)

        timeList.append(timeSimulated)

        u = yVel
        a = ACCELERATION

        distanceTravelled = 0

        estimatedHeight =  (u**2)/(2*a)

        print("[{}{}-cC{}] Instance complete!".format(colours.green(), threadNo, colours.reset()))
    
    def intense2(threadNo):
        print("[{}{}-rC{}] Crunching numbers...".format(colours.cyan(), threadNo, colours.reset()))

        arrowHeight = 500
        
        GFLUCTUATION = random.randint(-10,10)/10
        ACCELERATION = 9.81+GFLUCTUATION

        timeSimulated = 0
        timeIncrement = 1e-6

        yDistanceTravelled = 0
        xDistanceTravelled = 0

        yVel = 0
        xVel = 50

        timeToHit = math.sqrt(arrowHeight/(0.5*ACCELERATION))

        while yDistanceTravelled < arrowHeight:

            yVel = yVel - timeIncrement*ACCELERATION

            timeSimulated+=timeIncrement
            yDistanceTravelled = 0.5 * ACCELERATION * timeSimulated**2

            xDistanceTravelled = xVel*timeSimulated

            angle = -math.atan2(yVel,xVel)*(180/math.pi) #radians to degrees
            resultantVelocity = math.sqrt(yVel**2+xVel**2) #calculates the resultant velocity
        
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
                        ticker = 1
                    elif ticker == 1:
                        p = coreContext.Process(target=intense2, args=(i+1,))
                        ticker = 0
    
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
    score = round((1/(avgTime/(math.e/2))*(math.e)*(1000*(1/math.log(coreCount+4,10)))))
    clear()

    if not dynamicMode and not fullTest:
        data = [["", score, "", ""]]
        filename = "DATA/corebenchdata.csv"
        with open(filename, "a", newline="", encoding="utf-8") as file:
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


    def intense1(threadNo):
        print("[{}{}-rT{}] Crunching numbers...".format(colours.magenta(), threadNo, colours.reset()))
    
        ballHeight = 250
        
        GFLUCTUATION = random.randint(-10,10)/10
        ACCELERATION = 9.81+GFLUCTUATION
        BOUNCECONSTANT = random.randint(1, 10)

        timeSimulated = 0
        timeIncrement = 1e-6
        distanceTravelled = 0

        yVel = 0


        timeToHit = math.sqrt(ballHeight/(0.5*ACCELERATION))

        while distanceTravelled < ballHeight:

            yVel = yVel-timeIncrement*ACCELERATION
            timeSimulated+=timeIncrement

            
            distanceTravelled = 0.5 * ACCELERATION * timeSimulated**2

        yVel = -yVel - (BOUNCECONSTANT)

        timeList.append(timeSimulated)

        u = yVel
        a = ACCELERATION

        distanceTravelled = 0

        estimatedHeight =  (u**2)/(2*a)

        print("[{}{}-cT{}] Instance complete!".format(colours.green(), threadNo, colours.reset()))

    
    def intense2(threadNo):
        print("[{}{}-rT{}] Crunching numbers...".format(colours.magenta(), threadNo, colours.reset()))

        arrowHeight = 250
        
        GFLUCTUATION = random.randint(-10,10)/10
        ACCELERATION = 9.81+GFLUCTUATION

        timeSimulated = 0
        timeIncrement = 1e-6

        yDistanceTravelled = 0
        xDistanceTravelled = 0

        yVel = 0
        xVel = 50

        timeToHit = math.sqrt(arrowHeight/(0.5*ACCELERATION))

        while yDistanceTravelled < arrowHeight:

            yVel = yVel - timeIncrement*ACCELERATION

            timeSimulated+=timeIncrement
            yDistanceTravelled = 0.5 * ACCELERATION * timeSimulated**2

            xDistanceTravelled = xVel*timeSimulated

            angle = -math.atan2(yVel,xVel)*(180/math.pi) #radians to degrees
            resultantVelocity = math.sqrt(yVel**2+xVel**2) #calculates the resultant velocity
        
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
                    ticker = 1
                elif ticker == 1:
                    t = threading.Thread(target=intense2, args=(i+1,))
                    ticker = 0

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

        score = round((1/(avgTime/(math.e/1.3))*(math.e)*(2000*(1/math.log(threadCount-2,10)))))
        clear()

        if not dynamicMode and not fullTest:
            data = [["", "", score, ""]]
            filename = "DATA/corebenchdata.csv"
            with open(filename, "a", newline="", encoding="utf-8") as file:
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

    def coolDown(points):
        clear()
        print(f"Allowing {colours.green()}time{colours.reset()} for {colours.cyan()}cooldown{colours.reset()}...")
        time.sleep(5)
        clear()
        print(f"Your system scored {colours.magenta()}{points}{colours.reset()} points on the {colours.red()}most recent test{colours.red()}.")
        time.sleep(5)
        clear()
        for x in range(0,3):
            if 3-x != 1:
                print(f"{colours.magenta()}{3-x}{colours.reset()} seconds...")
            else:
                print(f"{colours.magenta()}{3-x}{colours.reset()} second...")
            time.sleep(1)
            clear()
        
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
        with open(filename, "a", newline="", encoding="utf-8") as file:
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
            if choice.strip(" ") != "":
                print(f"{colours.red()}Invalid command{colours.reset()}")
            else:
                clear()
                print(f"Please enter the {colours.magenta()}test command{colours.reset()}.")
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
