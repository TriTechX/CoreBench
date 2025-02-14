# How To Use CoreBench
## Basic Installation

Run the following command in your terminal, when the current directory is the file in which ```main.py``` is located.
```bash
sudo apt install neofetch && sudo apt update && sudo apt install python3-pip && pip install -r requirements.txt
```
This will install the dependencies prepare CoreBench for execution.<br>
To run CoreBench when in the directory in which ```main.py``` is located, just run
```bash
python main.py
```

## Use Instructions
On startup you will be greeted with a loading screen. Just press [ENTER] after you are presented with your system information. Make sure all of your hardware displays properly.<br>
You will then be asked to type a "test command". Here is the syntax for test commands: ```base -args```.<br>

Current bases are:
```
sc OR st - single core
mt - multithread
mc - multicore
fullc OR fc - full CPU benchmark
nic OR n - network
```

Currently, the only argument is "d", which runs the test in "Dynamic Mode" which scales the scores and tests based on how many cores and threads are in your processor.<br>
Use example: ```mc -d```, runs the single core test in dynamic mode.
