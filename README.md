# CoreBench - Benchmark for CoreOS
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
#### Linux
- Download version ```3.10.14``` of Python.
- Download files ```main.py```, ```colours.py```, and ```requirements.txt```
- Put them all in the same directory.
- Enter this directory and run ```pip install -r requirements.txt```
- Run ```sudo apt install neofetch```
- Then run ```python3 main.py```
#### Windows
- **WINDOWS IS CURRENTLY UNSUPPORTED**
#### MacOS
- MacOS has not been tested.
#### Core OS
- Coming soon™


### Info and Devlog

Windows users may run into issues such as lower scores, longer loading times, and inefficient hardware utilization. Higher end systems on Windows may achieve low scores compared to Linux users as the benchmark was designed for Linux

#### Version 1.0.0
- As of CoreBench version 1.0.0, there is no storage of data. There may be in future updates when a simple cloud solution is found
- This program lacks the ability to run GPU tests, it is currently limited to CPU single core, multi core, and multi thread benchmarks
- This program lacks testing data, so what can be considered "good" and "bad" has not been determined yet, so scores are currently arbitrary. Feel free after executing this program to send me your info and scores at TriTechUX@gmail.com
- During multicore and multithread tests, multiple lines of text will show for the progress of the different operations

#### Version 1.0.1
- Changed RAM to calculate more accurately by showing two decimal places
- Fixed misnaming of "totalTime" variable in the single core test
- Optimised to run faster and obtain more accurate scores representative of the system
- Fixed stage 3 single core test percentage going up in multiples of 2 instead of 1
- Fixed stage 2 multicore/multithread test progress showing one decimal place instead of only one significant figure
- Balanced single core scores to be higher and more representative of the system's power

#### Version 1.0.2
- Added full CPU performance test
- Improved readability of test select menu
- Renamed "info.txt" to "corebenchinfo.txt" as the name was too generic, and removal of this file could cause issues if the file is for other applications
- Added all test results to full CPU performance test results screen

#### Version 1.0.3
- Added checks for administrator/root permissions on startup

#### Version 1.0.4
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
- Neofetch is now a dependency of CoreBench. The reason why is... dumb
- Results stored in ```corebenchinfo.txt``` are stored alongside the date and time they were performed
