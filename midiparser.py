import mido
import struct

def parseForNoteMessages(midiFile):
    """
    Parses the midi file for messages related to notes only.
    Ignores all system real-time messages.
    Args:
        midiFile: A mido.MidiFile object.
    Returns:
        A list of all note-related MIDI messages as mido.Message objects.
    """
    noteMessageList = []
    single_track = mido.merge_tracks(midiFile.tracks)

    for message in single_track:
        if message.type == 'note_on' or message.type == 'note_off':
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
