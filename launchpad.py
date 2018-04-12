#!/usr/bin/env python
import sys, threading
import liblo
import gi
gi.require_version('Gtk', '3.0') 
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Gdk
from gi.repository import cairo
#import cairo
import re
import colorsys

import gui

# midi library
try:
    import mido
except:
    pass
import signal

#from config import *
config = {}
DEBUG = False

class Message(liblo.Message):
    def __init__(self, path, args):
        self._path = path
        self._args = args
        super(Message, self).__init__(path, args)
    def __repr__(self):
        return "%s %s" % (self._path, self._args)


class OSCServer(liblo.ServerThread):
    def __init__(self, app):
        liblo.ServerThread.__init__(self, config.LISTEN_PORT)
        self.app = app

        self.osc_routes = {
        }

    def parse_rgb(self, rgbstr):
        return [float(x) for x in re.match("RGB\(([\.0-9]+),([\.0-9]+),([\.0-9]+)\)", rgbstr).groups()]

    @liblo.make_method(None, None)
    def handle(self, path, args):
        if DEBUG:
            print "received '%s'" % path
            print args
        for pattern, action in self.osc_routes.items():
            match = re.match(pattern, path)
            if match:
                path_args = list(match.groups())
                path_args.append(args)
                action(*path_args)
                break

#    def set_track_color(self, track, args):
#        track = int(track)
#        for clip in range(1,num_scenes+1):
#            color = self.parse_rgb(args[0])
#            self.app.gui.leds[track][clip].color = color
#            self.app.gui.leds[track][clip].queue_draw()

class App(object):
    def __init__(self):
        self.controller = Controller()

        self.gui = gui.Gui(self, config)

        self.gui.connect("delete-event", Gtk.main_quit)
        self.gui.connect('destroy', lambda quit: Gtk.main_quit())
        self.gui.connect('key_press_event', self.gui.key_press)


    def run(self):
        Gtk.main()

    def quit(self, *arg):
        self.engine.teardown()
        self.gui.quit()

    def event(self, key, val):
        for ev in self.events:
            if key == ev.key:
                #self.gui.log(ev.path, val)
                ev.val = val
                ev.send()

class Controller(object):
    def __init__(self):
        self.host = config.SEND_HOST
        self.port = config.SEND_PORT
        self.osc_target = liblo.Address(self.host, self.port, liblo.UDP)
        try:
            self.midi_in = mido.open_input(config.MIDI_DEVICE, callback=self.receive_midi)
            self.midi_out = mido.open_output(config.MIDI_DEVICE)
        except:
            config.USE_MIDI = False

        self.action_map = {}
        self.button_map = {}

    def connect(self, button_id, button, actions):
        button.connect("button-press-event", self.trigger, button, actions)
        self.action_map[button_id] = actions
        self.button_map[button_id] = button

    def trigger(self, event, tgt, button, actions):
        edge = button.get_edge()

        # button toggled on, or trigger firing
        if edge == "falling":
            button.on()
            if actions.has_key('on'):
                self.execute_actions(actions['on'])

        # button toggled off, or auto rising
        if edge == "rising":
            button.off()
            if actions.has_key('off'):
                self.execute_actions(actions['off'])

    def execute_actions(self, actions):
        for action in actions:
            if DEBUG:
                print action
            if action['type'] == "OSC":
                print "Sending %s" % action['path']
                m = Message(action['path'], action['message'])
                self.send_osc(m)
            if action['type'] == "setstate":
                b = self.button_map[action['id']]
                if action["state"] == "on":
                    b.on()
                if action["state"] == "off":
                    b.off()
                if action["state"] == "prime":
                    b.prime()
                if action["propagate"] == True:
                    self.execute_actions(self.action_map[action['id']][action['state']])

    def teardown(self):
        if config.USE_MIDI:
            self.midi_in.close()
            self.midi_out.close()

    def run(self):
        try:
            server = OSCServer(self)
            #server.start()
        except liblo.ServerError, err:
            print(str(err))
            sys.exit()

    def receive_midi(self, msg):
        print(msg)

    def send_osc(self, msg):
        liblo.send(self.osc_target, msg)

    def clicked(self, tgt, ev):
        self.trigger()

    #def trigger(self):
    #    self.send_msg()

    def send_msg(self):
        if DEBUG:
            print 'Sending %s ' % self.msg
        self.controller.send_osc(self.msg)


def get_args():
    import argparse

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--config',
        default='config',
        help='config module (default: config i.e. config.py)')
    parser.add_argument('--debug', '-v',
        default=False, action='store_const', const=True,
        help='debug output')

    args = parser.parse_args()
    # people might accidentally supply a module filename, which we'll forgive them for
    args.config=re.sub('.py$', '', args.config)
    return args

if __name__=="__main__":

    args = get_args()
    config = __import__(args.config, fromlist=['*'])
    DEBUG = args.debug
    gui.DEBUG = DEBUG

    app = App()
    app.run()



