#!/bin/bash

if [ "$1" = "RED" ]; then
    if [ ! -e /sys/class/gpio/gpio18/value ]; then
        sudo echo "18" > /sys/class/gpio/export
        sudo echo "out" > /sys/class/gpio/gpio18/direction
        sudo echo "0" > /sys/class/gpio/gpio18/value
    else
        sudo echo "0" > /sys/class/gpio/gpio18/value
    fi
fi

if [ "$1" = "WHITE" ]; then
    if [ ! -e /sys/class/gpio/gpio23/value ]; then
        sudo echo "23" > /sys/class/gpio/export
        sudo echo "out" > /sys/class/gpio/gpio23/direction
        sudo echo "0" > /sys/class/gpio/gpio23/value
    else
        sudo echo "0" > /sys/class/gpio/gpio23/value
    fi
fi

if [ "$1" = "BLUE" ]; then
    if [ ! -e /sys/class/gpio/gpio24/value ]; then
        sudo echo "24" > /sys/class/gpio/export
        sudo echo "out" > /sys/class/gpio/gpio24/direction
        sudo echo "0" > /sys/class/gpio/gpio24/value
    else
        sudo echo "0" > /sys/class/gpio/gpio24/value
    fi
fi