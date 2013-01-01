#!/usr/bin/python

import pyaudio, wave, math
import numpy as np

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
	input = False, 
	output = True,
	frames_per_buffer = chunk)

def Pitch(signal):
	signal = np.fromstring(signal, 'Int16')
	crossing = [math.copysign(1.0, s) for s in signal]
	index = find(np.diff(crossing))
	f0 = round(len(index) * RATE / ( 2 * np.prod(len(signal))))
	return f0

for i in range(0, RATE / chunk * RECORD_SECONDS):
	data = stream.read(chunk)
	Frequency=Pitch(data)
	print "%f Frequency" %Frequency