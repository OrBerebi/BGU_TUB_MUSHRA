#!/bin/bash

if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root. Type "sudo su", hit enter and run the script again."
    exit 1
fi

# Set environment variable to bypass audio reservation
export JACK_NO_AUDIO_RESERVATION=1
# Function to start JACK server and application
start_jack() {
    # Start JACK with ALSA driver in real-time mode in a new terminal window
    echo "Starting JACK server..."
    #jackd -d coreaudio -r 48000 -d hw:UFX23643007 -p 256 -C -P hw:UFX23643007
    jackd -d coreaudio -r 48000 -o system -p 256


}

# Check if JACK is already running
if pgrep -x "jackd" > /dev/null; then
    echo "A JACK server is already running."
    
    # Ask user if they want to quit the running serverjackd -d coreaudio -r 48000 -d hw:0 -p 128 -n 2 -P 60 -t 2000 -C &
    read -p "Do you want to quit the running JACK server and start the script? (y/n) " answer
    if [ "$answer" = "y" ]; then
        # Terminate the running JACK server
        pkill -x jackd
        echo "Terminated the running JACK server."
        pkill -x qjackctl
        sleep 1 # Wait a moment for the application to close
        echo "Terminated the running qjackctl."

        sleep 5 # Give JACK some time to quit

        # Start JACK server and application
        start_jack
    else
        echo "Script execution aborted."
    fi
else
    start_jack
fi

