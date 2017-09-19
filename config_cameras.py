from defaults import *

MAX_LAYERS = 1
MAX_ACTIONS = 4

LISTEN_PORT = 9000

SEND_HOST = "10.0.20.119"
SEND_PORT = 6250

USE_MIDI = False
MIDI_DEVS = [
    {
        'id': 'apc',
        'device': 'APC Key 25 MIDI 1',
        'channel': 0
    },
]

LAYERS = [
    {
        'layer': 1,
        'label': 'Cams',
        'rundown': [
            {
                'id': 'CAM1',
                'label': 'CAM1',
                'type': 'toggle',
                'initial': 'off',
                'midi': {
                    'on': ['apc', 'note_on', 32, 0]
                },
                'actions': {
                    'on': [
                        { 'type': 'OSC', 'path': '/control/cam1/play', 'message': 1, },
                        #{ 'type': 'OSC', 'path': '/control/cam2/stop', 'message': 1, },
                        #{ 'type': 'OSC', 'path': '/control/cam3/stop', 'message': 1, },
                        #{ 'type': 'OSC', 'path': '/control/cam4/stop', 'message': 1, },
                        { 'type': 'setstate', 'id': 'CAM2', 'state': 'off', 'propagate': False },
                        { 'type': 'setstate', 'id': 'CAM3', 'state': 'off', 'propagate': False },
                        { 'type': 'setstate', 'id': 'CAM4', 'state': 'prime', 'propagate': False },
                    ],
                    'off': []
                }
            },
            {
                'id': 'CAM2',
                'label': 'CAM2',
                'type': 'toggle',
                'initial': 'prime',
                'actions': {
                    'on': [
                        #{ 'type': 'OSC', 'path': '/control/cam1/stop', 'message': 1, },
                        { 'type': 'OSC', 'path': '/control/cam2/play', 'message': 1, },
                        #{ 'type': 'OSC', 'path': '/control/cam3/stop', 'message': 1, },
                        #{ 'type': 'OSC', 'path': '/control/cam4/stop', 'message': 1, },
                        { 'type': 'setstate', 'id': 'CAM1', 'state': 'off', 'propagate': False },
                        { 'type': 'setstate', 'id': 'CAM3', 'state': 'off', 'propagate': False },
                        { 'type': 'setstate', 'id': 'CAM4', 'state': 'off', 'propagate': False },
                    ],
                    'off': []
                }
            },
            {
                'id': 'CAM3',
                'label': 'CAM3',
                'type': 'toggle',
                'initial': 'prime',
                'actions': {
                    'on': [
                        #{ 'type': 'OSC', 'path': '/control/cam1/stop', 'message': 1, },
                        #{ 'type': 'OSC', 'path': '/control/cam2/stop', 'message': 1, },
                        { 'type': 'OSC', 'path': '/control/cam3/play', 'message': 1, },
                        #{ 'type': 'OSC', 'path': '/control/cam4/stop', 'message': 1, },
                        { 'type': 'setstate', 'id': 'CAM1', 'state': 'off', 'propagate': False },
                        { 'type': 'setstate', 'id': 'CAM2', 'state': 'off', 'propagate': False },
                        { 'type': 'setstate', 'id': 'CAM4', 'state': 'off', 'propagate': False },
                    ],
                    'off': []
                }
            },
            {
                'id': 'CAM4',
                'label': 'CAM4',
                'type': 'toggle',
                'initial': 'prime',
                'actions': {
                    'on': [
                        #{ 'type': 'OSC', 'path': '/control/cam1/stop', 'message': 1, },
                        #{ 'type': 'OSC', 'path': '/control/cam2/stop', 'message': 1, },
                        #{ 'type': 'OSC', 'path': '/control/cam3/stop', 'message': 1, },
                        { 'type': 'OSC', 'path': '/control/cam4/play', 'message': 1, },
                        { 'type': 'setstate', 'id': 'CAM1', 'state': 'off', 'propagate': False },
                        { 'type': 'setstate', 'id': 'CAM2', 'state': 'off', 'propagate': False },
                        { 'type': 'setstate', 'id': 'CAM3', 'state': 'off', 'propagate': False },
                    ],
                    'off': []
                }
            },
        ],
    },
]
