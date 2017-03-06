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

def getDataRate(midiFile):
    """
    Generates a count of how many bytes, on average,
    there are in half a second of the provided MIDI file.
    """
    n = 0
    for message in midiFile:
        n=n+1

    print("Total Messages: " + str(n))
    print("Total song length: " + str(midiFile.length))
    
    msgps = n/ midiFile.length

    print("Messages per second: " + str(msgps))
    bps = msgps*7
    print("Bytes per second: " + str(bps))

    print("Bytes per 1/2 second: " + str(bps/2))
        
    
    return int(msgps/2) + 1 # +30
    

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
        packed_bytes = struct.pack('I%dB' % (len(ls),), (int) (message.time*1000), *ls)
        byteList.append(packed_bytes)

    return byteList
