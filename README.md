Boo
=============

A matrix of buttons useful for triggering events in OSC aware apps,
specifically in this case CasparCG.

Written for Python2 + GTK3 + Liblo.

## Installation

Distribution shipped `liblo` is fine, and the python liblo module depends on Cython, so this should be all you need to do:

```
apt-get install liblo cython
pip install -r requirements #preferably in a virtualenv, right?
```

## Use

```
./launchpad.py -v --config=config
```

Push the buttons.

## TODO

 - Midi in/out in order to communicate with control surfaces, etc

## Notes

 - https://mido.readthedocs.io/en/latest/messages.html
 - http://community.akaipro.com/akai_professional/topics/midi-information-for-apc-mini

