import mido
import signal
import sys

midi_device = 'APC Key 25 MIDI 1'

with mido.open_input(midi_device) as inport, mido.open_output(midi_device) as outport:

    notes = {}

    def signal_handler(signal, frame):
        print('Exiting gracefully.')
        print('Clearing grid.')
        for note in notes.keys():
            outport.send(mido.Message('note_on', note=note, velocity=0))
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    for msg in inport:
        print(msg)
        if msg.type == 'note_on':
            msg.velocity=1
            notes[msg.note] = 1
            outport.send(msg)
            #port.send(mido.Message('note_on', note=32, velocity=0))
