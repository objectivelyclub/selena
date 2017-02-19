import mido
import struct

def parseForNoteMessages(midiFile):
    """
    Parses the midi file for messages related to notes only.
    Args:
        midiFile: A mido.MidiFile object.
    Returns:
        A list of all note-related MIDI messages as mido.Message objects.
    """
    noteMessageList = []
    for track in midiFile.tracks:
        for message in track:
            if message.type == 'note_on':
                noteMessageList.append(message)

    return noteMessageList

def noteMessagesToBytes(messageList, ticksPerBeat, tempo=500000):
    """
    Takes a list of note messages, and packs each note message into bytes.
    """
    seconds_per_beat = tempo / 1000000.0
    seconds_per_tick = seconds_per_beat / float(ticksPerBeat)

    byteList = []
    for message in messageList:
        message_time = (int)(message.time * seconds_per_tick * 1000)
        packed_bytes = struct.pack('IBBB', message_time, *message.bytes())
        byteList.append(packed_bytes)

    return byteList


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser() 
    parser.add_argument('input_path', help="The path of the input MIDI file.")
    parser.add_argument('output_path', help="The path of the file to output.")
    args = parser.parse_args()

    midiFile = mido.MidiFile(args.input_path)
    noteMessageList = parseForNoteMessages(midiFile)
    noteBytes = noteMessagesToBytes(noteMessageList, midiFile.ticks_per_beat)

    with open(args.output_path, 'wb') as fout:
        for messageBytes in noteBytes:
            fout.write(messageBytes)
