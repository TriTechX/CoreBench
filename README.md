# CoreBench - Benchmark for Linux Systems
## This program aims to perform the following functions:

- Single core and thread performance
- Multithreaded CPU performance (Multiple threads on one core)
- Multicore CPU performance (1 thread per core)

## Then, if applicable:

- GPU performance

### And then finally retrieve all system information, inculding:
- Operating system
- RAM quantity
- CPU brand and name
- GPU brand and name
- System name (hostname)

This bench is more accurate on lower-end systems running Core. High end systems may achieve very fluctuating results. 

### When running CoreBench, you agree to the following:

- Your data (only listed above) may be stored on an external server.
- Your data uploaded to the external server (only listed above) belongs to TriTech for any fair use such as:
     - Making tables, graphs, or charts featuring your data.
  - Readjusting the program according to your data.
  - Publishing your data publicly unassociated with your system name.
  - Storage on any device owned by TriTech.
  - Any other use considered fair.

#### Privacy Notice

- If you do not wish for your data to be used any of the cases above, you may not use CoreBench.
- If your data (in the list above) is collected by CoreBench you may not request its deletion, as by using CoreBench you agree to the terms above.
- Any information not listed above will **not** be recorded. If it is, you have all right to request its deletion.
- You have all right to request the data related to your system from our servers at TriTechUX@gmail.com, and if it is stored you will receive it as soon as possible, if you format the email in the following fashion:
- - To: **TriTechUX@gmail.com**
  - Subject: **CoreBench Server Data Request**
  - Content: This is a request for the data for [INSERT HOSTNAME HERE].
- No sensitive data is collected by this program.


### Installation
#### Linux/Mac
- Download version ```3.10.14```+ of Python.
- Download files ```main.py```, ```colours.py```, and ```requirements.txt```
- Put them all in the same directory.
- Enter this directory and run ```pip install -r requirements.txt```
- run ```sudo apt install neofetch```
- Then run ```python3 main.py```
- Linux portable image coming soon™
- dmg will never exist
#### Windows
- **WINDOWS IS CURRENTLY UNSUPPORTED**
#### Core OS
- Coming soon™
### Info and Devlog

Users running on Windows through Python interpreters may run into issues such as absurdly low scores, much longer loading times, and inefficient hardware utilization. The multicore method used in this program is NOT compatible with Windows. Higher end systems on Windows may achieve low scores compared to Linux users, as the benchmark was designed for Linux. If you desperately want to run this and get accurate results, I guess you could make a tiny partition for dual booting a Linux distro.

#### Version 1.0.0 /xytro
- As of CoreBench version 1.0.0, there is no storage of data. There may be in future updates when a simple cloud solution is found
- This program lacks the ability to run GPU tests, it is currently limited to CPU single core, multi core, and multi thread benchmarks
- This program lacks testing data, so what can be considered "good" and "bad" has not been determined yet, so scores are currently arbitrary. Feel free after executing this program to send me your info and scores at TriTechUX@gmail.com
- During multicore and multithread tests, multiple lines of text will show for the progress of the different operations

#### Version 1.0.1 /xytro
- Changed RAM to calculate more accurately by showing two decimal places
- Fixed misnaming of "totalTime" variable in the single core test
- Optimised to run faster and obtain more accurate scores representative of the system
- Fixed stage 3 single core test percentage going up in multiples of 2 instead of 1
- Fixed stage 2 multicore/multithread test progress showing one decimal place instead of only one significant figure
- Balanced single core scores to be higher and more representative of the system's power

#### Version 1.0.2 /xytro
- Added full CPU performance test
- Improved readability of test select menu
- Renamed "info.txt" to "corebenchinfo.txt" as the name was too generic, and removal of this file could cause issues if the file is for other applications
- Added all test results to full CPU performance test results screen

#### Version 1.0.3 /xytro
- Added checks for administrator/root permissions on startup

#### Version 1.0.4 /xytro
- Aimed to fix a few small issues with text formatting and RAM calculations
- Added specific Linux distro identification to make recording results easier
- Full CPU test no longer flashes results from each individual test
- Full CPU test results are now stored to file ```corebenchinfo.txt```
- Added a timer cooldown between successive tests on the full CPU test
- Fixed multithread test results being bottlenecked by I/O operations and percentage calculations
- Fixed multithread epilepsy effect
- Fixed a very intellectual bug that meant that the script wouldn't correctly check for admin privileges on Linux/MacOS (totally didn't use os.geteuid() instead of os.getuid())
- Did the same fix to the multiprocessing test as the multithread test.
- Added compatibility with CPU temperature monitoring. This project may require lm_sensors in the future.
- Removed the 4 decimal place CPU clock speed response and rounded it to 2 decimal places as is standard.
- Updated core count to count physical CPU cores, and added a seperate info tab for threads - ruining my colour scheme >:(
- Neofetch is now a dependency of CoreBench. It is utilised to get the colour of your distro.

#### Version 1.0.5 /xytro
- Added support for the Windows-coloured name in the "OS Name" tab (despite there being no Windows support)
- Added more loading messages.
- Added an activation screen when grabbing "essential" variable data.
- The multithread test now utilises 12 threads.
- The multicore test now utilises 6 cores.
#### Major Feature!
- Dynamic mode - adjusts the performance tests based on your hardware. Multicore and multithread tests will match the number of cores and threads your CPU has. It's a test aimed at CPU efficiency (not power efficiency, core and thread utilisation efficiency), so comparing dynamic mode scores between 2 CPUs with different core/thread counts is not advised. (The default test runs on 6 cores and 12 threads.) **Your scores will not be submitted when recorded in dynamic mode**. Press [CTRL] + [C] when CoreBench is starting up (before it shows ```Activating...```) to enter dynamic mode.

- CoreBench *104* and *105 beta* only ran on 4 cores and 4 threads. This has been adjusted for realistic performance monitoring, now running on 6 cores and 12 threads.
- Various stability fixes.
- Various score re-balancing (comparing scores between *104* and *105* is no longer valid, and these changes explain why I haven't made the database yet)
- Scores in dynamic mode are based on the ratio of cores/threads to 6 and 12.
- Dynamic mode was finished on 05/02/2025.

#### Version 1.0.6 /xytro & avale
- Changed method of grabbing name to getpass.getuser() instead of pwd.
- Single core test was not guaranteed to be isolated to a single core. The single core test ignores hyperthreading, and runs on one core on one thread. This was hastily added after its discovery just after 105.
### CPU Utilisation Before 1.0.6<br> ![Before](https://i.ibb.co/snNxwvy/before.jpg "Before")<br>
- As you can see, all the CPU cores activate at the same time, indicating that Python is using more than 1 core, as this is a 1 core per thread processor.
### CPU Utilisation After 1.0.6<br> ![Afterwards](https://i.ibb.co/prfMzQJF/afterwards.jpg "Afterwards")<br>
- In the new 1.0.6 patch, only CPU 0 is fully utilised. The rest are supposed to be idling, but this is a Chromebook processor. (Thank you avale for being smarter than me!!!)<br>Yes, this example is running on Windows. This does not mean Windows support is coming. I think. Maybe I should add a multiplier for Windows machines, or make a seperate database for Windows machines or... no.

#### Version 1.1.0 /xytro
- Single core test doesn't take as long anymore.
- The percentage shows to one significant figure rather than the nearest integer to prevent I/O bottleneck.
- Moved the benchmark process code for multicore test into a main check.
- The reason why it isn't compatible with Windows is now known. Windows cannot "pickle" (initiate for use in multicore) local functions (functions defined inside of functions). I don't want to change this especially since I am so far into development, and it will mess up the few consistencies that exist in my spaghetti code. Once again, my totally nonexistent dreams for CoreBench on Windows are destroyed. Maybe I'll make one *for* Windows. I hate Windows so much man. Why can't it just *work*?
- Added one additional point to all test scores. Or did I?
- Another reason that CoreBench runs badly on Windows has been discovered (other than overhead). Due to Windows' Multilevel Feedback Queue process scheduling method, CoreBench is treated like a background process, and punished for being demanding. Linux uses the Completely Fair scheduling method, which is why scores are so much higher and more definitive.<br>

#### Before High Priority
![Before](https://i.ibb.co/6cbj4Wwr/beforee.jpg "Before")


#### After High Priority
![Afterwards](https://i.ibb.co/BHgZF1rf/after.jpg "Afterwards")<br>

It takes an extra 8 seconds without high priority. This was WITH background processes running in both tests. (Brave browser idling)<br>
Despite the tab saying "CoreBench105.py", it is actually CoreBench 1.0.7.

- Just realised it still says (c) TriTech 2024, meaning the copyright is outdated. That ain't good. Updated to (c) TriTech 2025 as of **7th February 2025**.
- Added version no. and dynamic mode info to the corebenchinfo.txt file. A new set of results will be written to corebench.txt when you run a full CPU test.

#### Major Feature!
- Added a set of data in .csv format called "corebenchdata.csv", created when not present and written to with each non-dynamic mode test result.
- Full CPU test now produces a visual bar chart showing performance vs your system's overall average, called "corebenchdata.png"
<br></br>

#### Version 1.1.1 /xytro

- Added "test commands" due to the growing number of tests.<br>
```py
"sc"/"st" - Single core test
"mc" - Multicore test
"mt" - Multithread test
"nic"/"n" - Internet speed test
"fullc"/"fc" - Full CPU test
```
Add "-d" to the end of your command to run the test in dynamic mode. The [CTRL] + [C] shortcut has been removed.

#### Version 1.2.0 /xytro & avale
- Completely reworks the single core algorithms.
- Stage 1 is now a gravity and collision detection simulator.
- Stage 2 simulates simple trigonometric calculations in quick succession and vector maths.
- Stage 3 calculates floating point performance for the single core through lots of demanding vector calculations.

#### Version 1.2.1 /avale
- Prettified single core text layout and colours.
- Sorted out code order issues.
- Added credits to readme.
- Fixed title header layout on readme.
