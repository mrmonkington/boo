#!/usr/bin/env python
import sys, threading
import liblo
import gi
from gi.repository import Gtk
gi.require_version('Gtk', '3.0') 
from gi.repository import GObject
from gi.repository import Gdk
import cairo
import re
import colorsys

from config import *

def lighten_rgb(col, mul):
    mul = float(mul)
    hls = list(colorsys.rgb_to_hls(*col))
    hls[1] = hls[1] + ((1.0 - hls[1]) / mul) * (mul-1)
    return colorsys.hls_to_rgb(*hls)

class OSCServer(liblo.ServerThread):
    def __init__(self, app):
        liblo.ServerThread.__init__(self, LISTEN_PORT)
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
        self.host = SEND_HOST
        self.port = SEND_PORT

        self.osc_target = liblo.Address(self.host, self.port, liblo.UDP)
        self.gui = Gui(self)

        self.gui.connect("delete-event", Gtk.main_quit)
        self.gui.connect('destroy', lambda quit: Gtk.main_quit())

    def run(self):
        try:
            server = OSCServer(self)
        except liblo.ServerError, err:
            print str(err)
            sys.exit()

        #server.start()
        Gtk.main()

    def quit(self, *arg):
        self.gui.quit()

    def event(self, key, val):
        for ev in self.events:
            if key == ev.key:
                #self.gui.log(ev.path, val)
                ev.val = val
                ev.send()

class OSCButton(Gtk.Widget):

    def __init__(self, osc_target, msg):
        Gtk.Widget.__init__(self)
        self.osc = osc_target
        self.msg = msg
        #self.connect("touch-event", self.touched)
        self.connect("button-press-event", self.clicked)
        self.color = (0.95, 0.95, 0.95)
        self.set_size_request(80, 60)

    def touched(self, tgt, ev):
        # a sort of debounce, cos touch fires loads of events
        if ev.touch.type == Gdk.EventType.TOUCH_BEGIN:
            if DEBUG:
                print 'Sending %s ' % self.msg
            liblo.send(self.osc, self.msg)

    def clicked(self, tgt, ev):
        if DEBUG:
            print 'Sending %s ' % self.msg
        liblo.send(self.osc, self.msg)

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

class ClipButton(OSCButton):

    def __init__(self, layer, label, osc_target, msg):
        OSCButton.__init__(self, osc_target, msg)
        self.color = (0.95, 0.95, 0.95)
        self.has_content = False
        self.is_playing = False
        self.is_queued = False
        self.flash_state = True

        self.label_index = u"%i" % (layer, )
        self.label_content = label

    def do_draw(self, cr):
        # paint background
        color = lighten_rgb(self.color, 1.4)
        if self.has_content:
            if self.is_playing:
                if self.flash_state:
                    color = self.color
            elif self.is_queued:
                color = lighten_rgb(self.color, 1.2)
        else:
            color = (0.95, 0.95, 0.95)

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


class StopButton(OSCButton):

    def __init__(self, osc_target, msg):
        OSCButton.__init__(self, osc_target, msg)

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

class SceneButton(OSCButton):

    def __init__(self, scene, osc_target, msg):
        OSCButton.__init__(self, osc_target, msg)
        self.scene = scene

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
        cr.text_path("Scene %i" % self.scene)
        cr.fill()

        self.play_icon(cr)

class Gui(Gtk.Window):
    def __init__(self, app):
        Gtk.Window.__init__(self, title="OSC Launchpad")
        self.app = app

        #gobject.threads_init()

        self.table = Gtk.Table(max_layers, max_actions+1, True)
        self.add(self.table)
        self.leds = [[False for x in range(max_actions)] for x in range(max_layers)] 

        self.headers = [False for x in range(max_layers)] 


        for lc, layer in enumerate(LAYERS):

            self.headers[lc] = Gtk.Label('%s' % layer['label'])
            self.table.attach(
                self.headers[lc],
                0,1,
                lc,lc+1,
                Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL,
                Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL,
                2,
                2
            )

            for ac, action in enumerate(layer['rundown']):
                self.leds[lc][ac] = ClipButton(
                    lc,
                    action['label'],
                    self.app.osc_target,
                    liblo.Message(action['path'], action['message'])
                )
                self.table.attach(
                    self.leds[lc][ac],
                    ac+1,ac+1+1,
                    lc,lc+1,
                    Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL,
                    Gtk.AttachOptions.EXPAND | Gtk.AttachOptions.FILL,
                    2,
                    2
                )

        self.show_all()

    def quit(self):
        Gtk.main_quit()

if __name__=='__main__':
    app = App()
    app.run()



