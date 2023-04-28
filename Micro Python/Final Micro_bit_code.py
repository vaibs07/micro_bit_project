from microbit import *
import math

def midiNoteOn(chan, n, vel):
    MIDI_NOTE_ON = 0x90
    if chan > 15 or n > 127 or vel > 127:
        return
    msg = bytes([MIDI_NOTE_ON | chan, n, vel])
    uart.write(msg)

def midiNoteOff(chan, n, vel):
    MIDI_NOTE_OFF = 0x80
    if chan > 15 or n > 127 or vel > 127:
        return
    msg = bytes([MIDI_NOTE_OFF | chan, n, vel])
    uart.write(msg)

def midiControlChange(chan, n, value):
    MIDI_CC = 0xB0
    if chan > 15 or n > 127 or value > 127:
        return
    msg = bytes([MIDI_CC | chan, n, value])
    uart.write(msg)

def midiControlChange(chan, n, value):
    MIDI_CC = 0xB0
    if chan > 15 or n > 127 or value > 127:
        return
    msg = bytes([MIDI_CC | chan, n, value])
    uart.write(msg)  
def Start():
    uart.init(baudrate=31250, bits=8, parity=None, stop=1, tx=pin0)

Start()
lastA = False
lastB = False
lastC = False
BUTTON_A_NOTE = 40
BUTTON_B_NOTE = 45
BUTTON_C_NOTE = 50
last_tilt_x = 0
last_tilt_y = 0
last_pot = 0

while True:
    pot = pin2.read_analog()
    if last_pot != pot:
        velocity = math.floor(pot / 1023 * 127)
        midiControlChange(0, 1, velocity)
        last_pot = pot

    a = button_a.is_pressed()
    b = button_b.is_pressed()
    c = pin1.is_touched()
    if a and not lastA:
        midiNoteOn(0, BUTTON_A_NOTE, 127)
    elif not a and lastA:
        midiNoteOff(0, BUTTON_A_NOTE, 127)
    if b and not lastB:
        midiNoteOn(0, BUTTON_B_NOTE, 127)
    elif not b and lastB:
        midiNoteOff(0, BUTTON_B_NOTE, 127)
    if c and not lastC:
        midiNoteOn(0, BUTTON_C_NOTE, 127)
    elif not c and lastC:
        midiNoteOff(0, BUTTON_C_NOTE, 127)
    lastA = a
    lastB = b
    lastC = c

    current_tilt_y = accelerometer.get_y()
    if current_tilt_y != last_tilt_y:
        mod_y = math.floor(math.fabs((((current_tilt_y + 1024) / 2048) * 127)))
        midiControlChange(0, 2, mod_y)
        last_tilt_y = current_tilt_y
    sleep(10)
