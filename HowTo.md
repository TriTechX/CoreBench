# How To Use CoreBench
## Basic Installation

Run the following command in your terminal, when the current directory is the file in which ```corebench.py``` is located.
```bash
sudo apt update && sudo apt install neofetch && sudo apt install python3-pip && pip install -r requirements.txt
```

This will install the dependencies prepare CoreBench for execution.<br>
To run CoreBench when in the directory in which ```corebench.py``` is located, just run
```bash
python3 corebench.py
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
home - view the home, check client status
api - change the API key
```

Using the argument `-d` will run the test in dynamic mode. Putting `*x` after the base will run that test `x` times. 


> Note: to upload scores to the website, you must have a valid API key - obtained through the website itself - and you must run the **full CPU test** - `fc`
