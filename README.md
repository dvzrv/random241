random241
=========

Python scripts for harvesting entropy from a random number generator (with an Americium 241 sample mounted over a webcam sensor as its source).
This repository also features an OSC enabled SuperCollider [random241.scd](https://raw2.github.com/davezerave/random241/master/SuperCollider/random241.scd) script that can interface with it and a rudimental python script [read_gpio.py](https://raw2.github.com/davezerave/random241/master/remote_control/read_gpio.py) (made for BeagleBone Black) that can be used to further modify effects on the generated sounds in a live setup.

Requirements:
-------------

For the [entropy_harvester](https://github.com/davezerave/random241/tree/master/entropy_harvester) you'll need the following packages and dependencies installed (names may vary depending on your distribution!):
- python2
- python2-numpy
- python2-pyliblo
- opencv
- liblo

For the [SuperCollider](https://github.com/davezerave/random241/tree/master/SuperCollider) script you'll need [SuperCollider](http://supercollider.github.io/) installed (duh!).

For the [remote_control](https://github.com/davezerave/random241/tree/master/remote_control) you'll need the following:
- python2
- python2-pyliblo
- [AdaFruit_BBIO](https://github.com/adafruit/adafruit-beaglebone-io-python)
- liblo

If you want to build your own random number generator from scratch, you can follow my little [howto guide](https://github.com/davezerave/random241/tree/master/howto) (it's far from being perfect though).

Features:
-----

As this is an ongoing project and was executed primarily within the boundaries of my course work for [Audiovisual Programming - Embedded Systems](https://github.com/redFrik/udk10-Embedded_Systems) led by Fredrik Olofsson at UDK Berlin in 2013/ 2014, bugs can be expected (especially if you set up your own device!) and the reporting of those is very welcome!

Currently the list of features for the [entropy_harvester](https://github.com/davezerave/random241/tree/master/entropy_harvester) is as follows:
- Grabbing of bright areas (aka regions of interest in pixels) above a certain threshold from a webcam
- Calculation of mean x/y values from regions of interest and conversion to float range
- Sending of time, x and y values via OSC to predefined host and port

The [SuperCollider](https://github.com/davezerave/random241/tree/master/SuperCollider) script is able to:
- Receive OSC messages for the creation of SynthDefs with certain pitch, amplitude, length and loop time, according to coordinates and time sent.
- Receive OSC messages for manipulation of post processing SynthDefs (FreeVerb for now).
- Ignore OSC messages after a certain amount of SynthDefs created.
- Release (all) SynthDefs after a certain amount of SynthDefs is reached.

The [remote_control](https://github.com/davezerave/random241/tree/master/remote_control) script is able to:
- Read GPIO data from BeagleBone Black (P9_39-42 for now)
- Send sensor data as OSC message to predefined host and port

TODOs:
------
- Externalization of settings for [remote_control](https://github.com/davezerave/random241/tree/master/remote_control) and [entropy_harvester](https://github.com/davezerave/random241/tree/master/entropy_harvester)
- Further settings and advancements in sound for the SuperCollider script
- Performance enhancements for entropy_harvester using different search algorithm (maybe even switch to C++)
- Detection of false positives (pixel errors) on wacky cameras

