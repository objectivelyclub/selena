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

def getMaxDataRate(midiFile, period):
    """
    Given a MIDI file, returns the max noteRate based by splitting,
    the file into lengths of the specifed period.
    Args:
        midiFile: A mido.midiFile object.
        period: A duration of time, in milliseconds.
    """
    n = 0
    msgtime = 0
    maxmsgs = 0

    for message in midiFile:
        n += 1
        msgtime += message.time*1000
        if  (msgtime > period)  :
            if (n > maxmsgs):
                maxmsgs = n
            n = 0
            msgtime = 0

    return ((maxmsgs + 1)/period)

def getDataRate(midiFile, minperiod = 700, maxperiod = 2500):
    """
    Given a MIDI file, returns an array with the time for each QR code,
    the number of messages in each QR code, and the amount of padding,
    to fill a QR code
    Args:
        midiFile: A mido.midiFile object.
        minperiod: The minimum scanning period in milliseconds.
        maxperiod: The maximum scanning period in milliseconds.
    """
    maxDataRate = getMaxDataRate(midiFile, minperiod)
    notesPerQR = maxDataRate*minperiod

    n = 0
    msgtime = 0
    msgarr = []
    timearr = []
    paddingarr = []
    for message in midiFile:
        tmptime = msgtime + message.time*1000
        if  (n >= notesPerQR and tmptime > minperiod) or (tmptime > maxperiod)  :
            timearr.append(msgtime)
            msgarr.append(n)
            paddingarr.append((int) (notesPerQR - n))
            msgtime = 0
            n = 0
        if not isinstance(message, mido.MetaMessage):
            n += 1
        msgtime += message.time*1000    

    return timearr, msgarr, paddingarr


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
