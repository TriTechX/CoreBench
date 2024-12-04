#Built-in packages
import time
import os
import socket
import multiprocessing
import threading
import math
import platform
#Third-party packages
import cpuinfo
import psutil
import GPUtil
from pick import pick
#Custom packages
import colours

#Get system information
def getData():
    
    global hostname, GPUs, osName, architecture, brandName, clockSpeed, CPUs, memRaw, memory, endLoad
    
    hostname = socket.gethostname()
    GPUs = GPUtil.getGPUs()
    osName = platform.system()
    architecture = platform.machine()
    brandName = cpuinfo.get_cpu_info()["brand_raw"]
    clockSpeed = cpuinfo.get_cpu_info()["hz_advertised_friendly"]
    CPUs = os.cpu_count()
    memRaw = round(((psutil.virtual_memory().total)/(1e+6)))
    memory = round(((psutil.virtual_memory().total)/(1e+9)),2)

    endLoad = True

def loadingScreen():
    
    def clear():
        
        name = str(os.name)
        if name == "nt":
            os.system("cls")
        else:
            os.system("clear")
    
    global endLoad

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
        time.sleep(0.3)
        clear()

if __name__ == "__main__":
    grep = threading.Thread(target=getData)
    load = threading.Thread(target=loadingScreen)

    endLoad = False
    
    grep.start()
    load.start()

    grep.join()
    load.join()

    print("Load done!")

def prettyPrintData():
    print("------")

    
    print(f"{colours.magenta()}OS Name{colours.reset()}: {osName}")
    
    
    print(f"{colours.cyan()}Architecture{colours.reset()}: {architecture}")
    
    
    print("------")
    
    
    print(f"{colours.magenta()}CPU name{colours.reset()}: {brandName}")
    
    
    print(f"{colours.cyan()}CPU clock speed{colours.reset()}: {clockSpeed}")
    
    
    print(f"{colours.green()}CPUs{colours.reset()}: {CPUs} cores")
    
    print("------")
    
    
    print(f"{colours.magenta()}RAM{colours.reset()}: {memory}{colours.cyan()} GB{colours.reset()}")
    
    print("------")
    
    for gpu in GPUs:
        print(f"{colours.cyan()}GPU Name{colours.reset()}: {gpu.name}")
        print(f"{colours.magenta()}VRAM{colours.reset()}: {gpu.memoryTotal} MB")


#set clear() to clear the screen
def clear():
    os.system("clear")

N = 1000000
#intensity of the test, point system will not scale with intensity

f=open("corebenchinfo.txt", "w")
f.close()
os.remove("corebenchinfo.txt")
f=open("corebenchinfo.txt", "w")

f.write("OS Name: " + str(osName) + "\n")
f.write("Architecture: " + str(architecture) + "\n")
f.write("CPU Name: " + str(brandName) + "\n")
f.write("CPU clock speed: " + str(clockSpeed) + "\n")
f.write("CPUs: " + str(CPUs) + "\n")
f.write("RAM: " + str(memRaw) + " MB\n")
for gpu in GPUs:
    f.write("GPU Name: " + str(gpu.name) + "\n")
    f.write("GPU Name: " + str(gpu.memoryTotal) + " MB\n")
f.close()
#write specifications to a file
#single core CPU test
def singleCore():
    global N
    numList = []

    #Stage 1, adds all the numbers to a list

    percent = 0
    oldPercent = 0

    print("Stage 1: {}% done".format(percent))

    start = time.perf_counter()

    for x in range(0,N):

        percent = int(round((x/1000000)*100,0))

        if oldPercent != percent:
            clear()
            print("Stage 1: {}% done".format(percent))

        numList.append(x)

        oldPercent = percent

    end = time.perf_counter()
    stageOne = end-start
    #Stage 2, finds the square root of all of those numbers

    percent = 0
    oldPercent = 0

    clear()
    print("Stage 2: {}% done".format(percent))

    start = time.perf_counter()

    i=0

    for item in numList:

        i+=1

        percent = round(i/1000000*100)

        if oldPercent != percent:
            clear()
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
    print("Stage 3: {}% done".format(percent))

    start = time.perf_counter()

    i=0

    for item in numList:

        i+=1

        percent = round(i/500000*100)

        if oldPercent != percent:
            clear()
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

    print(f"{colours.green()}Single Core Benchmark Complete!{colours.reset()}")
    print(f"{colours.magenta()}Total time{colours.reset()}: {totalTime} seconds")
    print(f"{colours.cyan()}Single Core Score{colours.reset()}: {score}")
    
    return score



#Multicore test
def multiCore(): 

    #function to create the list
    def createList():
        global N

        percent = 0
        oldPercent = 0

        newList = []

        print("Stage 1 (not measured): {}% done".format(percent))

        for x in range(0,N):

            percent = round((x/N)*100)

            if oldPercent != percent:
                clear()
                print("Stage 1 (not measured): {}% done".format(percent))

            newList.append(x)

            oldPercent = percent

        return newList


    #sqrts every number in the created list
    def intense1():
        def oneSgFg(x):
            return round(x, -int(math.floor(math.log10(abs(x)))))

        global N

        list = createList()

        percent = 0
        oldPercent = 0

        print("Stage 2: {}% done".format(percent))

        i=0

        for item in list:
            i+=1

            percent = int(oneSgFg(((i/N)*100)))

            if oldPercent != percent:
                clear()
                print("Stage 2: {}% done".format(percent))

            result = math.sqrt(item)

            oldPercent = percent

    def intense2():
        def oneSgFg(x):
            return round(x, -int(math.floor(math.log10(abs(x)))))

        global N

        list = createList()

        percent = 0
        oldPercent = 0

        print("Stage 2: {}% done".format(percent))

        i=0

        for item in list:
            i+=1

            percent = int(oneSgFg(((i/N)*100)))

            if oldPercent != percent:
                clear()
                print("Stage 2: {}% done".format(percent))

            result = item/(item+1/(item+1/2))

            oldPercent = percent

    if __name__ == "__main__": 
        def run_processes():
            core1 = multiprocessing.Process(target=intense1)
            core2 = multiprocessing.Process(target=intense2)
            core3 = multiprocessing.Process(target=intense1)
            core4 = multiprocessing.Process(target=intense2)

            core1.start()
            core2.start()
            core3.start()
            core4.start()

            core1.join()
            core2.join()
            core3.join()
            core4.join()

        timeList = []
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
        score = round((1/avgTime)*10000)
        clear()

        print(f"{colours.green()}Multicore Test Complete!{colours.reset()}")
        print("------")
        print(f"{colours.magenta()}Total time{colours.reset()}: {totalTime} seconds")
        print(f"{colours.cyan()}Score{colours.reset()}: {score} points")

        return score


#multithreading test, with the same basic algorithms as the multicore test
def multiThread():

    def createList():
        global N

        percent = 0
        oldPercent = 0

        newList = []

        print("Stage 1 (not measured): {}% done".format(percent))

        for x in range(0,N):

            percent = round((x/N)*100)

            if oldPercent != percent:
                clear()
                print("Stage 1 (not measured): {}% done".format(percent))

            newList.append(x)

            oldPercent = percent

        return newList


    #sqrts every number in the created list
    def intense1():
        def oneSgFg(x):
            return round(x, -int(math.floor(math.log10(abs(x)))))

        global N

        list = createList()

        percent = 0
        oldPercent = 0

        print("Stage 2: {}% done".format(percent))

        i=0

        for item in list:
            i+=1

            percent = int(oneSgFg(((i/N)*100)))

            if oldPercent != percent:
                clear()
                print("Stage 2: {}% done".format(percent))

            result = math.sqrt(item)

            oldPercent = percent

    def intense2():
        def oneSgFg(x):
            return round(x, -int(math.floor(math.log10(abs(x)))))

        global N

        list = createList()

        percent = 0
        oldPercent = 0

        print("Stage 2: {}% done".format(percent))

        i=0

        for item in list:
            i+=1

            percent = int(oneSgFg(((i/N)*100)))

            if oldPercent != percent:
                clear()
                print("Stage 2: {}% done".format(percent))

            result = item/(item+1/(item+1/2))

            oldPercent = percent

    if __name__ == "__main__": 

        def run_threads():
            thread1 = threading.Thread(target=intense1)
            thread2 = threading.Thread(target=intense2)
            thread3 = threading.Thread(target=intense1)
            thread4 = threading.Thread(target=intense2)

            thread1.start()
            thread2.start()
            thread3.start()
            thread4.start()

            thread1.join()
            thread2.join()
            thread3.join()
            thread4.join()

        timeList = []

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

        score = round((1/avgTime)*10000)
        clear()

        print(f"{colours.green()}Multithread Test Complete!{colours.reset()}")
        print("------")
        print(f"{colours.magenta()}Total time{colours.reset()}: {totalTime} seconds")
        print(f"{colours.cyan()}Score{colours.reset()}: {score} points")

        return score


def fullCPUTest():
    def clear():

        name = str(os.name)
        if name == "nt":
            os.system("cls")
        else:
            os.system("clear")
            
    singleCoreScore = singleCore()
    multiCoreScore = multiCore()
    multiThreadScore = multiThread()

    clear()
    
    totalScore = singleCoreScore+multiCoreScore+multiThreadScore
    finalScore = int(round(totalScore/3))
    
    print(f"{colours.green()}Overall CPU Performance Test Complete!{colours.reset()}")
    print("------")
    print(f"{colours.magenta()}Total points scored{colours.reset()}: {totalScore} || (S:{singleCoreScore}, MC:{multiCoreScore}, MT:{multiThreadScore})")
    print(f"{colours.cyan()}Overall score{colours.reset()}: {finalScore}")


prettyPrintData()

while True:
    temp = input(colours.grey()+"Press [ENTER] to continue..."+colours.reset())
    
    clear()
    
    time.sleep(1)
    
    #Main program
    
    question = "Please select the test you wish to perform"
    choices = ["CPU: Single core & thread test", "CPU: Multicore test", "CPU: Multithread test", "CPU: Full Test"]
    
    option, index = pick(choices, question, indicator='=>', default_index=0)
        
    if index == 0:
        singleCore()
        prettyPrintData()
    elif index == 1:
        multiCore()
        prettyPrintData()
    elif index == 2:
        multiThread()
        prettyPrintData()
    elif index == 3:
        fullCPUTest()
        prettyPrintData()