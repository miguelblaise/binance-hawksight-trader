#!/bin/bash

# Get directory of run.sh
WORKING_DIR="$(dirname "$(realpath $0)")"

cd $WORKING_DIR

# source venv
source venv/bin/activate

# Run env variables
source .envrc

# Run python script
python $WORKING_DIR/main.py