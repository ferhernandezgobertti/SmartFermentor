#!/bin/bash

if [ "$1" = "PON" ]; then
    if [ ! -e /sys/class/gpio/gpio13/value ]; then
        sudo echo "13" > /sys/class/gpio/export
        sudo echo "out" > /sys/class/gpio/gpio13/direction
        sudo echo "0" > /sys/class/gpio/gpio13/value
    else
        sudo echo "0" > /sys/class/gpio/gpio13/value
    fi
fi

if [ "$1" = "EXT" ]; then
    if [ ! -e /sys/class/gpio/gpio16/value ]; then
        sudo echo "16" > /sys/class/gpio/export
        sudo echo "out" > /sys/class/gpio/gpio16/direction
        sudo echo "0" > /sys/class/gpio/gpio16/value
    else
        sudo echo "0" > /sys/class/gpio/gpio16/value  
    fi
fi

if [ "$1" = "TEM" ]; then
    if [ ! -e /sys/class/gpio/gpio12/value ]; then
        sudo echo "12" > /sys/class/gpio/export
        sudo echo "out" > /sys/class/gpio/gpio12/direction
        sudo echo "0" > /sys/class/gpio/gpio12/value
    else
        sudo echo "0" > /sys/class/gpio/gpio12/value
    fi
fi

if [ "$1" = "ERR" ]; then
    if [ ! -e /sys/class/gpio/gpio5/value ]; then
        sudo echo "5" > /sys/class/gpio/export
        sudo echo "out" > /sys/class/gpio/gpio5/direction
        sudo echo "0" > /sys/class/gpio/gpio5/value
    else
        sudo echo "0" > /sys/class/gpio/gpio5/value
    fi
fi

if [ "$1" = "VEL" ]; then
    if [ ! -e /sys/class/gpio/gpio6/value ]; then
        sudo echo "6" > /sys/class/gpio/export
        sudo echo "out" > /sys/class/gpio/gpio6/direction
        sudo echo "0" > /sys/class/gpio/gpio6/value
    else
        sudo echo "0" > /sys/class/gpio/gpio6/value
    fi
fi

if [ "$1" = "POT" ]; then
    if [ ! -e /sys/class/gpio/gpio26/value ]; then
        sudo echo "26" > /sys/class/gpio/export
        sudo echo "out" > /sys/class/gpio/gpio26/direction
        sudo echo "0" > /sys/class/gpio/gpio26/value
    else
        sudo echo "0" > /sys/class/gpio/gpio26/value
    fi
fi
