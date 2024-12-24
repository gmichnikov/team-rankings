#!/bin/bash

source venv/bin/activate

echo -e "\nRunning colley.py..."
python colley.py input.csv

echo -e "\nRunning elo.py..."
python elo.py input.csv

echo -e "\nRunning massey.py..."
python massey.py input.csv

echo -e "\nAll ranking scripts have been executed successfully."