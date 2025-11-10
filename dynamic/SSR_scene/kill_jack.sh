#!/bin/bash

# Kill all running instances of jackd
pkill -x jackd

# Verify if JACK servers were terminated
if ! pgrep -x "jackd" > /dev/null; then
    echo "All running JACK servers have been terminated."
else
    echo "Failed to terminate all JACK servers."
fi
