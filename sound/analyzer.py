#!/usr/bin/python

import pyaudio
import numpy as np
import wave

chunk = 2048

window = np.blackman(chunk)

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

p = pyaudio.PyAudio()
myStream = p.open(
	format = FORMAT, 
	channels = CHANNELS, 
	rate = RATE, 
	input = True, 
	output = True,
	frames_per_buffer = chunk)

for i in range(0, RATE / chunk * RECORD_SECONDS):
	data = stream.read(chunk)
	Frequency=Pitch(data)
	print "%f Frequency" %Frequency