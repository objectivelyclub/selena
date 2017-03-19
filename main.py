import midiparser
import qr
import os
import tqdm

import mido
import base64
from random import randint

import argparse
argparser = argparse.ArgumentParser()
argparser.add_argument('input_path', nargs='+', help="The path of the input MIDI file.")
argparser.add_argument('--messages_per_qr', help="The number of MIDI messages a single QR code should contain.", default=50)
argparser.add_argument('--minimum_frame_duration', help="The minimum duration, in ms, of each frame of the generated GIF.", default=1000)
argparser.add_argument('--maximum_frame_duration', help="The maximum duration, in ms, of each frame of the generated GIF.", default=2500)
argparser.add_argument('--debug_note_bytes', action='store_true', help="Whether to output a file, raw_bytes_dump, that contains all note messages in byte format.")
argparser.add_argument('--debug_QR', action='store_true', help="Whether to output a file, raw_QR_dump, that contains all QR messages in base64 byte format.")
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
    timesPerFrame, messagesPerFrame, paddingPerFrame = midiparser.getDataRate(noteMessageList, args.minimum_frame_duration, args.maximum_frame_duration)

    image_frames = []
    giflength = len(messagesPerFrame)

    dataInd = 0;
    counter = 0;
    dataArr = []

    for i in messagesPerFrame:
        counter +=1
        dataHeader = b'\x41\x13\x08' + counter.to_bytes(2, 'little') + songnum.to_bytes(1,'little') + programHeader + i.to_bytes(1,'little')
        data = dataHeader + b''.join(noteByteList[dataInd:dataInd+i])

        dataInd = i + dataInd
        data = base64.b64encode(data)    
        dataArr.append(data)
        
    if args.debug_QR:
        with open('raw_QR_dump', 'wb') as fout:
            for data in dataArr:
                fout.write(data)
                fout.write(b"==\n")

        
    version = 1
    for data in dataArr:
        if ( qr.getVersionFromSize(len(data)) > version):
            version = qr.getVersionFromSize(len(data))

    pbar = tqdm.tqdm(total=giflength, desc="Generating QRs", unit=' QRs')
    for data in dataArr:
        image = qr.generateQRImage(data,version)
        image_frames.append(image)
        pbar.update(1)
    pbar.close()

    basename = os.path.basename(fname)
    filename, ext = os.path.splitext(basename)
    image_frames[0].save(filename + ".gif", format='GIF', duration=timesPerFrame, save_all=True, append_images=image_frames[1:], optimize=False)

