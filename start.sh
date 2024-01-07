#!/bin/bash

# Installing a virtual environment if it has not already been created
if [ ! -d "venv" ] 
then
    echo "Creating a virtual environment..."
    python3 -m venv venv
fi

# Activating the virtual environment
echo "Activating the virtual environment..."
source venv/bin/activate

# Installing dependencies
echo "Installing dependencies from the requirements.txt file..."
pip3 install -r requirements.txt

# Launching the application
echo "Launching the application..."
python3 app.py
