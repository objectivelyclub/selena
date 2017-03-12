import midiparser
import qr
import os

import mido
import base64
from random import randint

import argparse
argparser = argparse.ArgumentParser()
argparser.add_argument('input_path', nargs='+', help="The path of the input MIDI file.")
argparser.add_argument('--messages_per_qr', help="The number of MIDI messages a single QR code should contain.", default=50)
argparser.add_argument('--frame_duration', help="The duration, in ms, of each frame of the generated GIF.", default=700)
argparser.add_argument('--debug_note_bytes', action='store_true', help="Whether to output a file, raw_bytes_dump, that contains all note messages in byte format.")
args = argparser.parse_args()

for fname in args.input_path:
    print("Processing %s" % fname)
    midiFile = mido.MidiFile(fname)
    noteMessageList = midiparser.parseForNoteMessages(midiFile)
    programHeader = midiparser.getMIDIProgramInfo(midiFile)
    noteByteList = midiparser.noteMessagesToBytes(noteMessageList)

    if args.debug_note_bytes:
        with open('raw_bytes_dump', 'wb') as fout:
            for noteBytes in noteByteList:
                fout.write(noteBytes)

    songnum = randint(0, 255)
    messagesPerFrame = midiparser.getDataRate(midiFile, args.frame_duration)

    image_frames = []

    dataInd = 0;
    counter = 0;
    for i in messagesPerFrame:
        counter++
        dataHeader = counter.to_bytes(2, 'little') + songnum.to_bytes(1,'little') + programHeader + messagesPerFrame.to_bytes(1,'little')
        data = dataHeader + b''.join(noteByteList[dataInd:dataInd+i])

        dataInd = i + dataInd
        data = base64.b64encode(data)

        image = qr.generateQRImage(data)
        image_frames.append(image)

    basename = os.path.basename(fname)
    filename, ext = os.path.splitext(basename)
    image_frames[0].save(filename + ".gif", format='GIF', duration=args.frame_duration, save_all=True, append_images=image_frames[1:], optimize=True)
