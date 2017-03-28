#!/usr/bin/env python
import sys, threading
import liblo
import gi
gi.require_version('Gtk', '3.0') 
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Gdk
import cairo
import re
import colorsys

# midi library
import mido
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

def lighten_rgb(col, mul):
    mul = float(mul)
    hls = list(colorsys.rgb_to_hls(*col))
    hls[1] = hls[1] + ((1.0 - hls[1]) / mul) * (mul-1)
    return colorsys.hls_to_rgb(*hls)

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

        self.gui = Gui(self)

        self.gui.connect("delete-event", Gtk.main_quit)
        self.gui.connect('destroy', lambda quit: Gtk.main_quit())


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
            if actions.has_key('on'):
                self.execute_actions(actions['on'])

    def execute_actions(self, actions):
        for action in actions:
            if DEBUG:
                print action
            if action['type'] == "OSC":
                m = Message(action['path'], action['message'])
                self.send_osc(m)
            if action['type'] == "setstate":
                b = self.button_map[action['id']]
                if action["state"] == "on":
                    b.on()
                if action["state"] == "off":
                    b.off()
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

class Button(Gtk.Widget):

    def __init__(self, label, initial_state):
        Gtk.Widget.__init__(self)
        #self.controller = controller
        #self.msg = msg
        #self.connect("touch-event", self.touched)
        #self.connect("button-press-event", self.clicked)
        self.color = (0.95, 0.95, 0.95)
        self.set_size_request(80, 60)

    #def touched(self, tgt, ev):
    #    # a sort of debounce, cos touch fires loads of events
    #    if ev.touch.type == Gdk.EventType.TOUCH_BEGIN:
    #        self.trigger()

    def do_draw(self, cr):
        color = (0.95, 0.95, 0.95)
        cr.set_source_rgb(*color)

        allocation = self.get_allocation()
        cr.rectangle(0, 0, allocation.width, allocation.height)
        cr.fill()
        cr.set_source_rgb(0.9, 0.9, 0.9)
        cr.rectangle(0, 0, allocation.width, allocation.height)
        cr.stroke()

    def do_realize(self):
        allocation = self.get_allocation()
        attr = Gdk.WindowAttr()
        attr.window_type = Gdk.WindowType.CHILD
        attr.x = allocation.x
        attr.y = allocation.y
        attr.width = allocation.width
        attr.height = allocation.height
        attr.visual = self.get_visual()
        attr.event_mask = self.get_events() | Gdk.EventMask.EXPOSURE_MASK | Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.TOUCH_MASK
        WAT = Gdk.WindowAttributesType
        mask = WAT.X | WAT.Y | WAT.VISUAL

        window = Gdk.Window(self.get_parent_window(), attr, mask);
        self.set_window(window)
        self.register_window(window)

        self.set_realized(True)
        window.set_background_pattern(None)

    def play_icon(self, cr):
        allocation = self.get_allocation()
        cr.move_to(allocation.width-16, 6)
        cr.line_to(allocation.width-6, 11)
        cr.line_to(allocation.width-16, 16)
        cr.close_path()
        cr.set_source_rgb(0.7, 0.7, 0.7)
        cr.fill()

class TriggerButton(Button):

    def __init__(self, layer, label, initial_state):
        Button.__init__(self, label, initial_state)
        self.color = (0.85, 0.85, 0.85)
        self.has_content = False
        self.is_playing = False
        self.is_queued = False
        self.flash_state = True

        self.label_index = u"%i" % (layer, )
        self.label_content = label

    def get_edge(self):
        return "falling"

    def on(self):
        self.is_playing = True
        if DEBUG:
            print "on"
        self.timeout_id = GObject.timeout_add(1000, self.off)
        self.queue_draw()

    def off(self):
        self.is_playing = False
        if DEBUG:
            print "off"
        self.queue_draw()

    def do_draw(self, cr):
        # paint background
        if DEBUG:
            print "draw"
        color = lighten_rgb(self.color, 1.4)
        if self.is_playing:
            color = self.color

        cr.set_source_rgb(*color)

        allocation = self.get_allocation()
        cr.rectangle(0, 0, allocation.width, allocation.height)
        cr.fill()
        cr.set_source_rgb(0.9, 0.9, 0.9)
        cr.rectangle(0, 0, allocation.width, allocation.height)
        cr.stroke()

        cr.set_source_rgb(0.3, 0.3, 0.3)
        cr.select_font_face("Monaco", cairo.FONT_SLANT_NORMAL, 
            cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(11)
        cr.move_to(4,15)
        cr.show_text(self.label_index)
        cr.move_to(4,30)
        cr.show_text(self.label_content)

        self.play_icon(cr)

class ToggleButton(TriggerButton):
    def get_edge(self):
        if self.is_playing == True:
            return "rising"
        if self.is_playing == False:
            return "falling"

    def on(self):
        self.is_playing = True
        if DEBUG:
            print "on"
        self.queue_draw()

    def off(self):
        self.is_playing = False
        if DEBUG:
            print "off"
        self.queue_draw()

class ClearButton(Button):

    def __init__(self, controller, msg):
        Button.__init__(self, controller, msg)

    def do_draw(self, cr):
        allocation = self.get_allocation()
        cr.set_source_rgb(0.95, 0.95, 0.95)
        cr.rectangle(0, 0, allocation.width, allocation.height)
        cr.fill()
        cr.set_source_rgb(0.9, 0.9, 0.9)
        cr.rectangle(0, 0, allocation.width, allocation.height)
        cr.stroke()

        cr.set_source_rgb(0.6, 0.6, 0.6)
        cr.select_font_face("Monaco", cairo.FONT_SLANT_NORMAL, 
            cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(11)
        cr.move_to(4,15)
        cr.text_path("Stop")
        cr.fill()

        # stop icon
        cr.rectangle(allocation.width-16, 6, 10, 10)
        cr.set_source_rgb(0.7, 0.7, 0.7)
        cr.fill()

class LayerButton(Button):
    pass

class Gui(Gtk.Window):
    def __init__(self, app):
        Gtk.Window.__init__(self, title="OSC Launchpad")
        self.app = app

        #gobject.threads_init()

        self.table = Gtk.Grid() #(config.MAX_LAYERS, config.MAX_ACTIONS+1, True)
        self.add(self.table)
        self.leds = [[False for x in range(config.MAX_ACTIONS)] for x in range(config.MAX_LAYERS)] 

        self.headers = [False for x in range(config.MAX_LAYERS)] 


        for lc, layer in enumerate(config.LAYERS):

            self.headers[lc] = Gtk.Label('%s' % layer['label'])
            self.table.attach(
                self.headers[lc],
                0,lc,
                1,1
            )

            for ac, c_action in enumerate(layer['rundown']):
                btype = TriggerButton
                # set some defaults
                action = {
                    'type': 'trigger', # trigger|toggle
                    'initial': 'prime', # off|prime|on
                    'actions': {},
                }
                action.update(c_action)
                if DEBUG:
                    print "Adding action: %s" % (action)

                if action["type"] == "toggle":
                    btype = ToggleButton
                if action["type"] == "trigger":
                    btype = TriggerButton
                    
                self.leds[lc][ac] = btype(
                    lc,
                    action['label'],
                    initial_state = action['initial']
                    #Message(action['path'], action['message'])
                )
                self.table.attach(
                    self.leds[lc][ac],
                    ac+1,lc,
                    1,1
                )
                self.app.controller.connect(action['id'], self.leds[lc][ac], action['actions'])

        self.show_all()

    def quit(self):
        Gtk.main_quit()

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

    app = App()
    app.run()



