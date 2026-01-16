#!/bin/bash
#
# CoreBench runner script
#
# Author: T. de R-R
# License: Apache-2.0
# Date: 07.01.26
#
# ../corebench.sh

# Colors
INFO="\033[90m" # grey
ERROR="\033[91m" # red
RESET="\033[0m"

info()  { printf "[${INFO}Info${RESET}] %s\n" "$1"; }
error() { printf "[${ERROR}Error${RESET}] %s\n" "$1"; }

# ensure python 3.14
info "Checking for Python 3.14..."

if ! command -v python3.14 &> /dev/null; then
    info "Python 3.14 not found. Installing..."

    if ! sudo apt-get update -qq; then
        error "Failed to update package lists!"
    fi

    # enable deadsnakes if python 3.14 isn't in repo
    if ! apt-cache policy | grep -q "deadsnakes"; then
        info "Adding deadsnakes PPA..."
        sudo apt-get install -y software-properties-common > /dev/null 2>&1
        sudo add-apt-repository -y ppa:deadsnakes/ppa
        sudo apt-get update -qq
    fi

    if ! sudo apt-get install -y python3.14 python3.14-venv > /dev/null 2>&1; then
        error "Failed to install Python 3.14!"
        exit 1
    fi

    info "Python 3.14 installed successfully."
else
    info "Python 3.14 found."
fi

PY=python3.14

# install loonix dependencies
info "Installing Linux dependencies - elevation may be required..."
if ! sudo apt-get install -y neofetch > /dev/null 2>&1; then
    error "Failed to install system dependencies!"
fi
info "Linux dependencies installed."

# Virtual environment
info "Activating CoreBench virtual environment..."
if [ ! -d "corebench_env" ]; then
    if ! $PY -m venv corebench_env; then
        error "Failed to create virtual environment!"
        exit 1
    fi
fi

source corebench_env/bin/activate
info "CoreBench virtual environment activated."

# pip setup
info "Cleaning pip cache and installing Python requirements..."
if ! $PY -m pip cache purge > /dev/null 2>&1; then
    error "Failed to purge pip cache!"
fi

info "Upgrading pip tools..."
if ! $PY -m pip install --upgrade pip setuptools wheel > /dev/null 2>&1; then
    error "Failed to upgrade pip tools!"
    exit 1
fi

if ! $PY -m pip install -r requirements.txt; then
    error "Failed to install Python dependencies!"
    exit 1
fi

info "Setup complete!"

# Run benchmark
$PY src/corebench.py --m
