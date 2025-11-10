#!/bin/bash
sleep 1

# Launch PureData and store its Process ID (PID)
echo "Launching PureData with GUI..."
/Applications/Pd-0.55-0.app/Contents/MacOS/Pd -open ./PD/switch_player/exp_config_stereo.pd &
PD_PID=$! # <-- THIS LINE IS NEW (Stores the PID)
echo "Pd launched with PID: $PD_PID"
sleep 3

# Launch Python GUI (this script will wait here until Python exits)
echo "Launching Python MUSHRA GUI..."
python3 bgu_mushra.py
sleep 2

# After the Python script closes, this line will run
echo "Python GUI closed. Shutting down PureData..."
# Use kill -9 to be forceful and make sure it closes
kill -9 $PD_PID # <-- THIS LINE IS NEW (Kills the process)
echo "Done."