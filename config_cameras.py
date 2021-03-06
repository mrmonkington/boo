from defaults import *

from config_common import *

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
                },
                'shortcut': '1',
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
                },
                'shortcut': '2',
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
                },
                'shortcut': '3',
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
                },
                'shortcut': '4',
            },
        ],
    },
]
