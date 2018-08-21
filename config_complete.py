from defaults import *

from config_common import *

LAYERS = [
    {
        'layer': 1,
        'label': 'Cams',
        'rundown': [
            {
                'id': 'CAM1',
                'label': 'Head',
                'type': 'toggle',
                'initial': 'prime',
                'shortcut': '1',
                'midi': {
                    'on': ['apc', 'note_on', 32, 0]
                },
                'actions': {
                    'on': [
                        { 'type': 'OSC', 'path': '/control/cam1/play', 'message': 1, },
                        #{ 'type': 'OSC', 'path': '/control/cam2/stop', 'message': 1, },
                        #{ 'type': 'OSC', 'path': '/control/cam3/stop', 'message': 1, },
                        #{ 'type': 'OSC', 'path': '/control/cam4/stop', 'message': 1, },
                        { 'type': 'setstate', 'id': 'CAM2', 'state': 'prime', 'propagate': False },
                        { 'type': 'setstate', 'id': 'CAM3', 'state': 'prime', 'propagate': False },
                        { 'type': 'setstate', 'id': 'CAM4', 'state': 'prime', 'propagate': False },
                    ],
                    'off': []
                }
            },
            {
                'id': 'CAM2',
                'label': 'Wide',
                'type': 'toggle',
                'initial': 'prime',
                'shortcut': '2',
                'actions': {
                    'on': [
                        #{ 'type': 'OSC', 'path': '/control/cam1/stop', 'message': 1, },
                        { 'type': 'OSC', 'path': '/control/cam2/play', 'message': 1, },
                        #{ 'type': 'OSC', 'path': '/control/cam3/stop', 'message': 1, },
                        #{ 'type': 'OSC', 'path': '/control/cam4/stop', 'message': 1, },
                        { 'type': 'setstate', 'id': 'CAM1', 'state': 'prime', 'propagate': False },
                        { 'type': 'setstate', 'id': 'CAM3', 'state': 'prime', 'propagate': False },
                        { 'type': 'setstate', 'id': 'CAM4', 'state': 'prime', 'propagate': False },
                    ],
                    'off': []
                }
            },
            {
                'id': 'CAM3',
                'label': 'Audience',
                'type': 'toggle',
                'initial': 'prime',
                'shortcut': '3',
                'actions': {
                    'on': [
                        #{ 'type': 'OSC', 'path': '/control/cam1/stop', 'message': 1, },
                        #{ 'type': 'OSC', 'path': '/control/cam2/stop', 'message': 1, },
                        { 'type': 'OSC', 'path': '/control/cam3/play', 'message': 1, },
                        #{ 'type': 'OSC', 'path': '/control/cam4/stop', 'message': 1, },
                        { 'type': 'setstate', 'id': 'CAM1', 'state': 'prime', 'propagate': False },
                        { 'type': 'setstate', 'id': 'CAM2', 'state': 'prime', 'propagate': False },
                        { 'type': 'setstate', 'id': 'CAM4', 'state': 'prime', 'propagate': False },
                    ],
                    'off': []
                }
            },
            {
                'id': 'CAM4',
                'label': 'Feed',
                'type': 'toggle',
                'initial': 'prime',
                'shortcut': '4',
                'actions': {
                    'on': [
                        #{ 'type': 'OSC', 'path': '/control/cam1/stop', 'message': 1, },
                        #{ 'type': 'OSC', 'path': '/control/cam2/stop', 'message': 1, },
                        #{ 'type': 'OSC', 'path': '/control/cam3/stop', 'message': 1, },
                        { 'type': 'OSC', 'path': '/control/cam4/play', 'message': 1, },
                        { 'type': 'setstate', 'id': 'CAM1', 'state': 'prime', 'propagate': False },
                        { 'type': 'setstate', 'id': 'CAM2', 'state': 'prime', 'propagate': False },
                        { 'type': 'setstate', 'id': 'CAM3', 'state': 'prime', 'propagate': False },
                    ],
                    'off': []
                }
            },
        ],
    },
    {
        'layer': 2,
        'label': 'VFX1',
        'rundown': [
            {
                'id': 'LOWERNOW',
                'label': 'Lower Now',
                'type': 'trigger',
                'initial': 'off',
                'actions': {
                    'on': [
                        { 'type': 'OSC', 'path': '/control/lt_left/play', 'message': 1, },
                    ],
                    'off': []
                }
            },
            {
                'id': 'LOWERNEXT',
                'label': 'Lower Next',
                'type': 'trigger',
                'initial': 'off',
                'actions': {
                    'on': [
                        { 'type': 'OSC', 'path': '/control/lt_right/play', 'message': 1, },
                    ],
                    'off': []
                }
            },
            {
                'id': 'PIPON',
                'label': 'PiP On',
                'type': 'toggle',
                'initial': 'off',
                'actions': {
                    'on': [
                        { 'type': 'OSC', 'path': '/control/pip_on/play', 'message': 1, },
                    ],
                    'off': [
                        { 'type': 'OSC', 'path': '/control/pip_off/play', 'message': 1, },
                    ]
                }
            },
        ],
    },
]
