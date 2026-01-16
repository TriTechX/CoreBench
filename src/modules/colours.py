# colours.py
"""
Returns ANSI escape codes for colours.

author: T. de R-R
license: Apache-2.0
date: 31.12.24
"""
# modules/colours.py

def black():
    return "\033[30m"

def red():
    return "\033[31m"

def green():
    return "\033[92m"

def yellow():
    return "\033[33m"

def blue():
    return "\033[34m"

def magenta():
    return "\033[35m"

def cyan():
    return "\033[96m"
    
def bold():
    return "\033[1m"

def white():
    return "\033[37m"

def reset():
    return "\033[0m"

def grey():
    return "\033[90m"

def light_grey():
    return "\033[90m"