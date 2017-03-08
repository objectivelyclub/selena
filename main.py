import midiparser
import qr

import mido
import base64
from random import randint

import argparse
argparser = argparse.ArgumentParser() 
argparser.add_argument('input_path', help="The path of the input MIDI file.")
argparser.add_argument('output_path', help="The base pathname of the QR image files to output.")
argparser.add_argument('--messages_per_qr', help="The number of MIDI messages a single QR code should contain.", default=50)
argparser.add_argument('--frame_duration', help="The duration, in ms, of each frame of the generated GIF.", default=700)
argparser.add_argument('--debug_note_bytes', action='store_true', help="Whether to output a file, raw_bytes_dump, that contains all note messages in byte format.")
args = argparser.parse_args()

midiFile = mido.MidiFile(args.input_path)
noteMessageList = midiparser.parseForNoteMessages(midiFile)
programHeader = midiparser.getMIDIProgramInfo(midiFile)
noteByteList = midiparser.noteMessagesToBytes(noteMessageList)

if args.debug_note_bytes:
    with open('raw_bytes_dump', 'wb') as fout:
        for noteBytes in noteByteList:
            fout.write(noteBytes)

songnum = randint(0, 255)
msgsperhalfsecond = midiparser.getDataRate(midiFile)

image_frames = []

for i in range(len(noteByteList) // msgsperhalfsecond):
    dataInd = i * msgsperhalfsecond
    data = i.to_bytes(2, 'little') + songnum.to_bytes(1,'little') + programHeader + msgsperhalfsecond.to_bytes(1,'little') + b''.join(noteByteList[dataInd:dataInd+msgsperhalfsecond])
    data = base64.b64encode(data)

    image = qr.generateQRImage(data)
    image_frames.append(image)

image_frames[0].save(args.output_path + ".gif", format='GIF', duration=args.frame_duration, save_all=True, append_images=image_frames[1:], optimize=True)
