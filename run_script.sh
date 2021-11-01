#!/bin/bash

# Run env variables
sh ./.envrc

# source venv
source venv/bin/activate

# Run python script
python main.py