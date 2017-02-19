import midiparser
import qr

import mido

import argparse
argparser = argparse.ArgumentParser() 
argparser.add_argument('input_path', help="The path of the input MIDI file.")
argparser.add_argument('output_path', help="The base pathname of the QR image files to output.")
argparser.add_argument('--messages_per_qr', help="The number of MIDI messages a single QR code should contain.", default=26)
args = argparser.parse_args()

midiFile = mido.MidiFile(args.input_path)
noteMessageList = midiparser.parseForNoteMessages(midiFile)
noteByteList = midiparser.noteMessagesToBytes(noteMessageList, midiFile.ticks_per_beat)

for i in range(len(noteByteList) // args.messages_per_qr):
    data = b''.join(noteByteList[i:i+args.messages_per_qr])
    image = qr.generateQRImage(data)

    image.save(args.output_path + str(i) + '.png')
