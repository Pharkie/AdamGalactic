#!/bin/bash

# Define an array of audio device names
audio_devices=(
    "KT USB Audio"
    "MacBook Pro Speakers"
    "Plantronics Blackwire 310"
)

# Define the message to be said
message="Hello!"

# Loop through the array and switch to each audio device
for device in "${audio_devices[@]}"; do
    echo "Switching to $device"
    SwitchAudioSource -s "$device"

    # Say the same message on each device
    say "$message"
done
