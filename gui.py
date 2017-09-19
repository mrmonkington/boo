import sys, threading
import liblo
import gi
gi.require_version('Gtk', '3.0') 
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Gdk
#from gi.repository import cairo
import cairo
import re
import colorsys

# midi library
import signal

COLOR_PRIME = (0.95, 0.95, 0.35)
COLOR_ON = (0.35, 0.95, 0.35)
COLOR_OFF = (0.95, 0.95, 0.95)

DEBUG = False

def lighten_rgb(col, mul):
    mul = float(mul)
    hls = list(colorsys.rgb_to_hls(*col))
    hls[1] = hls[1] + ((1.0 - hls[1]) / mul) * (mul-1)
    return colorsys.hls_to_rgb(*hls)
def darken_rgb(col, mul):
    mul = 1/float(mul)
    hls = list(colorsys.rgb_to_hls(*col))
    hls[1] = hls[1] + ((1.0 - hls[1]) / mul) * (mul-1)
    return colorsys.hls_to_rgb(*hls)

class Button(Gtk.Widget):

    def __init__(self, label, initial_state):
        Gtk.Widget.__init__(self)
        #self.controller = controller
        #self.msg = msg
        #self.connect("touch-event", self.touched)
        #self.connect("button-press-event", self.clicked)
        self.color = COLOR_OFF
        self.set_size_request(80, 60)

        self.set_hexpand(True)
        self.set_vexpand(True)

    #def touched(self, tgt, ev):
    #    # a sort of debounce, cos touch fires loads of events
    #    if ev.touch.type == Gdk.EventType.TOUCH_BEGIN:
    #        self.trigger()

    def do_draw(self, cr):
        color = COLOR_OFF
        cr.set_source_rgb(*color)
        allocation = self.get_allocation()
        cr.rectangle(0, 0, allocation.width, allocation.height)
        cr.fill()
        cr.set_source_rgb(*darken_rgb(COLOR_OFF, 1.4))
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
        cr.set_source_rgb(*darken_rgb(COLOR_OFF, 1.4))
        cr.fill()

class TriggerButton(Button):

    def __init__(self, layer, label, initial_state):
        Button.__init__(self, label, initial_state)
        self.state = initial_state
        self.has_content = False
        self.is_queued = False
        self.flash_state = True
        self.initial_state = initial_state

        self.label_index = u"%i" % (layer, )
        self.label_content = label

    def get_edge(self):
        return "falling"

    def on(self):
        self.state = "on"
        if DEBUG:
            print "on"
        if self.initial_state == 'off':
            self.timeout_id = GObject.timeout_add(1000, self.off)
        if self.initial_state == 'prime':
            self.timeout_id = GObject.timeout_add(1000, self.prime)
        self.queue_draw()

    def off(self):
        self.state = "off"
        if DEBUG:
            print "off"
        self.queue_draw()

    def prime(self):
        self.state = "prime"
        if DEBUG:
            print "prime"
        self.queue_draw()

    def do_draw(self, cr):
        # paint background
        color = COLOR_OFF
        if DEBUG:
            print "draw"
        if self.state == "on":
            color = COLOR_ON
        if self.state == "prime":
            color = COLOR_PRIME

        cr.set_source_rgb(*color)

        allocation = self.get_allocation()
        cr.rectangle(0, 0, allocation.width, allocation.height)
        cr.fill()
        cr.set_source_rgb(*darken_rgb(color, 1.1))
        cr.rectangle(0, 0, allocation.width, allocation.height)
        cr.stroke()

        cr.set_source_rgb(*darken_rgb(color, 10))
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
        if self.state == "on":
            return "rising"
        if self.state in ("off", "prime"):
            return "falling"

    def on(self):
        self.state = "on"
        if DEBUG:
            print "on"
        self.queue_draw()

    def off(self):
        self.state = "off"
        if DEBUG:
            print "off"
        self.queue_draw()

    def prime(self):
        self.state = "prime"
        if DEBUG:
            print "prime"
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
    def __init__(self, app, config):
        Gtk.Window.__init__(self, title="OSC Launchpad")
        self.app = app

        #gobject.threads_init()

        self.table = Gtk.Grid() #(config.MAX_LAYERS, config.MAX_ACTIONS+1, True)
        self.table.set_hexpand(True)
        self.table.set_vexpand(True)
        self.add(self.table)
        self.leds = [[False for x in range(config.MAX_ACTIONS)] for x in range(config.MAX_LAYERS)] 

        self.headers = [False for x in range(config.MAX_LAYERS)] 


        for lc, layer in enumerate(config.LAYERS):

            self.headers[lc] = Gtk.Label('%s' % layer['label'])
            self.headers[lc].set_valign(Gtk.Align.START)
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
                    
                print action
                print action['initial']
                print
                self.leds[lc][ac] = btype(
                    lc,
                    action['label'],
                    action['initial']
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
