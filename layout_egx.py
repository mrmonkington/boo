from defaults import *

from config_common import *

LAYERS = [
    {
        'layer': 1,
        'label': 'Cams',
        'rundown': [
            {
                'id': 'CAM1',
                'label': 'PROJ',
                'type': 'toggle',
                'initial': 'prime',
                'actions': {
                    'on': [
                        { 'type': 'OSC', 'path': '/control/cam1/play', 'message': 1, },
                        { 'type': 'setstate', 'id': 'CAM2', 'state': 'prime', 'propagate': False },
                        { 'type': 'setstate', 'id': 'CAM3', 'state': 'prime', 'propagate': False },
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
                        { 'type': 'OSC', 'path': '/control/cam2/play', 'message': 1, },
                        { 'type': 'setstate', 'id': 'CAM1', 'state': 'prime', 'propagate': False },
                        { 'type': 'setstate', 'id': 'CAM3', 'state': 'prime', 'propagate': False },
                        { 'type': 'setstate', 'id': 'CAM4', 'state': 'prime', 'propagate': False },
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
                        { 'type': 'OSC', 'path': '/control/cam3/play', 'message': 1, },
                        { 'type': 'setstate', 'id': 'CAM1', 'state': 'prime', 'propagate': False },
                        { 'type': 'setstate', 'id': 'CAM2', 'state': 'prime', 'propagate': False },
                        { 'type': 'setstate', 'id': 'CAM4', 'state': 'prime', 'propagate': False },
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
        'label': 'VFX',
        'rundown': [
            {
                'id': 'UPNEXT',
                'label': 'Up next',
                'type': 'toggle',
                'initial': 'prime',
                'actions': {
                    'on': [
                        { 'type': 'OSC', 'path': '/control/ready/play', 'message': 1, },
                        { 'type': 'setstate', 'id': 'READY', 'state': 'prime', 'propagate': False },
                        { 'type': 'setstate', 'id': 'START', 'state': 'off', 'propagate': False },
                    ],
                    'off': []
                }
            },
            {
                'id': 'READY',
                'label': 'Ready to start',
                'type': 'toggle',
                'initial': 'off',
                'actions': {
                    'on': [
                        { 'type': 'OSC', 'path': '/control/ready/next', 'message': 1, },
                        { 'type': 'setstate', 'id': 'UPNEXT', 'state': 'off', 'propagate': False },
                        { 'type': 'setstate', 'id': 'START', 'state': 'prime', 'propagate': False },
                    ],
                    'off': []
                }
            },
            {
                'id': 'START',
                'label': 'Start',
                'type': 'toggle',
                'initial': 'off',
                'actions': {
                    'on': [
                        { 'type': 'OSC', 'path': '/control/ready/clear', 'message': 1, },
                        { 'type': 'setstate', 'id': 'READY', 'state': 'off', 'propagate': False },
                        { 'type': 'setstate', 'id': 'UPNEXT', 'state': 'off', 'propagate': False },
                        { 'type': 'setstate', 'id': 'END', 'state': 'prime', 'propagate': False },
                    ],
                    'off': []
                }
            },
            {
                'id': 'END',
                'label': 'End/Intermission',
                'type': 'toggle',
                'initial': 'off',
                'actions': {
                    'on': [
                        { 'type': 'OSC', 'path': '/control/intermission/play', 'message': 1, },
                        { 'type': 'setstate', 'id': 'READY', 'state': 'off', 'propagate': False },
                        { 'type': 'setstate', 'id': 'UPNEXT', 'state': 'off', 'propagate': False },
                        { 'type': 'setstate', 'id': 'START', 'state': 'off', 'propagate': False },
                        # TODO prime the slots layer?
                    ],
                    'off': []
                }
            },
        ]
    }
]
