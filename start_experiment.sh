#!/bin/bash
sleep 1

# Launch PureData (with GUI) and set MIDI in/out to "Head Tracker"
echo "Launching PureData with GUI..."
/Applications/Pd-0.55-0.app/Contents/MacOS/Pd -open ./dynamic/PD/example.pd &
PD_PID=$! # <-- THIS LINE IS NEW (Stores the PID)
echo "Pd launched with PID: $PD_PID"
sleep 3

# Launch Python GUI
echo "Launching Python MUSHRA GUI..."
cd dynamic
python bgu_mushra.py
sleep 2

# After the Python script closes, this line will run
echo "Python GUI closed. Shutting down PureData..."
# Use kill -9 to be forceful and make sure it closes
kill -9 $PD_PID # <-- THIS LINE IS NEW (Kills the process)
echo "Done."

sleep 1
cd ../

# Launch PureData (with GUI) and set MIDI in/out to "Head Tracker"
echo "Launching PureData with GUI..."
/Applications/Pd-0.55-0.app/Contents/MacOS/Pd -open ./static/PD/switch_player/exp_config_stereo.pd &
PD_PID=$! # <-- THIS LINE IS NEW (Stores the PID)
echo "Pd launched with PID: $PD_PID"
sleep 3

# Launch Python GUI
echo "Launching Python MUSHRA GUI..."
cd static
python bgu_mushra.py
sleep 2

# After the Python script closes, this line will run
echo "Python GUI closed. Shutting down PureData..."
# Use kill -9 to be forceful and make sure it closes
kill -9 $PD_PID # <-- THIS LINE IS NEW (Kills the process)
echo "Done."
cd ..