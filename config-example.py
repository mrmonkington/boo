from defaults import *

MAX_LAYERS = 3
MAX_ACTIONS = 2

LISTEN_PORT = 9000

SEND_HOST = "127.0.0.1"
SEND_PORT = 6250

USE_MIDI = False
MIDI_DEVICE = 'APC Key 25 MIDI 1'
MIDI_CHANNEL = 0

LAYERS = [
    {
        'layer': 3,
        'label': 'Cams',
        'rundown': [
            {
                'id': 'CAM1',
                'label': 'CAM1',
                'type': 'toggle',
                'initial': 'prime',
                'actions': {
                    'on': [
                        {
                            'type': 'OSC',
                            'path': '/control/cam1/play',
                            'message': 1,
                        },
                        {
                            'type': 'setstate',
                            'id': 'CAM2',
                            'state': 'off',
                            'propagate': False
                        },
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
                    'on': [],
                    'off': []
                }
            },
        ],
    },
    {
        'layer': 10,
        'label': 'gfx1',
        'rundown': [
            {
                'id': 'GFX1',
                'label': 'GFX1',
                'type': 'trigger',
                'initial': 'prime',
                'actions': {
                    'on': [
                        {
                            'type': 'OSC',
                            'path': '/control/gfx1/play',
                            'message': 1,
                        },
                    ],
                    'off': []
                }
            },
            {
                'id': 'GFX2',
                'label': 'GFX2',
                'type': 'trigger',
                'initial': 'prime',
                'actions': {
                    'on': [
                        {
                            'type': 'OSC',
                            'path': '/control/gfx1/play',
                            'message': 1,
                        },
                    ],
                    'off': []
                }
            },
        ],
    },
    {
        'layer': 5,
        'label': 'playout',
        'rundown': [
        ],
    },
]
