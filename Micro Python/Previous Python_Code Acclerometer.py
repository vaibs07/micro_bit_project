from microbit import *
import math

def midiNoteOn(chan, n, vel):
    MIDI_NOTE_ON = 0x90
    if chan > 15 or chan < 0 or n > 127 or n < 0 or vel > 127 or vel < 0:
        return
    msg = bytes([MIDI_NOTE_ON | chan, n, vel])
    uart.write(msg)


def midiNoteOff(chan, n, vel):
    MIDI_NOTE_OFF = 0x80
    if chan > 15 or chan < 0 or n > 127 or n < 0 or vel > 127 or vel < 0:
        return
    msg = bytes([MIDI_NOTE_OFF | chan, n, vel])
    uart.write(msg)


def midiControlChange(chan, n, value):
    MIDI_CC = 0xB0
    if chan > 15 or chan < 0 or n > 127 or n < 0 or value > 127 or value < 0:
        return
    msg = bytes([MIDI_CC | chan, n, value])
    uart.write(msg)


def Start():
    uart.init(baudrate=31250, bits=8, parity=None, stop=1, tx=pin0)


Start()
lastA = False
lastB = False
lastC = False
BUTTON_A_NOTE = 36
BUTTON_B_NOTE = 39
BUTTON_C_NOTE = 43
last_tilt = 0
last_pot = 0
while True:
    pot = pin2.read_analog()
    if abs(pot - last_pot) > 3:
        velocity = math.floor(pot / 1023 * 127)
        midiControlChange(0, 1, velocity)
        midiControlChange(0, 2, velocity)
    last_pot = pot

    a = button_a.is_pressed()
    b = button_b.is_pressed()
    c = pin1.is_touched()
    if a and not lastA:
        midiNoteOn(0, BUTTON_A_NOTE, 127)
        midiControlChange(0, 7, 127)
        midiControlChange(0, 8, 5)
    elif not a and lastA:
        midiNoteOff(0, BUTTON_A_NOTE, 127)
        midiControlChange(0, 7, 127)
        midiControlChange(0, 8, 127)
    if b and not lastB:
        midiNoteOn(0, BUTTON_B_NOTE, 127)
        midiControlChange(0, 5, 7)
    elif not b and lastB:
        midiNoteOff(0, BUTTON_B_NOTE, 127)
        midiControlChange(0, 5, 0)
    if c and not lastC:
        midiNoteOn(0, BUTTON_C_NOTE, 127)
        midiControlChange(0, 6, 5)
    elif not c and lastC:
        midiNoteOff(0, BUTTON_C_NOTE, 127)
        midiControlChange(0, 6, 0)

    lastA = a
    lastB = b
    lastC = c
    current_tilt = accelerometer.get_y()
    if abs(current_tilt - last_tilt) > 20:
        mod_y = math.floor((current_tilt + 1024) / 2047 * 127)
        midiControlChange(0, 2, mod_y)
        last_tilt = current_tilt
    current_tilt = accelerometer.get_x()
    if abs(current_tilt - last_tilt) > 20:
        mod_x = math.floor((current_tilt + 1024) / 2047 * 127)
        midiControlChange(0, 4, mod_x)
        last_tilt = current_tilt
    sleep(10)
