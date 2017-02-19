import midiparser
import qr

import mido

import argparse
argparser = argparse.ArgumentParser() 
argparser.add_argument('input_path', help="The path of the input MIDI file.")
argparser.add_argument('output_path', help="The path of the QR image file to output.")
args = argparser.parse_args()

midiFile = mido.MidiFile(args.input_path)
noteMessageList = midiparser.parseForNoteMessages(midiFile)
noteByteList = midiparser.noteMessagesToBytes(noteMessageList, midiFile.ticks_per_beat)

messagesPerQR = 26 
for i in range(len(noteByteList) // messagesPerQR):
    data = b''.join(noteByteList[i:i+messagesPerQR])
    image = qr.generateQRImage(data)

    image.save(args.output_path + str(i) + '.png')
