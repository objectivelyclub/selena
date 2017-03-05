import midiparser
import qr

import mido
import base64

import argparse
argparser = argparse.ArgumentParser() 
argparser.add_argument('input_path', help="The path of the input MIDI file.")
argparser.add_argument('output_path', help="The base pathname of the QR image files to output.")
argparser.add_argument('--messages_per_qr', help="The number of MIDI messages a single QR code should contain.", default=26)
args = argparser.parse_args()

midiFile = mido.MidiFile(args.input_path)
noteMessageList = midiparser.parseForNoteMessages(midiFile)
noteByteList = midiparser.noteMessagesToBytes(noteMessageList, midiFile.ticks_per_beat)


image_frames = []
for i in range(len(noteByteList) // args.messages_per_qr):
    # Add frame number at beginning of data
    data = i.to_bytes(2, 'little') + b''.join(noteByteList[i:i+args.messages_per_qr])
    data = base64.b64encode(data)

    image = qr.generateQRImage(data)
    image_frames.append(image)

image_frames[0].save(args.output_path + ".gif", format='GIF', duration=1000, save_all=True, append_images=image_frames[1:], optimize=True)
