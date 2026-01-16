# corebench.py
"""
The main entry point for CoreBench.

Executing this script starts the program 
depending on execution context.

author: T. de R-R
license: Apache-2.0
date: 05.12.25
"""
# corebench.py

import time, os, socket, multiprocessing, \
        threading, math, platform, random, \
        subprocess, re, getpass, csv, sys, \
        shutil, hashlib, queue, argparse, \
        inspect

from datetime import datetime

import cpuinfo, psutil, GPUtil, distro, \
        speedtest, matplotlib as mpl, \
        matplotlib.pyplot as plt, numpy as np, \
        requests

mpl.use("Agg")

## corebench utils
from modules import api, colours, env, tests, utils, loading, build
from modules.sub_modules import rtx

# Globals
key_data = {} ## A dictionary of all of the key data collected about the system

def takes_args(func: callable):
    """
    Determines how many arguments a function (callable) will take.
    """
    sig = inspect.signature(func)
    return len(sig.parameters)

def process_command(test_input: str, show_results: bool = True, is_terminal: bool=False):
    """
    Takes the test command input as a parameter, and then runs the related
    processes to that command.
    """
    # Parse the test input by initial keyword to check if it is a valid command
    # using the command map in env.p
    command = test_input.split(" ")[0].strip().lower()

    # normalize args
    if len(test_input.split(" ")) > 1:
        comm_args = test_input.split(" ")[1:]
        comm_args = [ item.lower() for item in comm_args ]

    if command in env.command_map.keys():
        if is_terminal and env.command_map[command].get("no_terminal"):
            # if running in terminal and the command isn't supported like this, ignore
            return
        
        # Run the associated function from the command map
        target_func = env.command_map[command]["function"]
        arg_count = takes_args(target_func)

        # Pass arguments depending on if the function takes that many to prevent TypeErrors
        if arg_count == 0:
            result = target_func()
        elif arg_count == 1:
            result = target_func(show_results)
        else:
            result = target_func(show_results, is_terminal)

        if env.command_map[command]["confirm"] and not is_terminal:
            input(f"{colours.grey()}Press [ENTER] to continue...{colours.reset()}")
            utils.clear_home()
    else:
        print(f"{colours.red()}Invalid test command.{colours.reset()}")

def initiate():
    """
    The main script that runs upon CoreBench's execution
    through the bash script. This handles entering command-line
    arguments
    """
    # Command-line argument handler

    # Create argument handler object
    parser = argparse.ArgumentParser()

    # Argument 1
    parser.add_argument("--t", default="", help="""Type of test
                        (fc - full test (default),
                        mc - multicore test,
                        sc - single core test,
                        mt - multithread test)""")

    # Argument 2 (secret)
    parser.add_argument(
        "--m",
        action="store_true",
        help="This is used by the initialisation bash script as an indicator to run the full application. Not recommended to pass as a terminal argument without being in the CoreBench virtual environment."
        )
    
    # Argument 3 - for developers that want to zip their CoreBench version
    parser.add_argument(
        "--b",
        nargs="?",
        const=f"CoreBench-v{utils.remove_char(env.version, '.')}.zip",
        default=False,
        help="Compress a CoreBench redistributable 'build'"
    )

    # parse the args from execution
    args=parser.parse_args()

    if args.m:
        if __name__ == "__main__":
            # The program has been started through the bash script
            # Do normal startup

            # Initialise the /DATA path
            utils.initialise_data_directory()

            ### Load key values ###
            utils.do_initial_load()

            # If there is no cached API key, ask the user for an API key
            if not api.return_api_key():
                api.input_api_key()

            # Print system information
            utils.print_system_data(welcome_user=True)

            # Prompt the user to enter a test command
            print(f"{colours.bold()}Please enter a test command:{colours.reset()}")

            # A variable for tracking whether the user has executed a valid test command to break the loop
            valid_command_entered = False

            while not valid_command_entered:
                # Take an input from the user asking what test command they would like to execute
                test_input = env.getinput()
                process_command(test_input=test_input)
    else:
        # The program has been started through a terminal command
        # Accept arguments
        if args.b:
            build.zip_release(args.b)
            print(f"Successfully saved release: '{args.b}'")
            return
        
        if args.t:
            process_command(test_input=args.t, show_results=True, is_terminal=True)
        else:
            print(f"{colours.red()}Please launch CoreBench using './corebench.sh'{colours.grey()}\nYou can launch the Python script directly by passing the argument '--m', but this will launch outside of CoreBench's controlled environment.{colours.reset()}") # Do nothing

if __name__ == "__main__":
    initiate()