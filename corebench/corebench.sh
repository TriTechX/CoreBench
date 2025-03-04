#!/bin/bash

python3 -m venv corebenchenv
source corebenchenv/bin/activate
pip cache purge
pip install -r requirements.txt
python3 corebench.py
