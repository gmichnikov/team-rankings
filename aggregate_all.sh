#!/bin/bash

source venv/bin/activate

echo "Running colley.py..."
python colley.py input.csv > colley.txt

echo "Running elo.py..."
python elo.py input.csv > elo.txt

echo "Running massey.py..."
python massey.py input.csv > massey.txt

echo "All ranking scripts have been executed successfully."

# Run the aggregation script
python aggregate.py
