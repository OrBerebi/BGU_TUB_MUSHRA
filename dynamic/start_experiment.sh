#!/bin/bash
sleep 1

# Launch PureData (with GUI) and set MIDI in/out to "Head Tracker"
echo "Launching PureData with GUI..."
/Applications/Pd-0.55-0.app/Contents/MacOS/Pd -open ./PD/example.pd &
sleep 3

# Launch Python GUI
echo "Launching Python MUSHRA GUI..."
python3 bgu_mushra.py
sleep 2
