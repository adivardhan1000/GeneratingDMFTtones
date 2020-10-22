import pyaudio
import array
import math
import time
import numpy as np

user_freq = [697.0, 770.0, 852.0, 941.0,
             1209.0, 1336.0, 1477.0, 1633.0]
user_tones = {
    '1': (user_freq[0], user_freq[4]),
    '2': (user_freq[0], user_freq[5]),
    '3': (user_freq[0], user_freq[6]),
    'A': (user_freq[0], user_freq[7]),
    '4': (user_freq[1], user_freq[4]),
    '5': (user_freq[1], user_freq[5]),
    '6': (user_freq[1], user_freq[6]),
    'B': (user_freq[1], user_freq[7]),
    '7': (user_freq[2], user_freq[4]),
    '8': (user_freq[2], user_freq[5]),
    '9': (user_freq[2], user_freq[6]),
    'C': (user_freq[2], user_freq[7]),
    '*': (user_freq[3], user_freq[4]),
    '0': (user_freq[3], user_freq[5]),
    '#': (user_freq[3], user_freq[6]),
    'D': (user_freq[3], user_freq[7]),
}

op_freq = [700.0, 900.0, 1100.0, 1300.0, 1300.0, 1500.0, 1700.0]

op_tones = {
    '1': (op_freq[0], op_freq[1]),
    '2': (op_freq[0], op_freq[2]),
    '3': (op_freq[1], op_freq[2]),
    '4': (op_freq[0], op_freq[3]),
    '5': (op_freq[1], op_freq[3]),
    '6': (op_freq[2], op_freq[3]),
    '7': (op_freq[0], op_freq[4]),
    '8': (op_freq[1], op_freq[4]),
    '9': (op_freq[2], op_freq[4]),
    '0': (op_freq[3], op_freq[4]),  # 0 or "10"
    'A': (op_freq[3], op_freq[4]),  # 0 or "10"
    'B': (op_freq[0], op_freq[5]),  # 11 or ST3
    'C': (op_freq[1], op_freq[5]),  # 12 or ST2
    'D': (op_freq[2], op_freq[5]),  # KP
    'E': (op_freq[3], op_freq[5]),  # KP2
    'F': (op_freq[4], op_freq[5]),  # ST
}

sr = 44100
length = float(input('Enter length of each tone(in seconds)'))
volume = 0.5
if volume > 0 and volume < 1:
    pass
else:
    print('Invalid volume. Re-Enter')
    volume = float(input('Set volume for the tones (between 0 and 1):'))

p = pyaudio.PyAudio()
stream = p.open(rate=sr, channels=1, format=pyaudio.paFloat32, output=True)

tone_set = user_tones
while True:
    commands = list(input('>>>').upper())
    for command in commands:
        if command == 'U':
            print('inside 1')
            tone_set = user_tones
            continue
        elif command == 'O':
            tone_set = op_tones
            continue
        elif command == 'P':
            time.sleep(length)
            continue
        try:
            tone = tone_set[command]
        except KeyError:
            print('Invalid sequence: \'{}\'. Ignoring'.format(command))
            continue
            #f1 = sin(2pi fs*duration * f/fs)
        
        f1 = (np.sin(2 * np.pi * np.arange(sr*length)*tone[0]/sr)).astype(np.float32)
        f2 = (np.sin(2 * np.pi * np.arange(sr*length)*tone[1]/sr)).astype(np.float32)
        stream = p.open(format=pyaudio.paFloat32,channels=1,rate=sr,output=True)
        stream.write(volume*(f1+f2))
        stream.stop_stream()
        stream.close()

            #sample = (volume * math.sin(2.0 * math.pi * length * tone[0] / float(sr)) + volume * math.sin(2.0 * math.pi * i * tone[1] / float(sr))
            #stream.write(array.array('f', sample).tostring())

            #samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

        # for paFloat32 sample values must be in range [-1.0, 1.0]
        #stream = p.open(format=pyaudio.paFloat32,channels=1,rate=fs,output=True)

        # play. May repeat with different volume values (if done interactively) 
        #stream.write(volume*samples)

        


#stream.close()
p.terminate()