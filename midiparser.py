import mido
import struct
import time

def parseForNoteMessages(midiFile):
    """
    Parses the midi file for Channel Voice Messages,
    i.e. all messages that have to do with note output.
    Args:
        midiFile: A mido.MidiFile object.
    Returns:
        A list of all note-related MIDI messages as mido.Message objects.
    """
    noteMessageList = []

    for message in midiFile: # This provides delta time in seconds, not ticks.
        if not isinstance(message, mido.MetaMessage):
                if message.type == 'note_on' or message.type == 'note_off':
                    noteMessageList.append(message)

    return noteMessageList

def getMIDIProgramInfo(midiFile):
    """
    Gets the Program (i.e. instrument) associated with each Channel.
    Args:
        midiFile: A mido.MidiFile object.
        This file should only contain 1 track.
    Returns:
        A 16-byte array containing the Program Number for each channel.
    """
    ar = [0] * 16
    for track in midiFile.tracks:
        for message in track:
            if message.type == 'program_change':
                ar[message.channel] = message.program

    packed_bytes = struct.pack('16B', *ar)
    return packed_bytes

def getDataRate(midiFile, duration):
    """
    Given a MIDI file, returns a count of how many MIDI messages,
    on average, there are in a specified time duration.
    Args:
        midiFile: A mido.midiFile object.
        duration: A duration of time, in milliseconds.
    """
    duration = duration/1000.0
    n = 0
    msgtime = 0
    msgarr = []
    for message in midiFile:
        n += 1
        msgtime += message.time
        if msgtime > duration :
            msgarr.append(n)
            msgtime = 0
            n = 0

    return msgarr


def noteMessagesToBytes(messageList):
    """
    Takes a list of note messages, and packs each note message into bytes.
    Note messages are assumed to have their delta times in seconds,
    rather than ticks.
    Args:
        messageList: A list of mido.MidiMessage objects.
    """
    byteList = []
    for message in messageList:
        ls = message.bytes()
        packed_bytes = struct.pack('H%dB' % (len(ls),), (int) (message.time*1000), *ls)
        byteList.append(packed_bytes)

    return byteList
